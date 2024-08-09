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
@router.post('/create',status_code=status.HTTP_201_CREATED,
             summary="Create a new blog post",
             description="Create a new blog post by providing the blog details in the request body. Requires authentication.",
             responses={
                 401: {"description": "Unauthorized. Authentication required."}
             }
             )
#pass in the authenticationa as a dependency to secure the route
def create_blog(user_blog:schemas.Blog,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return blogs.create_blog(user_blog,db)

#endpoints to view all blogs
@router.get('',response_model=List[schemas.ShowBlogs],
            summary="View all blogs",
            description="Retrieve a list of all blog posts from the database.",
            response_description="A list of all blogs with their details."
            )
def get_all_blogs(db:Session= Depends(database.get_db)):
    #pass in the database instance
    """ View all the blog in the databse, return all blogs"""
    return blogs.get_all(db)


#endpoints to view a single blog by id
@router.get('/{id}',response_model=schemas.ShowBlogs,
            summary="View a single blog by ID",
            description="Retrieve details of a single blog post by its ID.",
            response_description="The details of the specified blog post.",
            responses={
                404: {"description": "Blog post not found"}
            }
            )
def get_by_id(*,db:Session=Depends(database.get_db),id:int):
    return blogs.get_by_id(db,id)


#endpoints to delete a blog by id
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED,
               summary="Delete a blog by ID",
               description="Delete a blog post from the database by its ID. Requires authentication.",
               response_description="Returns a success message if the blog post was deleted.",
               responses={
                   404: {"description": "Blog post not found"},
                   401: {"description": "Unauthorized. Authentication required."}
               }
               )
#passing in the id and the database instance
def delete_blog_by_id(id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return blogs.destroy(id,db)


#endpoint to delete all the blog
@router.delete('/delete-all',status_code=status.HTTP_202_ACCEPTED,
               summary="Delete all blogs",
               description="Delete all blog posts from the database. Requires authentication.",
               response_description="Returns a success message if all blog posts were deleted.",
               responses={
                   401: {"description": "Unauthorized. Authentication required."}
               }
               )
def delete_all_blogs(db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return blogs.destroy_all(db)


#endpoints to edit or update a blog by id
@router.put('/{id}',
            summary="Update a blog by ID",
            description="Update the details of an existing blog post by its ID. Requires authentication.",
            responses={
                404: {"description": "Blog post not found"},
                401: {"description": "Unauthorized. Authentication required."}
            }
            )
def edit_blog(user_blog:schemas.UpdateBlogs,id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return blogs.update(user_blog,id,db)
