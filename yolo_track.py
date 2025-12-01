"""
YOLO11人脸跟踪测试
使用YOLO11和跟踪算法实现人脸跟踪
"""

import cv2
import numpy as np
import time
from ultralytics import YOLO
from collections import defaultdict


class FaceTracker:
    """人脸跟踪器"""
    
    def __init__(self, model_path='models/yolo11n.pt', conf_threshold=0.25):
        """
        初始化跟踪器
        
        Args:
            model_path: YOLO11模型文件路径
            conf_threshold: 置信度阈值
        """
        try:
            print(f"加载YOLO11模型: {model_path}")
            self.model = YOLO(model_path)
            self.conf_threshold = conf_threshold
        except Exception as e:
            print(f"加载模型失败: {e}")
            self.model = YOLO('yolo11n.pt')
            self.conf_threshold = conf_threshold
        
        # 跟踪数据
        self.track_history = defaultdict(list)
        self.track_colors = {}
        self.next_track_id = 0
    
    def calculate_iou(self, box1, box2):
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
    
    def update_tracks(self, detections):
        """
        更新跟踪
        
        Args:
            detections: 当前帧的检测结果 [(x1, y1, x2, y2, conf, cls), ...]
            
        Returns:
            tracks: 跟踪结果 {track_id: (x1, y1, x2, y2, conf, cls), ...}
        """
        current_tracks = {}
        used_detections = set()
        iou_threshold = 0.3
        
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
                if iou > best_iou and iou > iou_threshold:
                    best_iou = iou
                    best_detection_idx = idx
            
            if best_detection_idx >= 0:
                det = detections[best_detection_idx]
                current_tracks[track_id] = det
                self.track_history[track_id].append(det[:4])
                used_detections.add(best_detection_idx)
                
                # 限制历史长度
                if len(self.track_history[track_id]) > 30:
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
    
    def detect_and_track(self, frame):
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
    
    def draw_tracks(self, frame, tracks):
        """
        绘制跟踪结果
        
        Args:
            frame: 输入图像帧
            tracks: 跟踪结果
            
        Returns:
            frame: 绘制了跟踪框和轨迹的图像
        """
        for track_id, (x1, y1, x2, y2, conf, cls) in tracks.items():
            # 获取跟踪颜色
            color = self.track_colors.get(track_id, (0, 255, 0))
            
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # 绘制标签
            label = f'ID:{track_id} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # 绘制轨迹
            if track_id in self.track_history:
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


def main():
    """主测试函数"""
    print("初始化人脸跟踪器...")
    tracker = FaceTracker()
    
    print("打开摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    print("开始跟踪，按 'q' 键退出...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 检测和跟踪
        tracks = tracker.detect_and_track(frame)
        
        # 绘制跟踪结果
        frame = tracker.draw_tracks(frame, tracks)
        
        # 计算FPS
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = 30 / elapsed
            start_time = time.time()
        
        # 显示信息
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Tracks: {len(tracks)}', (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Face Tracking', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("跟踪结束")


if __name__ == '__main__':
    main()

