# Follow Elon
X 平台 @elonmusk 活动追踪程序

## 最终实现效果
自动从数据接口获取 @elonmusk 发布的推文、回复的推文、转发的推文，并写入数据库。
将推文上下文发送给 ChatGPT，解释帖子的上下文内容，帮助用户（尤其是非英语用户）理解推文内容和潜在含义。
每日、每周、每月总结马斯克发帖内容和关注事项。

## 相关资源

### 数据获取接口文档
https://docs.twitterapi.io/api-reference

## 项目编写规定
### 使用的依赖
- uv
- python-dotenv
### 项目结构
- 实现单独的 api 层并编写单元测试