# Follow Elon
X 平台 @elonmusk 活动追踪程序

## 项目简介
这是一个用于追踪和分析Elon Musk在X平台(原Twitter)上活动的程序。通过封装的API接口层，可以获取用户推文、回复、转发等数据，为后续的数据分析和内容理解提供基础。

## 功能特性
- ✅ **通用API客户端**: 封装了Twitter API的常用接口
- ✅ **推文获取**: 支持获取用户发布的推文
- ✅ **回复获取**: 支持获取用户的回复推文
- ✅ **转发获取**: 支持获取用户的转发推文
- ✅ **用户信息**: 支持获取用户基本信息
- ✅ **推文搜索**: 支持按关键词搜索推文
- ✅ **异常处理**: 完善的错误处理机制
- ✅ **单元测试**: 35个测试用例，100%通过率

## 安装和使用

### 1. 环境要求
- Python 3.10+
- Twitter API密钥 (从 [twitterapi.io](https://twitterapi.io) 获取)

### 2. 安装依赖
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install requests python-dotenv pytest pytest-mock responses
```

### 3. 配置API密钥
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的API密钥
TWITTER_API_KEY=your_twitter_api_key_here
```

### 4. 基础使用示例
```python
from src.follow_elon.api import TwitterAPIClient

# 创建API客户端
client = TwitterAPIClient()

# 获取用户推文
tweets = client.get_user_tweets('elonmusk', count=10)

# 获取用户信息
user_info = client.get_user_info('elonmusk')

# 搜索推文
search_results = client.search_tweets('Tesla', count=20)

# 关闭客户端
client.close()
```

完整的使用示例请参考 `examples/basic_usage.py`

## 项目结构
```
follow-elon/
├── src/follow_elon/           # 源代码
│   ├── __init__.py
│   └── api/                   # API层
│       ├── __init__.py
│       ├── client.py          # API客户端
│       └── exceptions.py      # 异常定义
├── tests/                     # 单元测试
│   ├── __init__.py
│   ├── test_api_client.py     # 客户端测试
│   └── test_exceptions.py     # 异常测试
├── examples/                  # 使用示例
│   └── basic_usage.py
├── .env.example              # 环境变量模板
├── pytest.ini               # 测试配置
└── pyproject.toml           # 项目配置
```

## API接口说明

### TwitterAPIClient类

#### 初始化
```python
client = TwitterAPIClient(api_key=None, base_url=None)
```
- `api_key`: API密钥，可从环境变量`TWITTER_API_KEY`获取
- `base_url`: API基础URL，默认为`https://api.twitterapi.io/v1/`

#### 主要方法

**获取用户推文**
```python
tweets = client.get_user_tweets(username, count=20, include_replies=False)
```

**获取用户回复**
```python
replies = client.get_user_replies(username, count=20)
```

**获取用户转发**
```python
retweets = client.get_user_retweets(username, count=20)
```

**获取用户信息**
```python
user_info = client.get_user_info(username)
```

**搜索推文**
```python
results = client.search_tweets(query, count=20, result_type='recent')
```

## 异常处理

项目定义了完善的异常体系：

- `TwitterAPIError`: 基础API异常
- `AuthenticationError`: 认证失败异常
- `RateLimitError`: 速率限制异常
- `NotFoundError`: 资源未找到异常
- `ValidationError`: 参数验证异常

## 运行测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行所有测试
PYTHONPATH=/workspace python -m pytest tests/ -v

# 运行特定测试文件
PYTHONPATH=/workspace python -m pytest tests/test_api_client.py -v
```

测试结果: **35个测试用例全部通过** ✅

## 未来规划

### 数据存储层
- 实现数据库集成，存储推文数据
- 支持多种数据库后端（SQLite, PostgreSQL等）

### 内容分析
- 集成ChatGPT API，分析推文内容和上下文
- 支持多语言翻译和解释

### 数据聚合
- 实现每日、每周、每月的推文内容总结
- 生成活动报告和趋势分析

### Web界面
- 开发Web管理界面
- 提供数据可视化功能

## 相关资源

- [Twitter API文档](https://docs.twitterapi.io/api-reference)
- [项目GitHub仓库](#)

## 许可证

MIT License