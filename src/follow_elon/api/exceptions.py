"""Twitter API异常类"""


class TwitterAPIError(Exception):
    """Twitter API基础异常类"""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(TwitterAPIError):
    """认证失败异常"""
    pass


class RateLimitError(TwitterAPIError):
    """API速率限制异常"""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None, reset_time: int = None):
        super().__init__(message, status_code, response_data)
        self.reset_time = reset_time


class NotFoundError(TwitterAPIError):
    """资源未找到异常"""
    pass


class ValidationError(TwitterAPIError):
    """参数验证异常"""
    pass