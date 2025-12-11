"""
登录注册系统演示脚本
展示系统的基本工作流程
"""

import time

from db_manager import DatabaseManager


def print_section(title):
    """打印分隔符"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_workflow():
    """演示工作流程"""

    print_section("登录注册系统演示")

    # 初始化数据库
    print("1. 初始化数据库连接...")
    db = DatabaseManager()

    if not db.connect():
        print("✗ 数据库连接失败")
        return False

    print("✓ 数据库连接成功")

    # 创建表
    print("\n2. 创建用户表...")
    if db.create_user_table():
        print("✓ 用户表已准备好")
    else:
        print("✗ 用户表创建失败")
        return False

    # 演示注册流程
    print_section("演示注册流程")

    test_users = [
        ("demo_user1", "password123"),
        ("demo_user2", "securepass456"),
        ("demo_user3", "mypassword789"),
    ]

    for username, password in test_users:
        print(f"注册用户: {username}")
        success, message = db.register_user(username, password)
        if success:
            print(f"  ✓ {message}")
        else:
            print(f"  ✗ {message}")
        time.sleep(0.5)

    # 演示登录流程
    print_section("演示登录流程")

    # 成功登录
    print("测试1: 正确的用户名和密码")
    success, message = db.login_user("demo_user1", "password123")
    print(f"  结果: {message}")
    if success:
        print("  ✓ 登录成功")
    else:
        print("  ✗ 登录失败")

    time.sleep(0.5)

    # 错误的密码
    print("\n测试2: 错误的密码")
    success, message = db.login_user("demo_user1", "wrongpassword")
    print(f"  结果: {message}")
    if not success:
        print("  ✓ 正确拒绝了错误的密码")

    time.sleep(0.5)

    # 不存在的用户
    print("\n测试3: 不存在的用户")
    success, message = db.login_user("nonexistent_user", "password123")
    print(f"  结果: {message}")
    if not success:
        print("  ✓ 正确拒绝了不存在的用户")

    time.sleep(0.5)

    # 演示验证规则
    print_section("演示验证规则")

    # 用户名过短
    print("测试1: 用户名过短（少于3个字符）")
    success, message = db.register_user("ab", "password123")
    print(f"  结果: {message}")

    time.sleep(0.5)

    # 密码过短
    print("\n测试2: 密码过短（少于6个字符）")
    success, message = db.register_user("testuser", "pass")
    print(f"  结果: {message}")

    time.sleep(0.5)

    # 重复的用户名
    print("\n测试3: 重复的用户名")
    success, message = db.register_user("demo_user1", "newpassword")
    print(f"  结果: {message}")

    # 显示统计信息
    print_section("系统统计")

    print("已注册的用户:")
    query = "SELECT username, created_at FROM mv_user ORDER BY created_at DESC"
    try:
        db.cursor.execute(query)
        users = db.cursor.fetchall()
        for i, (username, created_at) in enumerate(users, 1):
            print(f"  {i}. {username} (注册时间: {created_at})")
    except Exception as e:
        print(f"  ✗ 查询失败: {e}")

    # 关闭连接
    print("\n关闭数据库连接...")
    db.disconnect()
    print("✓ 连接已关闭")

    print_section("演示完成")
    print("✓ 所有演示测试已完成")
    print("\n提示: 运行 'python app_main.py' 启动完整的GUI应用程序")

    return True


if __name__ == '__main__':
    try:
        demo_workflow()
    except KeyboardInterrupt:
        print("\n\n演示已中断")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()

