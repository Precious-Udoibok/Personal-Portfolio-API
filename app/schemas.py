#models for pydantic 
from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from enum import Enum
from datetime import date

#class for the status of the project
class StatusEnum(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"

class Projects(BaseModel):
    title: str= Field(None, description="The title of the projects")
    description: str = Field(None, description="The description of the projects")
    Url: Optional[str] = None #the url is optional
    technologies: str = Field(None, description="The programming language used for the projects")
    date_created:date = Field(None, description="The start date of the projects")
    date_completed:Optional[date] = None #date completed is optional
    status: StatusEnum = Field(None, description="The current status of the projects")

#to show the projects without the id
class ShowProjetcs(Projects):
    class Config():
        orm = True #set it to this, because we are using the orm query

#class to edit projects
class UpdateProject(BaseModel):
    title:Optional[str] = None
    description:Optional[str]= None
    Url:Optional[str]= None
    technologies:Optional[str]= None
    date_created:Optional[date] = None
    date_completed:Optional[date] = None
    status:Optional[StatusEnum]= None

#class for blogs
class Blog(BaseModel):
    title:str = Field(None, description="The title of the blog")
    content:str = Field(None, description="The content of the blog")
    author:str = Field(None, description="The author of the blog")

#to show the projects without the id
class ShowBlogs(Blog):
    class Config():
        orm = True #set it to this, because we are using the orm query


#class to edit blogs
class UpdateBlogs(BaseModel):
    title:Optional[str] = None
    content:Optional[str] = None
    author:Optional[str] = None

#class for contacts
class Contact(BaseModel):
    email:EmailStr = Field(None, description="The email of the contact")
    phone:int = Field(None, description="The phone number of the contact")
    office:str = Field(None, description="The office of the contact")
    
class ShowContact(Contact):
    class Config():
        orm = True #set it to this, because we are using the orm query


#class to edit contact
class UpdateContact(BaseModel):
    email:Optional[EmailStr] = None
    phone:Optional[int] = None
    office:Optional[str] = None

#schema for the token
class Token(BaseModel):
    access_token:str = Field(None, description="The access token")
    token_type:str = Field(None, description="The token type")


#schema for login
class Login(BaseModel):
    email: EmailStr
    password:str

class TokenData(BaseModel):
    email: str | None = None