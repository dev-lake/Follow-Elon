"""Follow Elon - 基础使用示例"""

import os
from src.follow_elon.api import TwitterAPIClient, TwitterAPIError


def main():
    """主函数 - 演示API客户端的基础用法"""
    
    # 确保设置了API密钥
    api_key = os.getenv('TWITTER_API_KEY')
    if not api_key:
        print("请设置TWITTER_API_KEY环境变量")
        print("你可以复制.env.example为.env文件并填入你的API密钥")
        return
    
    # 创建API客户端
    client = TwitterAPIClient(api_key=api_key)
    
    try:
        print("=== 获取Elon Musk的用户信息 ===")
        user_info = client.get_user_info('elonmusk')
        print(f"用户名: {user_info.get('screen_name')}")
        print(f"显示名称: {user_info.get('name')}")
        print(f"粉丝数: {user_info.get('followers_count', 0):,}")
        print(f"关注数: {user_info.get('friends_count', 0):,}")
        print()
        
        print("=== 获取Elon Musk的最新推文 ===")
        tweets = client.get_user_tweets('elonmusk', count=5)
        if isinstance(tweets, list):
            for i, tweet in enumerate(tweets, 1):
                print(f"{i}. {tweet.get('full_text', tweet.get('text', ''))[:100]}...")
                print(f"   发布时间: {tweet.get('created_at')}")
                print(f"   转发数: {tweet.get('retweet_count', 0)}")
                print(f"   点赞数: {tweet.get('favorite_count', 0)}")
                print()
        
        print("=== 获取Elon Musk的回复推文 ===")
        replies = client.get_user_replies('elonmusk', count=3)
        if isinstance(replies, list):
            reply_tweets = [tweet for tweet in replies if tweet.get('in_reply_to_status_id')]
            print(f"找到 {len(reply_tweets)} 条回复推文")
            for i, reply in enumerate(reply_tweets[:3], 1):
                print(f"{i}. {reply.get('full_text', reply.get('text', ''))[:100]}...")
                print()
        
        print("=== 获取Elon Musk的转发推文 ===")
        retweets = client.get_user_retweets('elonmusk', count=3)
        if isinstance(retweets, list):
            print(f"找到 {len(retweets)} 条转发推文")
            for i, retweet in enumerate(retweets, 1):
                original = retweet.get('retweeted_status', {})
                print(f"{i}. 转发了 @{original.get('user', {}).get('screen_name', 'unknown')} 的推文:")
                print(f"   {original.get('full_text', original.get('text', ''))[:100]}...")
                print()
        
        print("=== 搜索包含Tesla的推文 ===")
        search_results = client.search_tweets('Tesla', count=3, result_type='popular')
        if 'statuses' in search_results:
            statuses = search_results['statuses']
            print(f"找到 {len(statuses)} 条相关推文")
            for i, tweet in enumerate(statuses, 1):
                print(f"{i}. @{tweet.get('user', {}).get('screen_name', 'unknown')}: {tweet.get('full_text', tweet.get('text', ''))[:100]}...")
                print()
        
    except TwitterAPIError as e:
        print(f"API错误: {e}")
        if hasattr(e, 'status_code') and e.status_code:
            print(f"状态码: {e.status_code}")
        if hasattr(e, 'response_data') and e.response_data:
            print(f"响应数据: {e.response_data}")
    
    finally:
        # 关闭客户端会话
        client.close()
        print("API客户端已关闭")


if __name__ == '__main__':
    main()