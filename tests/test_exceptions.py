"""API异常类单元测试"""

import pytest
from src.follow_elon.api.exceptions import (
    TwitterAPIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError
)


class TestTwitterAPIError:
    """TwitterAPIError基础异常类测试"""
    
    def test_basic_exception(self):
        """测试基础异常创建"""
        error = TwitterAPIError("测试错误")
        assert str(error) == "测试错误"
        assert error.message == "测试错误"
        assert error.status_code is None
        assert error.response_data == {}
    
    def test_exception_with_status_code(self):
        """测试带状态码的异常"""
        error = TwitterAPIError("测试错误", status_code=400)
        assert error.status_code == 400
        assert error.message == "测试错误"
    
    def test_exception_with_response_data(self):
        """测试带响应数据的异常"""
        response_data = {"error": "详细错误信息"}
        error = TwitterAPIError("测试错误", response_data=response_data)
        assert error.response_data == response_data
    
    def test_exception_with_all_params(self):
        """测试带所有参数的异常"""
        response_data = {"error": "详细错误信息"}
        error = TwitterAPIError("测试错误", status_code=500, response_data=response_data)
        assert error.message == "测试错误"
        assert error.status_code == 500
        assert error.response_data == response_data


class TestAuthenticationError:
    """AuthenticationError认证错误测试"""
    
    def test_authentication_error_inheritance(self):
        """测试认证错误继承关系"""
        error = AuthenticationError("认证失败")
        assert isinstance(error, TwitterAPIError)
        assert str(error) == "认证失败"
    
    def test_authentication_error_with_params(self):
        """测试带参数的认证错误"""
        error = AuthenticationError("认证失败", status_code=401, response_data={"error": "Invalid token"})
        assert error.status_code == 401
        assert error.response_data["error"] == "Invalid token"


class TestRateLimitError:
    """RateLimitError速率限制错误测试"""
    
    def test_rate_limit_error_inheritance(self):
        """测试速率限制错误继承关系"""
        error = RateLimitError("速率限制")
        assert isinstance(error, TwitterAPIError)
        assert str(error) == "速率限制"
        assert error.reset_time is None
    
    def test_rate_limit_error_with_reset_time(self):
        """测试带重置时间的速率限制错误"""
        reset_time = 1640995200
        error = RateLimitError("速率限制", reset_time=reset_time)
        assert error.reset_time == reset_time
    
    def test_rate_limit_error_with_all_params(self):
        """测试带所有参数的速率限制错误"""
        reset_time = 1640995200
        response_data = {"error": "Rate limit exceeded"}
        error = RateLimitError(
            "速率限制",
            reset_time=reset_time,
            status_code=429,
            response_data=response_data
        )
        assert error.reset_time == reset_time
        assert error.status_code == 429
        assert error.response_data == response_data


class TestNotFoundError:
    """NotFoundError资源未找到错误测试"""
    
    def test_not_found_error_inheritance(self):
        """测试资源未找到错误继承关系"""
        error = NotFoundError("资源未找到")
        assert isinstance(error, TwitterAPIError)
        assert str(error) == "资源未找到"
    
    def test_not_found_error_with_params(self):
        """测试带参数的资源未找到错误"""
        error = NotFoundError("用户未找到", status_code=404, response_data={"error": "User not found"})
        assert error.status_code == 404
        assert error.response_data["error"] == "User not found"


class TestValidationError:
    """ValidationError参数验证错误测试"""
    
    def test_validation_error_inheritance(self):
        """测试参数验证错误继承关系"""
        error = ValidationError("参数验证失败")
        assert isinstance(error, TwitterAPIError)
        assert str(error) == "参数验证失败"
    
    def test_validation_error_with_params(self):
        """测试带参数的验证错误"""
        error = ValidationError("无效参数", status_code=400, response_data={"error": "Invalid parameter"})
        assert error.status_code == 400
        assert error.response_data["error"] == "Invalid parameter"


class TestExceptionChaining:
    """测试异常链和异常处理"""
    
    def test_exception_can_be_raised_and_caught(self):
        """测试异常能够正常抛出和捕获"""
        with pytest.raises(TwitterAPIError):
            raise TwitterAPIError("测试异常")
        
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("认证异常")
        
        with pytest.raises(RateLimitError):
            raise RateLimitError("速率限制异常")
        
        with pytest.raises(NotFoundError):
            raise NotFoundError("未找到异常")
        
        with pytest.raises(ValidationError):
            raise ValidationError("验证异常")
    
    def test_specific_exceptions_caught_as_base_exception(self):
        """测试具体异常能被基础异常类捕获"""
        with pytest.raises(TwitterAPIError):
            raise AuthenticationError("认证异常")
        
        with pytest.raises(TwitterAPIError):
            raise RateLimitError("速率限制异常")
        
        with pytest.raises(TwitterAPIError):
            raise NotFoundError("未找到异常")
        
        with pytest.raises(TwitterAPIError):
            raise ValidationError("验证异常")