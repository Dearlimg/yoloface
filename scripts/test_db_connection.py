"""
测试数据库连接
"""

from db_manager import DatabaseManager

def test_connection():
    """测试数据库连接"""
    print("正在测试数据库连接...")

    db = DatabaseManager()

    if db.connect():
        print("✓ 数据库连接成功")

        if db.create_user_table():
            print("✓ 用户表创建/验证成功")
        else:
            print("✗ 用户表创建失败")
            return False

        # 测试注册
        print("\n测试注册功能...")
        success, message = db.register_user("testuser", "password123")
        print(f"  注册结果: {message}")

        # 测试登录
        print("\n测试登录功能...")
        success, message = db.login_user("testuser", "password123")
        print(f"  登录结果: {message}")

        # 测试错误密码
        print("\n测试错误密码...")
        success, message = db.login_user("testuser", "wrongpassword")
        print(f"  登录结果: {message}")

        db.disconnect()
        print("\n✓ 所有测试完成")
        return True
    else:
        print("✗ 数据库连接失败")
        return False

if __name__ == '__main__':
    test_connection()

