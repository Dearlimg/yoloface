# 项目整理说明

## 整理内容

本次整理已完成以下工作：

### ✅ 文档整理

所有文档文件已移动到 `doc/` 目录：

**新增文档**：
- `doc/AGE_AND_GENDER_UPGRADE_SUMMARY.md` - 年龄和性别升级总结
- `doc/COMPLETION_REPORT.md` - 完成报告
- `doc/GENDER_DETECTION_GUIDE.md` - 性别检测指南
- `doc/GENDER_DETECTION_QUICK_REFERENCE.md` - 性别检测快速参考
- `doc/GENDER_DETECTION_SUMMARY.md` - 性别检测总结
- `doc/IMPLEMENTATION_SUMMARY.md` - 实现总结
- `doc/LOGIN_GUIDE.md` - 登录指南
- `doc/QUICK_START.md` - 快速开始
- `doc/SETUP_INSTRUCTIONS.md` - 安装说明
- `doc/项目答辩介绍.md` - 项目答辩介绍
- `doc/答辩常见问题Q&A.md` - 答辩Q&A

**文档索引**：
- `doc/INDEX.md` - 完整的文档索引，按类别组织

### ✅ 脚本整理

所有脚本文件已移动到 `scripts/` 目录：

**主要脚本**（保留）：
- `scripts/check_imports.py` - 依赖检查
- `scripts/diagnose.py` - 环境诊断
- `scripts/download_gender_model.py` - 下载性别模型
- `scripts/download_haarcascades.py` - 下载Haar级联
- `scripts/exporter.py` - 模型导出
- `scripts/install.sh` - 安装脚本
- `scripts/legacy_compat.py` - 兼容性脚本
- `scripts/run_tests.py` - 测试运行
- `scripts/test_gender.py` - 性别测试

**历史脚本**（已移动，仅供参考）：
- `scripts/1.py, 2.py` - 临时测试脚本
- `scripts/age_detector.py` - 年龄检测器（旧版）
- `scripts/app_main.py` - 旧版应用入口
- `scripts/cv_test.py` - OpenCV测试
- `scripts/db_manager.py` - 数据库管理
- `scripts/debug_gender_features.py` - 性别特征调试
- `scripts/demo_workflow.py` - 演示工作流
- `scripts/gender_detector.py` - 性别检测器（旧版）
- `scripts/login_ui.py` - 登录UI
- `scripts/test_*.py` - 各种测试脚本
- `scripts/yolo_test.py` - YOLO测试
- `scripts/yolo_track.py` - YOLO跟踪

### ✅ 项目结构

整理后的项目结构：

```
yoloface/
├── src/yoloface/          # 源代码（主要功能）
│   ├── detectors/         # 检测器模块
│   ├── utils/            # 工具模块
│   ├── config/           # 配置管理
│   ├── gui/              # GUI模块
│   └── app.py            # 应用入口
├── tests/                # 单元测试
├── scripts/              # 所有脚本和工具
├── doc/                  # 所有文档
├── models/               # 模型文件
├── haarcascades/         # Haar级联文件
├── config.yaml           # 配置文件
├── requirements.txt      # 依赖列表
├── setup.py              # 安装脚本
├── pyproject.toml        # 项目配置
├── Makefile              # Make命令
└── README.md             # 主README
```

### ✅ 更新的文件

1. **README.md** - 更新了文档链接，添加了分类
2. **doc/INDEX.md** - 创建了完整的文档索引
3. **scripts/README.md** - 更新了脚本说明
4. **.gitignore** - 更新了忽略规则

## 注意事项

1. **历史脚本**：移动到 `scripts/` 的旧脚本仅供参考，不建议直接使用
2. **主要代码**：所有主要功能代码在 `src/yoloface/` 目录
3. **文档路径**：所有文档引用已更新为 `doc/` 路径
4. **脚本路径**：所有脚本引用已更新为 `scripts/` 路径

## 后续建议

1. 可以删除 `scripts/` 中的历史脚本（如果确定不再需要）
2. 可以合并重复的文档（如果有）
3. 可以添加更多测试用例到 `tests/` 目录

