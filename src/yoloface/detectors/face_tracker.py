"""
人脸跟踪器
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
from collections import defaultdict

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

from ..utils.logger import get_logger
from ..utils.file_utils import get_model_path
from ..config import get_config

logger = get_logger(__name__)

# 延迟导入性别分类器
_gender_classifier = None

def _get_gender_classifier():
    """获取性别分类器实例（单例）"""
    global _gender_classifier
    if _gender_classifier is None:
        try:
            from .gender_classifier import GenderClassifier
            _gender_classifier = GenderClassifier()
        except Exception as e:
            logger.warning(f"无法加载性别分类器: {e}")
            _gender_classifier = None
    return _gender_classifier


class FaceTracker:
    """人脸跟踪器"""
    
    def __init__(self, model_path: Optional[str] = None, conf_threshold: Optional[float] = None, **kwargs):
        """
        初始化跟踪器
        
        Args:
            model_path: YOLO11模型文件路径
            conf_threshold: 置信度阈值
            **kwargs: 其他参数
        """
        if not YOLO_AVAILABLE:
            raise ImportError("ultralytics未安装，请运行: pip install ultralytics")
        
        config = get_config()
        
        if model_path is None:
            model_path = config.get('detection.yolo11.model_path', 'yolo11n.pt')
        
        if conf_threshold is None:
            conf_threshold = config.get('detection.yolo11.conf_threshold', 0.25)
        
        self.conf_threshold = conf_threshold
        
        try:
            full_path = get_model_path(model_path)
            logger.info(f"加载YOLO11模型: {full_path}")
            self.model = YOLO(full_path)
        except Exception as e:
            logger.error(f"加载模型失败: {e}")
            logger.info("尝试使用预训练模型...")
            self.model = YOLO('yolo11n.pt')
        
        # 跟踪参数
        tracking_config = config.get('detection.tracking', {})
        self.iou_threshold = kwargs.get('iou_threshold') or tracking_config.get('iou_threshold', 0.3)
        self.max_history = kwargs.get('max_history') or tracking_config.get('max_history', 30)
        self.track_lost_threshold = kwargs.get('track_lost_threshold') or tracking_config.get('track_lost_threshold', 5)
        
        # 跟踪数据
        self.track_history = defaultdict(list)
        self.track_colors = {}
        self.next_track_id = 0
    
    def calculate_iou(self, box1: Tuple[int, int, int, int], box2: Tuple[int, int, int, int]) -> float:
        """
        计算两个边界框的IoU
        
        Args:
            box1: (x1, y1, x2, y2)
            box2: (x1, y1, x2, y2)
            
        Returns:
            iou: IoU值
        """
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        # 计算交集
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        
        if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
            return 0.0
        
        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        
        # 计算并集
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        if union_area == 0:
            return 0.0
        
        return inter_area / union_area
    
    def update_tracks(self, detections: List[Tuple[int, int, int, int, float, int]]) -> Dict[int, Tuple[int, int, int, int, float, int]]:
        """
        更新跟踪
        
        Args:
            detections: 当前帧的检测结果 [(x1, y1, x2, y2, conf, cls), ...]
            
        Returns:
            tracks: 跟踪结果 {track_id: (x1, y1, x2, y2, conf, cls), ...}
        """
        current_tracks = {}
        used_detections = set()
        
        # 尝试匹配现有跟踪
        for track_id, history in self.track_history.items():
            if len(history) == 0:
                continue
            
            last_box = history[-1]
            best_iou = 0
            best_detection_idx = -1
            
            for idx, det in enumerate(detections):
                if idx in used_detections:
                    continue
                
                iou = self.calculate_iou(last_box[:4], det[:4])
                if iou > best_iou and iou > self.iou_threshold:
                    best_iou = iou
                    best_detection_idx = idx
            
            if best_detection_idx >= 0:
                det = detections[best_detection_idx]
                current_tracks[track_id] = det
                self.track_history[track_id].append(det[:4])
                used_detections.add(best_detection_idx)
                
                # 限制历史长度
                if len(self.track_history[track_id]) > self.max_history:
                    self.track_history[track_id].pop(0)
            else:
                # 跟踪丢失，保留历史但标记为丢失
                if len(self.track_history[track_id]) > 0:
                    self.track_history[track_id].pop(0)
        
        # 为未匹配的检测创建新跟踪
        for idx, det in enumerate(detections):
            if idx not in used_detections:
                track_id = self.next_track_id
                self.next_track_id += 1
                current_tracks[track_id] = det
                self.track_history[track_id] = [det[:4]]
                
                # 生成随机颜色
                self.track_colors[track_id] = (
                    np.random.randint(0, 255),
                    np.random.randint(0, 255),
                    np.random.randint(0, 255)
                )
        
        # 清理丢失的跟踪
        lost_tracks = [tid for tid in self.track_history.keys()
                      if tid not in current_tracks and len(self.track_history[tid]) == 0]
        for tid in lost_tracks:
            del self.track_history[tid]
            if tid in self.track_colors:
                del self.track_colors[tid]
        
        return current_tracks
    
    def detect_and_track(self, frame: np.ndarray) -> Dict[int, Tuple[int, int, int, int, float, int]]:
        """
        检测并跟踪
        
        Args:
            frame: 输入图像帧
            
        Returns:
            tracks: 跟踪结果
        """
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                detections.append((int(x1), int(y1), int(x2), int(y2), conf, cls))
        
        tracks = self.update_tracks(detections)
        return tracks
    
    def draw_tracks(
        self,
        frame: np.ndarray,
        tracks: Dict[int, Tuple[int, int, int, int, float, int]],
        show_trail: bool = True,
        show_gender: bool = True
    ) -> np.ndarray:
        """
        绘制跟踪结果
        
        Args:
            frame: 输入图像帧
            tracks: 跟踪结果
            show_trail: 是否显示轨迹
            show_gender: 是否显示性别
            
        Returns:
            frame: 绘制了跟踪框和轨迹的图像
        """
        gender_classifier = _get_gender_classifier() if show_gender else None
        
        for track_id, (x1, y1, x2, y2, conf, cls) in tracks.items():
            # 获取跟踪颜色
            color = self.track_colors.get(track_id, (0, 255, 0))
            
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # 性别识别
            label = f'ID:{track_id} {conf:.2f}'
            if gender_classifier:
                try:
                    # 提取人脸区域（确保坐标有效）
                    x1_safe = max(0, x1)
                    y1_safe = max(0, y1)
                    x2_safe = min(frame.shape[1], x2)
                    y2_safe = min(frame.shape[0], y2)
                    
                    if x2_safe > x1_safe and y2_safe > y1_safe:
                        face_roi = frame[y1_safe:y2_safe, x1_safe:x2_safe]
                        if face_roi.size > 0 and face_roi.shape[0] > 10 and face_roi.shape[1] > 10:
                            gender, gender_conf = gender_classifier.predict(face_roi)
                            if gender.value != "未知":
                                label = f'ID:{track_id} {gender.value} {gender_conf:.2f}'
                except Exception as e:
                    logger.debug(f"性别识别失败: {e}")
            
            # 绘制标签
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # 绘制轨迹
            if show_trail and track_id in self.track_history:
                history = self.track_history[track_id]
                if len(history) > 1:
                    points = []
                    for box in history[-10:]:  # 只显示最近10个点
                        cx = int((box[0] + box[2]) / 2)
                        cy = int((box[1] + box[3]) / 2)
                        points.append((cx, cy))
                    
                    for i in range(1, len(points)):
                        cv2.line(frame, points[i-1], points[i], color, 2)
        
        return frame

