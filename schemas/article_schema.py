from typing import Optional
from pydantic import BaseModel, HttpUrl, ConfigDict

class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    source_url: HttpUrl
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
    