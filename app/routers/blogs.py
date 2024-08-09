from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from .. import schemas,database,oauth2
from typing import List
from .. repository import blogs

router = APIRouter(
    prefix='/my-portfolio/blogs',
    tags=['blogs'],
)

#pass in the authentication as a dependency to secure the routes.
#the user(me) has to login in order to edit, delete and create a blog post


#endpoints to create a new blog post
@router.post('/create',status_code=status.HTTP_201_CREATED)
#pass in the authenticationa as a dependency to secure the route
def create_blog(user_blog:schemas.Blog,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    """ Create a new blog post returns the blog created"""
    return blogs.create_blog(user_blog,db)

#endpoints to view all blogs
@router.get('',response_model=List[schemas.ShowBlogs])
def get_all_blogs(db:Session= Depends(database.get_db)):
    #pass in the database instance
    """ View all the blog in the databse, return all blogs"""
    return blogs.get_all(db)


#endpoints to view a single blog by id
@router.get('/{id}',response_model=schemas.ShowBlogs)
def get_by_id(*,db:Session=Depends(database.get_db),id:int):
    """View a blog by id, id is an int and return the blog with the specific id"""
    return blogs.get_by_id(db,id)


#endpoints to delete a blog by id
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED)
#passing in the id and the database instance
def delete_blog_by_id(id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    """Delete the blog by id and return a successful deleted message and status code of 202"""
    return blogs.destroy(id,db)


#endpoint to delete all the blog
@router.delete('/delete-all',status_code=status.HTTP_202_ACCEPTED)
def delete_all_blogs(db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    """Delete all the blogs from the database returns a successful delete message"""
    return blogs.destroy_all(db)


#endpoints to edit or update a blog by id
@router.put('/{id}')
def edit_blog(user_blog:schemas.UpdateBlogs,id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    """Edit blog by getting the id return a successful delete message"""
    return blogs.update(user_blog,id,db)
