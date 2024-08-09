from fastapi import APIRouter, Depends,status
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
@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_project(user_project:schemas.Projects,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.create_project(user_project,db)


#endpoints to view all projects
@router.get('/',response_model=List[schemas.ShowProjetcs])
def get_all_projects(db:Session= Depends(database.get_db)):
    #pass in the database instance
    return projects.get_all(db)


#endpoints to view a single project by id
@router.get('/{id}',response_model=schemas.ShowProjetcs)
def get_by_id(*,db:Session=Depends(database.get_db),id:int):
    return projects.get_by_id(db,id)


#endpoints to delete a project by id
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED)
#passing in the id and the database instance
def delete_project_by_id(id,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.destroy(id,db)


#endpoint to delete all the projects
@router.delete('/delete-all',status_code=status.HTTP_202_ACCEPTED)
def delete_all_projects(db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.destroy_all(db)


#endpoints to edit or update a project by id
@router.put('/{id}')
def edit_project(user_project:schemas.UpdateProject,id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return projects.update(user_project,id,db)
