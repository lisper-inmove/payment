# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.1.7.4](https://github.com/so1n/protobuf_to_pydantic)
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing





class DemoCreateRequest(BaseModel):

    name: str = Field(default="") 



class DemoDeleteRequest(BaseModel):

    id: str = Field(default="") 



class DemoUpdateRequest(BaseModel):

    id: str = Field(default="") 
    name: str = Field(default="") 



class DemoQueryRequest(BaseModel):

    id: str = Field(default="") 



class DemoListRequest(BaseModel):

    latestCreateTime: int = Field(default=0) 



class DemoCommonResponse(BaseModel):

    id: str = Field(default="") 
    name: str = Field(default="") 
    createTime: int = Field(default=0) 
    updateTime: int = Field(default=0) 



class DemoListResponse(BaseModel):

    demos: typing.List[DemoCommonResponse] = Field(default_factory=list) 

