from fastapi import APIRouter, Depends,status,Path
from sqlalchemy.orm import Session
from .. import schemas,database,oauth2
from typing import List
from .. repository import projects

router = APIRouter(
    prefix='/my-portfolio/projects',
    tags=['projects'],
)

#pass in the authentication as a dependency to secure the routes.
#the user(me) has to login in order to edit, delete and create a project

#endpoints to create a new projects
@router.post('/create',status_code=status.HTTP_201_CREATED,
            summary="Create a new project projects", 
          description="Create a new project using a request body and add it to the database",
          response_description="Returns a successful created message and status code of 201")

def create_project(user_project:schemas.Projects,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.create_project(user_project,db)


#endpoints to view all projects
@router.get('/',response_model=List[schemas.ShowProjetcs],
          summary="Get all projects", 
          description="Retrieve a list of all projects from the database.",
          response_description="A list of projects with their details.")

def get_all_projects(db:Session= Depends(database.get_db)):
    #pass in the database instance
    return projects.get_all(db)


#endpoints to view a single project by id
@router.get('/{id}',response_model=schemas.ShowProjetcs,
          summary="Get a single project",
          description="Retrieve details of a single project by its ID.",
          response_description="The details of the specified project.",
          responses={
              404: {"description": "Project not found"}
          }
            )
def get_by_id(*,db:Session=Depends(database.get_db),id:int= Path(description="The ID of the project to retrieve")):
    return projects.get_by_id(db,id)


#endpoints to delete a project by id
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED,
               summary="Delete a project",
               description="Delete a single project using the id",
                response_description="The details of the specified project.",
                responses={404: {"description": "Blog post not found"}}
               )
#passing in the id and the database instance
def delete_project_by_id(id:int=Path(description="The id of the project to be deleted"),db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.destroy(id,db)


#endpoint to delete all the projects
@router.delete('/delete-all',status_code=status.HTTP_202_ACCEPTED,
               summary="Delete all projects",
               description="Delete all the projects in the databse",
                responses={202: {"description": "Projects deleted successfully"}}
                )
def delete_all_projects(db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.destroy_all(db)


#endpoints to edit or update a project by id
@router.put('/{id}',
        summary="Update a project",
          description="Update the details of an existing project by its ID.",
          response_description="The updated project details.",
          responses={
              404: {"description": "Blog post not found"}
          }
            )
def edit_project(user_project:schemas.UpdateProject,id:int=Path(description="The id of the project you want to edit"),
                 db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.update(user_project,id,db)
