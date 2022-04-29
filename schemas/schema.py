import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class Message(BaseModel):
	detail: str


class Role(BaseModel):
	id_role: int = Field(...)
	role_name: str = Field(...)

	class Config:
		orm_mode = True
		allow_population_by_field_name = True


class NewRoleIn(BaseModel):
	role_id: int

	class Config:
		orm_mode = True
		allow_population_by_field_name = True


class NewPrivilegesIn(BaseModel):
	"""
	TODO: everything is ok?
	"""

	email: EmailStr
	new_privileges: int


class User(BaseModel):
	name: str = Field(...)
	surname: str = Field(...)
	email: str = Field(...)
	role_id: int = Field(...)

	class Config:
		orm_mode = True
		allow_population_by_field_name = True


class UserIn(User):
	password: str = Field(...)

	class Config:
		orm_mode = True
		allow_population_by_field_name = True


class UserSec(BaseModel):
	username: str
	disabled: Optional[bool] = None
	hashed_password: str


class UserOut(User):
	id: int = Field(...)

	class Config:
		orm_mode = True
		allow_population_by_field_name = True


class UserProfileOut(BaseModel):
	id: int = Field(...)
	name: str = Field(...)
	surname: str = Field(...)
	email: str = Field(...)
	created_on: datetime.datetime = Field(...)
	role_name: str = Field(...)


class UserAuth(BaseModel):
	username: str
	disabled: Optional[bool] = None


class NewPasswordIn(BaseModel):
	old_password: str
	new_password: str
	new_password_repeat: str


class Token(BaseModel):
	user: str
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None


class Tag(BaseModel):
	tag: str

	class Config:
		orm_mode = True
		allow_population_by_field_name = True


class TagOut(Tag):
	id: int


class PostInOut(BaseModel):
	tag_id: int
	post: str
	created_on: datetime.datetime

	class Config:
		orm_mode = True


class PostIn(BaseModel):
	post: str
	tag: str


class PostOut(PostInOut):
	id: int
	user_id:int
