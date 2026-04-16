from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime

class URLCreate(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_code: str
    original_url: str
    status: str # 'safe' or 'suspicious'
    created_at: datetime

class AnalyticsResponse(BaseModel):
    short_code: str
    total_clicks: int
    clicks_per_day: Dict[str, int]
