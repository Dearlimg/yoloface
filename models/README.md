# 模型文件目录

此目录用于存放训练好的模型文件。

## 模型文件说明

### YOLO11模型
- `yolo11n.pt` - YOLO11 Nano模型（轻量级，推荐用于嵌入式设备）
- `yolo11s.pt` - YOLO11 Small模型
- `yolo11m.pt` - YOLO11 Medium模型
- `yolo11l.pt` - YOLO11 Large模型
- `yolo11x.pt` - YOLO11 XLarge模型

### 获取模型

1. **自动下载**：程序首次运行时会自动从Ultralytics下载预训练模型
2. **手动下载**：访问 https://github.com/ultralytics/ultralytics 获取模型
3. **自定义训练**：使用自己的数据集训练模型

### 模型导出

使用 `exporter.py` 工具可以将PyTorch模型导出为其他格式：

```bash
# 导出为ONNX
python exporter.py --model models/yolo11n.pt --format onnx

# 导出为NCNN（用于EAIDK-310）
python exporter.py --model models/yolo11n.pt --format ncnn

# 导出所有格式
python exporter.py --model models/yolo11n.pt --format all
```

## 注意事项

- 模型文件较大，建议使用Git LFS或不上传到Git仓库
- 已添加到 `.gitignore` 中，不会被提交到版本控制

