"""
YOLO11多进程人脸检测测试
使用多进程提高检测性能
"""

import cv2
import numpy as np
import time
import multiprocessing as mp
from queue import Queue
from ultralytics import YOLO


class YOLO11MultiProcessDetector:
    """YOLO11多进程检测器"""
    
    def __init__(self, model_path='models/yolo11n.pt', conf_threshold=0.25, num_processes=2):
        """
        初始化YOLO11多进程模型
        
        Args:
            model_path: YOLO11模型文件路径
            conf_threshold: 置信度阈值
            num_processes: 进程数量
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.num_processes = min(num_processes, mp.cpu_count())
        self.input_queue = Queue(maxsize=10)
        self.output_queue = Queue(maxsize=10)
        self.processes = []
        
    def worker_process(self, worker_id):
        """工作进程函数"""
        try:
            model = YOLO(self.model_path)
            print(f"工作进程 {worker_id} 已启动")
            
            while True:
                frame_data = self.input_queue.get()
                if frame_data is None:
                    break
                
                frame, frame_id = frame_data
                results = model(frame, conf=self.conf_threshold, verbose=False)
                
                faces = []
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        faces.append((int(x1), int(y1), int(x2), int(y2), conf, cls))
                
                self.output_queue.put((frame_id, faces))
        except Exception as e:
            print(f"工作进程 {worker_id} 错误: {e}")
    
    def start_workers(self):
        """启动工作进程"""
        for i in range(self.num_processes):
            p = mp.Process(target=self.worker_process, args=(i,))
            p.start()
            self.processes.append(p)
        print(f"已启动 {self.num_processes} 个工作进程")
    
    def stop_workers(self):
        """停止工作进程"""
        for _ in range(self.num_processes):
            self.input_queue.put(None)
        for p in self.processes:
            p.join()
        print("所有工作进程已停止")
    
    def detect(self, frame, frame_id):
        """
        检测人脸（异步）
        
        Args:
            frame: 输入图像帧
            frame_id: 帧ID
            
        Returns:
            faces: 检测结果（可能为None，如果还未处理完成）
        """
        try:
            if not self.input_queue.full():
                self.input_queue.put((frame, frame_id))
        except:
            pass
        
        # 尝试获取结果
        try:
            if not self.output_queue.empty():
                result_id, faces = self.output_queue.get()
                if result_id == frame_id:
                    return faces
        except:
            pass
        
        return None
    
    def draw_detections(self, frame, faces):
        """在图像上绘制检测结果"""
        if faces is None:
            return frame
        
        for (x1, y1, x2, y2, conf, cls) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'Person {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame


def main():
    """主测试函数"""
    print("初始化YOLO11多进程检测器...")
    detector = YOLO11MultiProcessDetector(num_processes=2)
    detector.start_workers()
    
    print("打开摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        detector.stop_workers()
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    fps = 0
    frame_count = 0
    start_time = time.time()
    frame_id = 0
    current_faces = []
    
    print("开始检测，按 'q' 键退出...")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_id += 1
            
            # 异步检测
            faces = detector.detect(frame, frame_id)
            if faces is not None:
                current_faces = faces
            
            # 绘制检测结果
            frame = detector.draw_detections(frame, current_faces)
            
            # 计算FPS
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps = 30 / elapsed
                start_time = time.time()
            
            # 显示信息
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Detections: {len(current_faces)}', (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Processes: {detector.num_processes}', (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('YOLO11 Multi-Process Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        detector.stop_workers()
        cap.release()
        cv2.destroyAllWindows()
        print("检测结束")


if __name__ == '__main__':
    # 设置多进程启动方法
    mp.set_start_method('spawn', force=True)
    main()

