import asyncio
from functools import wraps
from typing import Callable, Any, Type, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self._lock = asyncio.Lock()

    async def call(self, func: Callable):
        async with self._lock:
            if self.state == "OPEN":
                if self.last_failure_time and asyncio.get_event_loop().time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                else:
                    raise Exception("Circuit breaker is OPEN")

        try:
            result = await func()
            
            async with self._lock:
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
            return result
            
        except Exception as e:
            async with self._lock:
                self.failure_count += 1
                self.last_failure_time = asyncio.get_event_loop().time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
            raise e


def retry(max_attempts: int = 2, delay: float = 0.5):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            last_exception = Exception("Unknown error")
            
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


def with_circuit_breaker(circuit_breaker_param: Union['CircuitBreaker', Callable[[Any], 'CircuitBreaker']]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            circuit_breaker = circuit_breaker_param(self) if callable(circuit_breaker_param) else circuit_breaker_param
            return await circuit_breaker.call(lambda: func(self, *args, **kwargs))
        return wrapper
    return decorator