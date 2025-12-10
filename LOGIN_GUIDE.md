# 登录注册系统使用指南

## 功能概述

本系统在主界面前添加了一个登录注册界面，用户需要先登录或注册才能使用人脸识别系统。

## 系统架构

### 新增文件

1. **db_manager.py** - 数据库管理模块
   - 处理MySQL数据库连接
   - 实现用户注册和登录功能
   - 密码使用SHA256加密存储

2. **login_ui.py** - 登录注册UI界面
   - 提供登录界面
   - 提供注册界面
   - 支持界面切换

3. **test_db_connection.py** - 数据库连接测试脚本

## 数据库配置

### 连接信息

- **主机**: 113.44.144.219
- **端口**: 3306
- **用户名**: root
- **密码**: 123456
- **数据库**: yoloface
- **表名**: mv_user

### 表结构

```sql
CREATE TABLE mv_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 测试数据库连接

```bash
python test_db_connection.py
```

### 3. 运行主程序

```bash
python app_main.py
```

程序启动时会显示登录注册界面。

## 功能说明

### 登录界面

- 输入用户名和密码
- 点击"登录"按钮进行登录
- 点击"去注册"按钮切换到注册界面

### 注册界面

- 输入用户名（至少3个字符）
- 输入密码（至少6个字符）
- 确认密码（两次输入必须一致）
- 点击"注册"按钮进行注册
- 点击"返回登录"按钮返回登录界面

## 验证规则

### 用户名
- 长度至少3个字符
- 必须唯一（不能重复）

### 密码
- 长度至少6个字符
- 使用SHA256加密存储
- 登录时自动验证

## 错误处理

系统会显示以下错误信息：

- "用户名和密码不能为空" - 输入字段为空
- "用户名长度至少为3个字符" - 用户名过短
- "密码长度至少为6个字符" - 密码过短
- "用户名已存在" - 注册时用户名重复
- "用户不存在" - 登录时用户不存在
- "密码错误" - 登录时密码不匹配
- "两次输入的密码不一致" - 注册时密码确认不匹配

## 登录成功后

登录成功后，主窗口标题会显示当前登录用户的用户名：

```
基于EAIDK-310的人脸识别系统 - 用户: username
```

## 数据库初始化

首次运行时，系统会自动创建 `mv_user` 表（如果不存在）。

## 安全性说明

- 密码使用SHA256加密存储，不存储明文密码
- 数据库连接使用提供的凭证
- 建议在生产环境中修改数据库密码

## 故障排除

### 无法连接到数据库

1. 检查网络连接
2. 确认数据库服务器地址和端口正确
3. 验证数据库用户名和密码
4. 检查防火墙设置

### 运行 test_db_connection.py 进行诊断

```bash
python test_db_connection.py
```

## 修改数据库配置

如需修改数据库配置，编辑 `db_manager.py` 中的 `DatabaseManager` 类初始化参数：

```python
db_manager = DatabaseManager(
    host='your_host',
    port=3306,
    user='your_user',
    password='your_password',
    database='your_database'
)
```

或在 `login_ui.py` 中修改：

```python
self.db_manager = DatabaseManager(
    host='your_host',
    port=3306,
    user='your_user',
    password='your_password',
    database='your_database'
)

