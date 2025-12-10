"""
检查所有模块导入是否正常
用于验证项目依赖是否正确安装
"""

import sys

def check_import(module_name, package_name=None):
    """检查模块导入"""
    try:
        if package_name:
            __import__(package_name)
            print(f"✅ {module_name} ({package_name}) - 导入成功")
        else:
            __import__(module_name)
            print(f"✅ {module_name} - 导入成功")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - 导入失败: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - 导入时出现错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("检查项目依赖...")
    print("=" * 50)
    
    results = []
    
    # 检查基础库
    print("\n【基础库】")
    results.append(check_import("cv2", "opencv-python"))
    results.append(check_import("numpy"))
    results.append(check_import("PIL", "Pillow"))
    
    # 检查PyQt5
    print("\n【GUI库】")
    results.append(check_import("PyQt5.QtWidgets", "PyQt5"))
    results.append(check_import("PyQt5.QtCore", "PyQt5"))
    results.append(check_import("PyQt5.QtGui", "PyQt5"))
    
    # 检查深度学习库
    print("\n【深度学习库】")
    results.append(check_import("torch"))
    results.append(check_import("torchvision"))
    try:
        from ultralytics import YOLO
        print("✅ ultralytics - 导入成功")
        results.append(True)
    except Exception as e:
        print(f"❌ ultralytics - 导入失败: {e}")
        results.append(False)
    
    # 检查项目模块
    print("\n【项目模块】")
    try:
        from cv_test import HaarFaceDetector
        print("✅ cv_test - 导入成功")
        results.append(True)
    except Exception as e:
        print(f"❌ cv_test - 导入失败: {e}")
        results.append(False)
    
    try:
        from yolo_test import YOLO11FaceDetector
        print("✅ yolo_test - 导入成功")
        results.append(True)
    except Exception as e:
        print(f"❌ yolo_test - 导入失败: {e}")
        results.append(False)
    
    try:
        from yolo_track import FaceTracker
        print("✅ yolo_track - 导入成功")
        results.append(True)
    except Exception as e:
        print(f"❌ yolo_track - 导入失败: {e}")
        results.append(False)
    
    try:
        from yolo_fastestv2_test import YoloFastestV2Detector
        print("✅ yolo_fastestv2_test - 导入成功")
        results.append(True)
    except Exception as e:
        print(f"❌ yolo_fastestv2_test - 导入失败: {e}")
        results.append(False)
    
    # 总结
    print("\n" + "=" * 50)
    success_count = sum(results)
    total_count = len(results)
    print(f"检查完成: {success_count}/{total_count} 通过")
    
    if success_count == total_count:
        print("✅ 所有依赖检查通过！项目可以正常运行。")
        return 0
    else:
        print("⚠️  部分依赖缺失，请运行: pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())

