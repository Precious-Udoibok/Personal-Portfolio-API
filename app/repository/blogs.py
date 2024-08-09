from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status

#operations or functions for the blog router

#function to create a new blog
#we will need the schema and the database instance
def create_blog(user_blog:schemas.Blog,db:Session):
    #create a new project using the sqlalchamey model
    new_blog = models.Blog(title=user_blog.title,content= user_blog.content,author=user_blog.author)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {f'The blog {new_blog.title} has been created successfully'}

#function to view all the blogs in the database
def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

#functions to view a single blog by id
def get_by_id(db:Session,id:int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    #if blog is not available raise an exception
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} does not exists")
    return blog


#function to delete a blog by id
def destroy(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    #if Blog does not exists
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with the id {id} does not exists")
    blog.delete(synchronize_session=False)
    db.commit()
    return f'blog with id {id} has been deleted successfully'


#function to delete all blogs
def destroy_all(db:Session):
    Blog = db.query(models.Blog)
    Blog.delete(synchronize_session=False)
    db.commit()
    return f'All Blog has been deleted successfully'


#functions to edit or update a blog by id
#passing in the schema to edit the project, id and db
def update(user_blog:schemas.UpdateBlogs,id:int,db:Session):
    #get the blog by id
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    #if the project is not available
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The project with the id {id} does not exists")
    
    #incase the user doesn't want to change everything
    #if the user doesn't give any update, set it to the default
    if user_blog.title == None:
        user_blog.title = blog.first().title

    if user_blog.content == None:
        user_blog.content = blog.first().content

    if user_blog.author == None:
        user_blog.author = blog.first().author

    #update the project to the user project
    blog.update(user_blog.dict())
    db.commit()
    return {f'Project with id {id} updated successfully'}