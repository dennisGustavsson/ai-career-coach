from fastapi import Request, HTTPException
from typing import Dict
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        # Store user sessions: {session_id: {"count": int, "timestamp": float}}
        self.sessions: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "timestamp": time.time()})
        self.max_matches = 10  # Maximum job matches per session
        self.session_timeout = 3600 * 24  # 24 hours in seconds
    
    def get_client_identifier(self, request: Request) -> str:
        """Get unique identifier for the client using IP + User-Agent"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0]
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        user_agent = request.headers.get("User-Agent", "unknown")
        # Create a simple session ID from IP and User-Agent
        return f"{client_ip}_{hash(user_agent)}"
    
    def check_rate_limit(self, request: Request) -> bool:
        """Check if the client has exceeded rate limits"""
        client_id = self.get_client_identifier(request)
        current_time = time.time()
        
        session = self.sessions[client_id]
        
        # Reset if session has timed out
        if current_time - session["timestamp"] > self.session_timeout:
            session["count"] = 0
            session["timestamp"] = current_time
        
        # Check if limit exceeded
        if session["count"] >= self.max_matches:
            return False
        
        return True
    
    def increment_count(self, request: Request):
        """Increment the match count for a client"""
        client_id = self.get_client_identifier(request)
        self.sessions[client_id]["count"] += 1
    
    def get_remaining(self, request: Request) -> int:
        """Get remaining matches for a client"""
        client_id = self.get_client_identifier(request)
        session = self.sessions[client_id]
        current_time = time.time()
        
        # Reset if session has timed out
        if current_time - session["timestamp"] > self.session_timeout:
            return self.max_matches
        
        return max(0, self.max_matches - session["count"])
    
    def cleanup_old_sessions(self):
        """Remove expired sessions to prevent memory leaks"""
        current_time = time.time()
        expired = [
            client_id for client_id, session in self.sessions.items()
            if current_time - session["timestamp"] > self.session_timeout
        ]
        for client_id in expired:
            del self.sessions[client_id]

# Global rate limiter instance
rate_limiter = RateLimiter()
