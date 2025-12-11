"""
测试数据库连接
验证数据库配置是否正确
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

print("=" * 60)
print("测试数据库连接")
print("=" * 60)

# 数据库配置
db_config = {
    'host': '113.44.144.219',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'xupt_sta'
}

print(f"\n数据库配置:")
print(f"  主机: {db_config['host']}")
print(f"  端口: {db_config['port']}")
print(f"  用户: {db_config['user']}")
print(f"  数据库: {db_config['database']}")
print(f"  表名: mv_user")

try:
    # 尝试导入MySQL驱动
    print("\n[1] 检查MySQL驱动...")
    try:
        import mysql.connector
        from mysql.connector import Error
        print("  ✓ 使用 mysql.connector")
        MYSQL_CONNECTOR_AVAILABLE = True
    except ImportError:
        try:
            import pymysql
            pymysql.install_as_MySQLdb()
            import MySQLdb as mysql
            from MySQLdb import Error
            print("  ✓ 使用 pymysql")
            MYSQL_CONNECTOR_AVAILABLE = False
        except ImportError:
            print("  ✗ 未安装MySQL驱动")
            print("  请运行: pip install mysql-connector-python 或 pip install pymysql")
            sys.exit(1)
    
    # 尝试连接
    print("\n[2] 尝试连接数据库...")
    connection = None
    cursor = None
    
    try:
        if MYSQL_CONNECTOR_AVAILABLE:
            connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                connect_timeout=5
            )
        else:
            connection = mysql.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                passwd=db_config['password'],
                db=db_config['database'],
                connect_timeout=5
            )
        
        print("  ✓ 数据库连接成功")
        
        # 创建游标
        cursor = connection.cursor()
        
        # 检查表是否存在
        print("\n[3] 检查表 mv_user...")
        if MYSQL_CONNECTOR_AVAILABLE:
            cursor.execute("SHOW TABLES LIKE 'mv_user'")
        else:
            cursor.execute("SHOW TABLES LIKE 'mv_user'")
        
        result = cursor.fetchone()
        if result:
            print("  ✓ 表 mv_user 已存在")
            
            # 检查表结构
            print("\n[4] 检查表结构...")
            cursor.execute("DESCRIBE mv_user")
            columns = cursor.fetchall()
            print("  表字段:")
            for col in columns:
                print(f"    - {col[0]}: {col[1]}")
            
            # 检查现有用户数量
            cursor.execute("SELECT COUNT(*) FROM mv_user")
            count = cursor.fetchone()[0]
            print(f"\n  现有用户数: {count}")
        else:
            print("  ⚠ 表 mv_user 不存在，将在首次使用时创建")
        
        # 测试查询
        print("\n[5] 测试查询...")
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"  ✓ 查询测试成功: {result[0]}")
        
        print("\n" + "=" * 60)
        print("数据库连接测试完成！")
        print("=" * 60)
        
    except Error as e:
        print(f"  ✗ MySQL错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"  ✗ 连接异常: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 关闭连接
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if connection:
            try:
                connection.close()
            except:
                pass

except KeyboardInterrupt:
    print("\n\n测试被用户中断")
    sys.exit(1)
except Exception as e:
    print(f"\n\n测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
