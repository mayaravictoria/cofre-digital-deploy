import re
import logging
from functools import wraps

class SecureLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.sensitive_patterns = [
            (r'password["\s]*[:=]["\s]*([^"\s,}]+)', r'password="***MASKED***"'),
            (r'api[_-]?key["\s]*[:=]["\s]*([^"\s,}]+)', r'api_key="***MASKED***"'),
            (r'token["\s]*[:=]["\s]*([^"\s,}]+)', r'token="***MASKED***"'),
            (r'secret["\s]*[:=]["\s]*([^"\s,}]+)', r'secret="***MASKED***"')
        ]

    def _mask_sensitive_data(self, message):
        for pattern, replacement in self.sensitive_patterns:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        return message

    def info(self, message): self.logger.info(self._mask_sensitive_data(str(message)))
    def error(self, message): self.logger.error(self._mask_sensitive_data(str(message)))

def mask_secret(secret, visible_chars=4):
    if not secret or len(secret) <= visible_chars * 2:
        return "***MASKED***"
    return secret[:visible_chars] + "*" * (len(secret) - visible_chars * 2) + secret[-visible_chars:]

def secure_log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        secure_logger = SecureLogger(func.__module__)
        safe_kwargs = {k: (mask_secret(str(v)) if any(x in k.lower() for x in ['password', 'key', 'token', 'secret']) else v) for k, v in kwargs.items()}
        secure_logger.info(f"Executando {func.__name__} com args: {safe_kwargs}")
        try:
            result = func(*args, **kwargs)
            secure_logger.info(f"{func.__name__} executado com sucesso")
            return result
        except Exception as e:
            secure_logger.error(f"Erro em {func.__name__}: {str(e)}")
            raise
    return wrapper
