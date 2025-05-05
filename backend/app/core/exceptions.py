class SecurityException(Exception):
    """安全领域基础异常"""
    err: str = "SECURITY_ERROR"
    description: str = "安全验证异常"


class TokenDecodeError(SecurityException):
    err = "TOKEN_DECODE_FAILURE"
    description = "令牌解析失败"


class TokenExpiredError(SecurityException):
    err = "TOKEN_EXPIRED"
    description = "令牌已过期"


class TokenTypeMismatchError(SecurityException):
    err = "TOKEN_TYPE_MISMATCH"
    description = "令牌类型不匹配"

