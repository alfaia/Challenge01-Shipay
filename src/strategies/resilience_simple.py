from typing import Optional, Callable, Any
import asyncio
from functools import wraps


def retry_simple(max_attempts: int = 2, delay: float = 0.5):
    """Simplified retry without exponential backoff"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)
                    continue
            
            raise last_exception
        return wrapper
    return decorator


class SimpleCircuitBreaker:
    """Simplified circuit breaker"""
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN
        self._lock = asyncio.Lock()

    async def call(self, func: Callable):
        async with self._lock:
            if self.state == "OPEN":
                if self.last_failure_time and asyncio.get_event_loop().time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "CLOSED"
                    self.failure_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")

        try:
            result = await func()
            
            async with self._lock:
                if self.failure_count > 0:
                    self.failure_count = max(0, self.failure_count - 1)
            
            return result
            
        except Exception as e:
            async with self._lock:
                self.failure_count += 1
                self.last_failure_time = asyncio.get_event_loop().time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
            raise e


def with_simple_circuit_breaker(circuit_breaker_param):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            circuit_breaker = circuit_breaker_param(self) if callable(circuit_breaker_param) else circuit_breaker_param
            return await circuit_breaker.call(lambda: func(self, *args, **kwargs))
        return wrapper
    return decorator