from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

from schemas.article_schema import ArticleSchema

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    lastname: str
    email: EmailStr
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserSchemaCreate(UserSchemaBase):
    password: str

class UserSchemaArticles(UserSchemaBase):
    articles: Optional[List[ArticleSchema]]

class UserSchemaUp(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
