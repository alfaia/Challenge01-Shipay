import time
import asyncio
from typing import Dict, Optional, List
from fastapi import Request, HTTPException

# Rate limiting storage (in-memory for production)
class InMemoryStorage:
    def __init__(self):
        self.storage: Dict[str, List[float]] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[List[float]]:
        async with self._lock:
            return self.storage.get(key)
    
    async def set(self, key: str, value: List[float], expire: int) -> None:
        async with self._lock:
            self.storage[key] = value
            # Simple expiration
            asyncio.create_task(self._expire_after(key, expire))
    
    async def _expire_after(self, key: str, seconds: int) -> None:
        await asyncio.sleep(seconds)
        async with self._lock:
            if key in self.storage:
                del self.storage[key]

def get_remote_address(request: Request) -> str:
    """Get client IP address"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

storage = InMemoryStorage()

def rate_limiter(requests: int = 10, window_seconds: int = 60):
    """
    Rate limiting decorator for FastAPI endpoints
    
    Args:
        requests: Number of allowed requests
        window_seconds: Time window in seconds
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs or args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                return await func(*args, **kwargs)
            
            client_ip = get_remote_address(request)
            key = f"rate_limit:{client_ip}:{func.__name__}"
            
            current_time = time.time()
            window_start = current_time - window_seconds
            
            # Get existing requests
            stored = await storage.get(key)
            if stored is None:
                stored = []
            
            # Filter old requests
            recent_requests = [req_time for req_time in stored if req_time > window_start]
            
            # Check rate limit
            if len(recent_requests) >= requests:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Maximum {requests} requests per {window_seconds} seconds."
                )
            
            # Add current request
            recent_requests.append(current_time)
            await storage.set(key, recent_requests, window_seconds)
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator