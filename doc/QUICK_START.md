# 快速开始指南

## 一句话总结
为人脸识别系统添加了登录注册功能，用户需要先登录才能使用。

## 30秒快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行程序
python app_main.py

# 3. 在登录界面注册或登录
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `python app_main.py` | 启动主程序 |
| `python test_db_connection.py` | 测试数据库连接 |
| `python demo_workflow.py` | 演示系统功能 |

## 登录界面操作

### 注册新用户
1. 点击"去注册"按钮
2. 输入用户名（至少3个字符）
3. 输入密码（至少6个字符）
4. 确认密码
5. 点击"注册"按钮

### 登录
1. 输入用户名
2. 输入密码
3. 点击"登录"按钮

## 数据库信息

```
主机: 113.44.144.219
端口: 3306
用户名: root
密码: 123456
数据库: yoloface
表名: mv_user
```

## 新增文件

| 文件 | 说明 |
|------|------|
| `db_manager.py` | 数据库管理 |
| `login_ui.py` | 登录UI界面 |
| `test_db_connection.py` | 数据库测试 |
| `demo_workflow.py` | 系统演示 |

## 修改文件

| 文件 | 修改 |
|------|------|
| `app_main.py` | 添加登录界面 |
| `requirements.txt` | 添加MySQL依赖 |

## 常见问题

**Q: 无法连接到数据库？**
A: 检查网络连接和数据库配置

**Q: 用户名已存在？**
A: 使用不同的用户名

**Q: 密码错误？**
A: 检查大小写，确保密码正确

**Q: 如何修改数据库配置？**
A: 编辑 `db_manager.py` 中的连接参数

## 文档

- `LOGIN_GUIDE.md` - 详细使用指南
- `SETUP_INSTRUCTIONS.md` - 设置说明
- `IMPLEMENTATION_SUMMARY.md` - 实现总结

## 技术栈

- PyQt5 (GUI)
- MySQL (数据库)
- PyMySQL (驱动)
- SHA256 (加密)

## 下一步

1. 运行 `python app_main.py` 启动程序
2. 注册一个新账号
3. 使用账号登录
4. 开始使用人脸识别系统

祝你使用愉快！

