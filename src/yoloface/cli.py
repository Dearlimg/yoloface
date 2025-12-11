"""
命令行界面（无GUI版本）
用于在没有PyQt5的嵌入式设备上运行
"""

import sys
import cv2
import time
import signal
from typing import Optional

from .utils.logger import get_logger
from .utils.video import VideoCapture, FPSCounter, draw_info
from .detectors import HaarFaceDetector, YOLO11FaceDetector, YoloFastestV2Detector, FaceTracker
from .config import Config

logger = get_logger(__name__)


class CLIDetector:
    """命令行检测器"""
    
    def __init__(self, detector_type: str, config: Config):
        """
        初始化检测器
        
        Args:
            detector_type: 检测器类型 ('haar', 'yolo11', 'fastestv2', 'track')
            config: 配置对象
        """
        self.detector_type = detector_type
        self.config = config
        self.detector = None
        self.tracker = None
        self.running = False
        self.cap: Optional[VideoCapture] = None
        self.fps_counter = FPSCounter(
            config.get('performance.fps_update_interval', 30)
        )
        self.init_detector()
    
    def init_detector(self):
        """初始化检测器"""
        try:
            if self.detector_type == 'haar':
                self.detector = HaarFaceDetector()
            elif self.detector_type == 'yolo11':
                self.detector = YOLO11FaceDetector()
            elif self.detector_type == 'fastestv2':
                self.detector = YoloFastestV2Detector()
            elif self.detector_type == 'track':
                self.tracker = FaceTracker()
            logger.info(f"检测器初始化成功: {self.detector_type}")
        except Exception as e:
            logger.error(f"检测器初始化失败: {e}")
            raise
    
    def start(self):
        """开始检测"""
        try:
            camera_config = self.config.get('camera', {})
            self.cap = VideoCapture(
                index=camera_config.get('index', 0),
                width=camera_config.get('width', 640),
                height=camera_config.get('height', 480)
            )
            self.running = True
            logger.info("摄像头已打开，开始检测...")
            logger.info("按 Ctrl+C 停止检测")
            
            self.fps_counter.reset()
            frame_count = 0
            
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("无法读取摄像头帧")
                    break
                
                frame_count += 1
                
                # 检测
                if self.detector_type == 'track':
                    tracks = self.tracker.detect_and_track(frame)
                    frame = self.tracker.draw_tracks(frame, tracks)
                    detection_count = len(tracks)
                elif self.detector_type in ['haar', 'yolo11', 'fastestv2']:
                    faces = self.detector.detect(frame)
                    frame = self.detector.draw_detections(frame, faces)
                    detection_count = len(faces)
                else:
                    detection_count = 0
                
                # 计算FPS
                fps = self.fps_counter.update()
                
                # 添加信息
                algorithm_names = {
                    'haar': 'Haar',
                    'yolo11': 'YOLO11',
                    'fastestv2': 'FastestV2',
                    'track': 'Tracking'
                }
                frame = draw_info(
                    frame, fps, detection_count,
                    algorithm_names.get(self.detector_type, '')
                )
                
                # 控制台输出（每30帧输出一次）
                if frame_count % 30 == 0:
                    print(f"\r[帧 {frame_count}] FPS: {fps:.2f} | 检测数量: {detection_count} | 算法: {algorithm_names.get(self.detector_type, '')}", 
                          end='', flush=True)
                
                # 可选：保存检测结果图像
                save_config = self.config.get('output', {})
                if save_config.get('save_frames', False) and frame_count % save_config.get('save_interval', 100) == 0:
                    output_dir = save_config.get('output_dir', 'output')
                    import os
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, f'frame_{frame_count:06d}.jpg')
                    cv2.imwrite(output_path, frame)
                    logger.debug(f"保存帧: {output_path}")
                
                # 控制帧率
                time.sleep(1.0 / 30)  # 约30 FPS
            
            print()  # 换行
            logger.info("检测已停止")
            
        except KeyboardInterrupt:
            print()  # 换行
            logger.info("收到停止信号，正在关闭...")
        except Exception as e:
            logger.error(f"检测过程中出错: {e}")
            raise
        finally:
            self.stop()
    
    def stop(self):
        """停止检测"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        logger.info("资源已释放")


def run_cli(detector_type: str = 'haar', config: Optional[Config] = None):
    """
    运行命令行界面
    
    Args:
        detector_type: 检测器类型
        config: 配置对象，如果为None则使用默认配置
    """
    if config is None:
        from .config import load_config
        config = load_config()
    
    # 注册信号处理
    def signal_handler(sig, frame):
        logger.info("收到中断信号，正在退出...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        detector = CLIDetector(detector_type, config)
        detector.start()
    except Exception as e:
        logger.error(f"运行失败: {e}")
        sys.exit(1)


def main():
    """命令行主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='基于EAIDK-310的人脸识别系统（命令行版本）')
    parser.add_argument(
        '--algorithm', '-a',
        choices=['haar', 'yolo11', 'fastestv2', 'track'],
        default='haar',
        help='选择检测算法 (默认: haar)'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='配置文件路径'
    )
    parser.add_argument(
        '--camera', '-cam',
        type=int,
        default=0,
        help='摄像头索引 (默认: 0)'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    from .config import load_config
    config = load_config(args.config)
    
    # 设置摄像头索引
    if args.camera != 0:
        config.set('camera.index', args.camera)
    
    # 运行
    run_cli(args.algorithm, config)


if __name__ == '__main__':
    main()



