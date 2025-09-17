"""API异常类定义"""


class TwitterAPIError(Exception):
    """Twitter API基础异常类"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(TwitterAPIError):
    """认证错误异常"""
    pass


class RateLimitError(TwitterAPIError):
    """速率限制异常"""
    
    def __init__(self, message: str, reset_time: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.reset_time = reset_time


class NotFoundError(TwitterAPIError):
    """资源未找到异常"""
    pass


class ValidationError(TwitterAPIError):
    """参数验证错误异常"""
    pass