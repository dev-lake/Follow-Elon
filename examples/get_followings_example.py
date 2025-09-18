#!/usr/bin/env python3
"""获取用户关注列表的示例"""

import sys
import os

# 添加项目路径以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from follow_elon.api import TwitterAPIClient


def main():
    """主函数"""
    try:
        # 初始化客户端，使用x-api-key认证方式（默认）
        client = TwitterAPIClient(auth_type="x-api-key")
        
        # 获取用户关注列表
        username = "KaitoEasyAPI"  # 您curl示例中使用的用户名
        print(f"正在获取 @{username} 的关注列表...")
        
        # 获取关注列表
        followings = client.get_user_followings(username, count=10)
        print(f"成功获取关注列表:")
        print(f"数据类型: {type(followings)}")
        
        # 如果返回的是字典且包含数据
        if isinstance(followings, dict):
            if "data" in followings:
                users = followings["data"]
                print(f"找到 {len(users)} 个关注的用户")
                for i, user in enumerate(users[:5], 1):
                    username = user.get('username', user.get('screen_name', '未知'))
                    name = user.get('name', user.get('display_name', '未知'))
                    print(f"{i}. @{username} ({name})")
            else:
                print(f"响应数据: {followings}")
        elif isinstance(followings, list):
            print(f"找到 {len(followings)} 个关注的用户")
            for i, user in enumerate(followings[:5], 1):
                username = user.get('username', user.get('screen_name', '未知'))
                name = user.get('name', user.get('display_name', '未知'))
                print(f"{i}. @{username} ({name})")
        else:
            print(f"未预期的数据格式: {followings}")
        
        # 也可以获取粉丝列表
        print(f"\n正在获取 @{username} 的粉丝列表...")
        followers = client.get_user_followers(username, count=5)
        print(f"粉丝数据类型: {type(followers)}")
        
        # 关闭客户端
        client.close()
        
    except Exception as e:
        print(f"发生错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        if hasattr(e, 'status_code'):
            print(f"HTTP状态码: {e.status_code}")
        if hasattr(e, 'response_data'):
            print(f"响应数据: {e.response_data}")


if __name__ == "__main__":
    main()