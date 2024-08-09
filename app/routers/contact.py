from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from .. import schemas,database,oauth2
from typing import List
from .. repository import contact

router = APIRouter(
    prefix='/my-portfolio/contact',
    tags=['contact'],
)

#pass in the authentication as a dependency to secure the routes.
#the user(me) has to login in order to edit, delete and create a contact

#endpoints to create a new contact post
@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_contact(user_contact:schemas.Contact,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    """Create a new contact passing in a request body return a successful messsage and status code of 201"""
    return contact.create_contact(user_contact,db)

#endpoints to view all contact
@router.get('',response_model=List[schemas.ShowContact])
def get_all_contact(db:Session= Depends(database.get_db)):
    #pass in the database instance
    return contact.get_all(db)


#endpoints to view a single contact by id
@router.get('/{id}',response_model=schemas.ShowContact)
def get_by_id(*,db:Session=Depends(database.get_db),id:int):
    return contact.get_by_id(db,id)


#endpoints to delete a contact by id
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED)
#passing in the id and the database instance
def delete_contact_by_id(id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.destroy(id,db)


#endpoint to delete all the contact
@router.delete('/delete-all',status_code=status.HTTP_202_ACCEPTED)
def delete_all_contact(db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.destroy_all(db)


#endpoints to edit or update a contact by id
@router.put('/{id}')
def edit_contact(user_contact:schemas.UpdateContact,id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.update(user_contact,id,db)
