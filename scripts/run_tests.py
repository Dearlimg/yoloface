"""
运行测试脚本
"""

import sys
import subprocess
from pathlib import Path

def main():
    """运行所有测试"""
    project_root = Path(__file__).parent.parent
    
    # 运行pytest
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '-v'],
        cwd=project_root
    )
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())

