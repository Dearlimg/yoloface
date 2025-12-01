# Haar级联分类器文件

此目录用于存放OpenCV的Haar级联分类器文件。

## 获取Haar级联分类器

OpenCV已经内置了Haar级联分类器，程序会自动使用内置的文件。

如果需要使用自定义的Haar级联分类器，可以：

1. 从OpenCV源码获取：
   - 访问 https://github.com/opencv/opencv/tree/master/data/haarcascades
   - 下载所需的XML文件到此目录

2. 常用的人脸检测级联分类器：
   - `haarcascade_frontalface_default.xml` - 正面人脸检测（默认）
   - `haarcascade_frontalface_alt.xml` - 正面人脸检测（替代）
   - `haarcascade_frontalface_alt2.xml` - 正面人脸检测（替代2）
   - `haarcascade_profileface.xml` - 侧面人脸检测

## 使用方法

在代码中指定路径：
```python
detector = HaarFaceDetector('haarcascades/haarcascade_frontalface_default.xml')
```

如果不指定路径，程序会自动使用OpenCV内置的级联分类器。

