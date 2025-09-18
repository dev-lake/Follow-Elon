"""Twitter API客户端"""

import os
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv

from .exceptions import (
    TwitterAPIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

# 加载环境变量
load_dotenv()


class TwitterAPIClient:
    """Twitter API通用客户端类"""

    def __init__(self, api_key: str = None, base_url: str = None, auth_type: str = "x-api-key"):
        """
        初始化Twitter API客户端

        Args:
            api_key: API密钥，如果不提供则从环境变量TWITTER_API_KEY获取
            base_url: API基础URL，默认使用twitterapi.io
            auth_type: 认证类型，可选值: "x-api-key" 或 "bearer"
        """
        self.api_key = api_key or os.getenv("TWITTER_API_KEY")
        self.base_url = base_url or "https://api.twitterapi.io/"
        self.auth_type = auth_type

        if not self.api_key:
            raise AuthenticationError(
                "API密钥未提供，请设置TWITTER_API_KEY环境变量或传入api_key参数"
            )

        self.session = requests.Session()
        
        # 根据认证类型设置不同的头部
        if self.auth_type == "x-api-key":
            self.session.headers.update(
                {
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json",
                    "User-Agent": "follow-elon/0.1.0",
                }
            )
        elif self.auth_type == "bearer":
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "follow-elon/0.1.0",
                }
            )
        else:
            raise ValidationError("auth_type必须是 'x-api-key' 或 'bearer' 之一")

    def _make_request(
        self, method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Dict:
        """
        发送HTTP请求的通用方法

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: API端点
            params: URL参数
            data: 请求体数据

        Returns:
            API响应数据

        Raises:
            TwitterAPIError: API请求失败时抛出相应异常
        """
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        try:
            response = self.session.request(
                method=method.upper(), url=url, params=params, json=data, timeout=30
            )

            # 处理不同的HTTP状态码
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthenticationError(
                    "认证失败，请检查API密钥", response.status_code, response.json()
                )
            elif response.status_code == 404:
                raise NotFoundError("资源未找到", response.status_code, response.json())
            elif response.status_code == 429:
                # 处理速率限制
                reset_time = response.headers.get("X-RateLimit-Reset")
                reset_time = int(reset_time) if reset_time else None
                raise RateLimitError(
                    "API速率限制已达到",
                    status_code=response.status_code,
                    response_data=response.json(),
                    reset_time=reset_time,
                )
            elif response.status_code == 400:
                raise ValidationError(
                    "请求参数错误", response.status_code, response.json()
                )
            else:
                raise TwitterAPIError(
                    f"API请求失败: {response.status_code}",
                    response.status_code,
                    response.json(),
                )

        except requests.exceptions.Timeout:
            raise TwitterAPIError("请求超时")
        except requests.exceptions.ConnectionError:
            raise TwitterAPIError("网络连接错误")
        except requests.exceptions.RequestException as e:
            raise TwitterAPIError(f"请求异常: {str(e)}")

    def get_user_followings(self, username: str, count: int = 20) -> Dict:
        """
        获取用户关注列表

        Args:
            username: 用户名（不包含@符号）
            count: 返回用户数量，默认20

        Returns:
            包含关注用户数据的字典

        Raises:
            ValidationError: 参数验证失败
            TwitterAPIError: API请求失败
        """
        if not username:
            raise ValidationError("用户名不能为空")

        if not isinstance(count, int) or count < 1:
            raise ValidationError("count参数必须是大于0的整数")

        # 移除用户名前的@符号
        username = username.lstrip("@")

        params = {
            "userName": username,
            "count": count,
        }

        return self._make_request("GET", "/twitter/user/followings", params=params)

    def get_user_followers(self, username: str, count: int = 20) -> Dict:
        """
        获取用户粉丝列表

        Args:
            username: 用户名（不包含@符号）
            count: 返回用户数量，默认20

        Returns:
            包含粉丝用户数据的字典

        Raises:
            ValidationError: 参数验证失败
            TwitterAPIError: API请求失败
        """
        if not username:
            raise ValidationError("用户名不能为空")

        if not isinstance(count, int) or count < 1:
            raise ValidationError("count参数必须是大于0的整数")

        # 移除用户名前的@符号
        username = username.lstrip("@")

        params = {
            "userName": username,
            "count": count,
        }

        return self._make_request("GET", "/twitter/user/followers", params=params)

    def get_user_tweets(
        self, username: str, count: int = 20, include_replies: bool = False
    ) -> Dict:
        """
        获取用户推文

        Args:
            username: 用户名（不包含@符号）
            count: 返回推文数量，默认20，最大200
            include_replies: 是否包含回复，默认False

        Returns:
            包含推文数据的字典

        Raises:
            ValidationError: 参数验证失败
            TwitterAPIError: API请求失败
        """
        if not username:
            raise ValidationError("用户名不能为空")

        if not isinstance(count, int) or count < 1 or count > 200:
            raise ValidationError("count参数必须是1-200之间的整数")

        # 移除用户名前的@符号
        username = username.lstrip("@")

        params = {
            "screen_name": username,
            "count": count,
            "include_rts": True,  # 包含转发
            "exclude_replies": not include_replies,
            "tweet_mode": "extended",  # 获取完整推文文本
        }

        return self._make_request("GET", "/statuses/user_timeline", params=params)

    def get_user_replies(self, username: str, count: int = 20) -> Dict:
        """
        获取用户回复的推文

        Args:
            username: 用户名（不包含@符号）
            count: 返回推文数量，默认20，最大200

        Returns:
            包含回复推文数据的字典
        """
        if not username:
            raise ValidationError("用户名不能为空")

        if not isinstance(count, int) or count < 1 or count > 200:
            raise ValidationError("count参数必须是1-200之间的整数")

        username = username.lstrip("@")

        params = {
            "screen_name": username,
            "count": count,
            "include_rts": False,  # 不包含转发
            "exclude_replies": False,  # 包含回复
            "tweet_mode": "extended",
        }

        return self._make_request("GET", "/statuses/user_timeline", params=params)

    def get_user_retweets(self, username: str, count: int = 20) -> Dict:
        """
        获取用户转发的推文

        Args:
            username: 用户名（不包含@符号）
            count: 返回推文数量，默认20，最大200

        Returns:
            包含转发推文数据的字典
        """
        if not username:
            raise ValidationError("用户名不能为空")

        if not isinstance(count, int) or count < 1 or count > 200:
            raise ValidationError("count参数必须是1-200之间的整数")

        username = username.lstrip("@")

        # 首先获取用户的时间线
        params = {
            "screen_name": username,
            "count": count,
            "include_rts": True,  # 包含转发
            "exclude_replies": True,  # 排除回复
            "tweet_mode": "extended",
        }

        timeline_data = self._make_request(
            "GET", "/statuses/user_timeline", params=params
        )

        # 过滤出转发的推文
        if isinstance(timeline_data, list):
            retweets = [
                tweet for tweet in timeline_data if tweet.get("retweeted_status")
            ]
            return retweets
        elif isinstance(timeline_data, dict) and "data" in timeline_data:
            retweets = [
                tweet
                for tweet in timeline_data["data"]
                if tweet.get("retweeted_status")
            ]
            timeline_data["data"] = retweets
            return timeline_data
        else:
            return timeline_data

    def get_user_info(self, username: str) -> Dict:
        """
        获取用户信息

        Args:
            username: 用户名（不包含@符号）

        Returns:
            用户信息字典
        """
        if not username:
            raise ValidationError("用户名不能为空")

        username = username.lstrip("@")

        params = {"screen_name": username}

        return self._make_request("GET", "/users/show", params=params)

    def search_tweets(
        self, query: str, count: int = 20, result_type: str = "recent"
    ) -> Dict:
        """
        搜索推文

        Args:
            query: 搜索查询字符串
            count: 返回结果数量，默认20，最大100
            result_type: 结果类型，可选值: 'recent', 'popular', 'mixed'

        Returns:
            搜索结果字典
        """
        if not query:
            raise ValidationError("搜索查询不能为空")

        if not isinstance(count, int) or count < 1 or count > 100:
            raise ValidationError("count参数必须是1-100之间的整数")

        if result_type not in ["recent", "popular", "mixed"]:
            raise ValidationError(
                "result_type必须是 'recent', 'popular' 或 'mixed' 之一"
            )

        params = {
            "q": query,
            "count": count,
            "result_type": result_type,
            "tweet_mode": "extended",
        }

        return self._make_request("GET", "/search/tweets", params=params)

    def close(self):
        """关闭会话"""
        if self.session:
            self.session.close()