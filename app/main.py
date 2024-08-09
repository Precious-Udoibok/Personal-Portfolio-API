from fastapi import FastAPI
from . import models
from .database import engine
from .routers import projects,blogs,contact,authentication


app = FastAPI(
    title="A personal portfolio website api",
    description='''This is a personal portfolio website API that including endpoints for projects (add, edit, delete,all project, single project), 
    \nblog posts (add, edit, delete,all blog posts, single blog post),\nand contact information (add, edit, delete). with authentication''',
    version="1.0.0",
)


#include your routes in your main.py 
app.include_router(projects.router)
app.include_router(blogs.router)
app.include_router(contact.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(bind=engine)

