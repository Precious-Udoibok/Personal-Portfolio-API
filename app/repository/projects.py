from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status


#operations or functions for the project routers

#function to create a new project
#we will need the schema and the database instance
def create_project(user_project:schemas.Projects,db:Session):
    #create a new project using the sqlalchamey model
    new_project = models.Projects(title=user_project.title, description=user_project.description,
                                  Url = user_project.Url,technologies=user_project.technologies,
                                  date_created= user_project.date_created,date_completed=user_project.date_completed,
                                  status=user_project.status)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {f'The project {new_project.title} has been created successfully'}

#function to view all the projects in the database
def get_all(db:Session):
    projects = db.query(models.Projects).all()
    return projects

#functions to view a single projects by id
def get_by_id(db:Session,id:int):
    project = db.query(models.Projects).filter(models.Projects.id == id).first()
    #if projects is not available raise an exception
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The project with id {id} does not exists")
    return project


#function to delete a project by id
def destroy(id:int,db:Session):
    project = db.query(models.Projects).filter(models.Projects.id == id)
    #if projects does not exists
    if not project.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The project with the id {id} does not exists")
    project.delete(synchronize_session=False)
    db.commit()
    return f'Project with id {id} has been deleted successfully'


#function to delete all project
def destroy_all(db:Session):
    projects = db.query(models.Projects)
    projects.delete(synchronize_session=False)
    db.commit()
    return f'All projects has been deleted successfully'


#functions to edit or update a project by id
#passing in the schema to edit the project, id and db
def update(user_project:schemas.UpdateProject,id:int,db:Session):
    #get the project by id
    project = db.query(models.Projects).filter(models.Projects.id == id)
    #if the project is not available
    if not project.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The project with the id {id} does not exists")
    
    #incase the user doesn't want to change everything
    #if the user doesn't give any update, set it to the default
    if user_project.title == None:
        user_project.title = project.first().title

    if user_project.description == None:
        user_project.description = project.first().description

    if user_project.technologies == None:
        user_project.technologies = project.first().technologies

    if user_project.Url == None:
        user_project.Url = project.first().Url

    if user_project.status == None:
        user_project.status = project.first().status

    if user_project.date_created == None:
        user_project.date_created = project.first().date_created

    if user_project.date_completed == None:
        user_project.date_completed = project.first().date_completed

    #update the project to the user project
    project.update(user_project.dict())
    db.commit()
    return {f'Project with id {id} updated successfully'}



