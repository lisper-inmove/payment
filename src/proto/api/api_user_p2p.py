# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.1.7.4](https://github.com/so1n/protobuf_to_pydantic)
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing





class UserCreateRequest(BaseModel):

    name: str = Field(default="") 



class UserDeleteRequest(BaseModel):

    id: str = Field(default="") 



class UserUpdateRequest(BaseModel):

    id: str = Field(default="") 
    name: str = Field(default="") 



class UserQueryRequest(BaseModel):

    id: str = Field(default="") 



class UserListRequest(BaseModel):

    latestCreateTime: int = Field(default=0) 



class UserCommonResponse(BaseModel):

    id: str = Field(default="") 
    name: str = Field(default="") 
    createTime: int = Field(default=0) 
    updateTime: int = Field(default=0) 



class UserListResponse(BaseModel):

    users: typing.List[UserCommonResponse] = Field(default_factory=list) 

