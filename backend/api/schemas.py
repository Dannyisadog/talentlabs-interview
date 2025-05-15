from typing import List, Optional

from ninja import Schema


class JobIn(Schema):
    """Schema for job creation and updates"""
    title: str
    company: str
    location: str
    description: str

class JobOut(Schema):
    """Schema for job output responses"""
    id: int
    title: str
    company: str
    location: str
    description: str

class JobsResponse(Schema):
    """Schema for multiple jobs response"""
    jobs: List[JobOut]

class ErrorResponse(Schema):
    """Schema for error responses"""
    error: str

class MessageResponse(Schema):
    """Schema for success message responses"""
    message: str 