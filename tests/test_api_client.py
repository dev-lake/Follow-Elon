"""Twitter API客户端单元测试"""

import pytest
import responses
from unittest.mock import patch, MagicMock
import json

from src.follow_elon.api.client import TwitterAPIClient
from src.follow_elon.api.exceptions import (
    TwitterAPIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError
)


class TestTwitterAPIClient:
    """Twitter API客户端测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端实例"""
        return TwitterAPIClient(api_key='test_api_key')
    
    @pytest.fixture
    def mock_tweet_data(self):
        """模拟推文数据"""
        return [
            {
                "id": 1234567890,
                "full_text": "这是一条测试推文",
                "created_at": "Mon Oct 10 20:16:13 +0000 2022",
                "user": {
                    "screen_name": "elonmusk",
                    "name": "Elon Musk"
                },
                "retweeted_status": None
            },
            {
                "id": 1234567891,
                "full_text": "RT @someone: 这是一条转发推文",
                "created_at": "Mon Oct 10 20:17:13 +0000 2022",
                "user": {
                    "screen_name": "elonmusk",
                    "name": "Elon Musk"
                },
                "retweeted_status": {
                    "id": 1234567889,
                    "full_text": "这是一条转发推文"
                }
            }
        ]
    
    def test_client_initialization_with_api_key(self):
        """测试使用API密钥初始化客户端"""
        client = TwitterAPIClient(api_key='test_key')
        assert client.api_key == 'test_key'
        assert client.base_url == 'https://api.twitterapi.io/v1/'
    
    def test_client_initialization_without_api_key_raises_error(self):
        """测试没有API密钥时初始化失败"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(AuthenticationError, match="API密钥未提供"):
                TwitterAPIClient()
    
    @patch.dict('os.environ', {'TWITTER_API_KEY': 'env_api_key'})
    def test_client_initialization_from_env(self):
        """测试从环境变量获取API密钥"""
        client = TwitterAPIClient()
        assert client.api_key == 'env_api_key'
    
    @responses.activate
    def test_get_user_tweets_success(self, client, mock_tweet_data):
        """测试成功获取用户推文"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json=mock_tweet_data,
            status=200
        )
        
        result = client.get_user_tweets('elonmusk', count=10)
        assert len(result) == 2
        assert result[0]['full_text'] == '这是一条测试推文'
        
        # 验证请求参数
        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert 'screen_name=elonmusk' in request.url
        assert 'count=10' in request.url
    
    @responses.activate
    def test_get_user_tweets_with_at_symbol(self, client, mock_tweet_data):
        """测试用户名包含@符号的情况"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json=mock_tweet_data,
            status=200
        )
        
        result = client.get_user_tweets('@elonmusk')
        assert len(result) == 2
        
        # 验证@符号被正确移除
        request = responses.calls[0].request
        assert 'screen_name=elonmusk' in request.url
    
    def test_get_user_tweets_validation_errors(self, client):
        """测试获取用户推文的参数验证"""
        # 空用户名
        with pytest.raises(ValidationError, match="用户名不能为空"):
            client.get_user_tweets('')
        
        # 无效的count参数
        with pytest.raises(ValidationError, match="count参数必须是1-200之间的整数"):
            client.get_user_tweets('elonmusk', count=0)
        
        with pytest.raises(ValidationError, match="count参数必须是1-200之间的整数"):
            client.get_user_tweets('elonmusk', count=300)
        
        with pytest.raises(ValidationError, match="count参数必须是1-200之间的整数"):
            client.get_user_tweets('elonmusk', count='invalid')
    
    @responses.activate
    def test_get_user_replies_success(self, client, mock_tweet_data):
        """测试成功获取用户回复"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json=mock_tweet_data,
            status=200
        )
        
        result = client.get_user_replies('elonmusk', count=10)
        assert len(result) == 2
        
        # 验证请求参数
        request = responses.calls[0].request
        assert 'exclude_replies=False' in request.url
        assert 'include_rts=False' in request.url
    
    @responses.activate
    def test_get_user_retweets_success(self, client, mock_tweet_data):
        """测试成功获取用户转发"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json=mock_tweet_data,
            status=200
        )
        
        result = client.get_user_retweets('elonmusk', count=10)
        # 应该只返回有retweeted_status的推文
        assert len(result) == 1
        assert result[0]['retweeted_status'] is not None
    
    @responses.activate
    def test_get_user_info_success(self, client):
        """测试成功获取用户信息"""
        user_data = {
            "id": 44196397,
            "screen_name": "elonmusk",
            "name": "Elon Musk",
            "followers_count": 100000000
        }
        
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/users/show',
            json=user_data,
            status=200
        )
        
        result = client.get_user_info('elonmusk')
        assert result['screen_name'] == 'elonmusk'
        assert result['name'] == 'Elon Musk'
    
    @responses.activate
    def test_search_tweets_success(self, client, mock_tweet_data):
        """测试成功搜索推文"""
        search_result = {
            "statuses": mock_tweet_data,
            "search_metadata": {
                "count": 2,
                "query": "Tesla"
            }
        }
        
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/search/tweets',
            json=search_result,
            status=200
        )
        
        result = client.search_tweets('Tesla', count=10, result_type='recent')
        assert 'statuses' in result
        assert len(result['statuses']) == 2
        
        # 验证请求参数
        request = responses.calls[0].request
        assert 'q=Tesla' in request.url
        assert 'count=10' in request.url
        assert 'result_type=recent' in request.url
    
    def test_search_tweets_validation_errors(self, client):
        """测试搜索推文的参数验证"""
        # 空查询
        with pytest.raises(ValidationError, match="搜索查询不能为空"):
            client.search_tweets('')
        
        # 无效的count参数
        with pytest.raises(ValidationError, match="count参数必须是1-100之间的整数"):
            client.search_tweets('test', count=0)
        
        # 无效的result_type参数
        with pytest.raises(ValidationError, match="result_type必须是"):
            client.search_tweets('test', result_type='invalid')
    
    @responses.activate
    def test_authentication_error(self, client):
        """测试认证错误处理"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json={"error": "Unauthorized"},
            status=401
        )
        
        with pytest.raises(AuthenticationError, match="认证失败"):
            client.get_user_tweets('elonmusk')
    
    @responses.activate
    def test_rate_limit_error(self, client):
        """测试速率限制错误处理"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json={"error": "Rate limit exceeded"},
            status=429,
            headers={'X-RateLimit-Reset': '1640995200'}
        )
        
        with pytest.raises(RateLimitError, match="API速率限制已达到") as exc_info:
            client.get_user_tweets('elonmusk')
        
        assert exc_info.value.reset_time == 1640995200
    
    @responses.activate
    def test_not_found_error(self, client):
        """测试资源未找到错误处理"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/users/show',
            json={"error": "User not found"},
            status=404
        )
        
        with pytest.raises(NotFoundError, match="资源未找到"):
            client.get_user_info('nonexistentuser')
    
    @responses.activate
    def test_validation_error_from_api(self, client):
        """测试API返回的验证错误"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json={"error": "Bad request"},
            status=400
        )
        
        with pytest.raises(ValidationError, match="请求参数错误"):
            client.get_user_tweets('elonmusk')
    
    @responses.activate
    def test_generic_api_error(self, client):
        """测试通用API错误处理"""
        responses.add(
            responses.GET,
            'https://api.twitterapi.io/v1/statuses/user_timeline',
            json={"error": "Internal server error"},
            status=500
        )
        
        with pytest.raises(TwitterAPIError, match="API请求失败: 500"):
            client.get_user_tweets('elonmusk')
    
    def test_close_session(self, client):
        """测试关闭会话"""
        mock_session = MagicMock()
        client.session = mock_session
        
        client.close()
        mock_session.close.assert_called_once()
    
    @responses.activate
    def test_request_timeout(self, client):
        """测试请求超时处理"""
        import requests
        
        # 模拟超时异常
        with patch.object(client.session, 'request', side_effect=requests.exceptions.Timeout):
            with pytest.raises(TwitterAPIError, match="请求超时"):
                client.get_user_tweets('elonmusk')
    
    @responses.activate
    def test_connection_error(self, client):
        """测试连接错误处理"""
        import requests
        
        # 模拟连接异常
        with patch.object(client.session, 'request', side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(TwitterAPIError, match="网络连接错误"):
                client.get_user_tweets('elonmusk')
    
    def test_custom_base_url(self):
        """测试自定义基础URL"""
        custom_url = 'https://custom.api.com/v2/'
        client = TwitterAPIClient(api_key='test_key', base_url=custom_url)
        assert client.base_url == custom_url