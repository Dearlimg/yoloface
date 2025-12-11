import cv2

# 加载OpenCV内置的Haar人脸分类器（通用路径，无需手动找文件）
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 打开默认摄像头（编号0，多摄像头可换1/2等）
cap = cv2.VideoCapture(0)

while True:
    # 读取摄像头帧（ret为是否读取成功，frame为图像帧）
    ret, frame = cap.read()
    if not ret: break  # 读取失败则退出循环

    # 转换为灰度图（Haar算法要求灰度输入，减少计算量）
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测人脸（核心步骤）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # 为人脸绘制绿色矩形框
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示检测结果
    cv2.imshow('Haar Face Detection', frame)

    # 按小写q退出（需聚焦窗口）
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源，关闭窗口
cap.release()
cv2.destroyAllWindows()