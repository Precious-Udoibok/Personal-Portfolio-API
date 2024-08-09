from fastapi import APIRouter, Depends,status,Path
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
@router.post('/create',status_code=status.HTTP_201_CREATED,
            summary="Create a new contact info", 
          description="Create a new contact info using a request body and add it to the database",
          response_description="Returns a successful created message and status code of 201"
             )
def create_contact(user_contact:schemas.Contact,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.create_contact(user_contact,db)

#endpoints to view all contact
@router.get('',response_model=List[schemas.ShowContact],
            summary="View all contacts",
            description="Retrieve a list of all contact information from the database.",
            response_description="A list of all contacts with their details."
            )
def get_all_contact(db:Session= Depends(database.get_db)):
    #pass in the database instance
    return contact.get_all(db)


#endpoints to view a single contact by id
@router.get('/{id}',response_model=schemas.ShowContact,
            summary="View a single contact by ID",
            description="Retrieve details of a single contact by its ID.",
            response_description="The details of the specified contact.",
            responses={
                404: {"description": "Contact not found"}
            }
            )
def get_by_id(*,db:Session=Depends(database.get_db),id:int=Path(description='THE id of the contact you want to get')):
    return contact.get_by_id(db,id)


#endpoints to delete a contact by id
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED,
               summary="Delete a contact by ID",
               description="Delete a contact entry from the database by its ID.",
               response_description="Returns a success message if the contact was deleted.",
               responses={
                   404: {"description": "Contact not found"}
               }
               )
#passing in the id and the database instance
def delete_contact_by_id(id:int,db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.destroy(id,db)


#endpoint to delete all the contact
@router.delete('/delete-all',status_code=status.HTTP_202_ACCEPTED,
               summary="Delete all contacts",
               description="Delete all contact entries from the database.",
               response_description="Returns a success message if all contacts were deleted."
               )
def delete_all_contact(db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.destroy_all(db)


#endpoints to edit or update a contact by id
@router.put('/{id}',
            description="Update the details of an existing contact by its ID.",
            response_description="Returns the updated contact details.",
            responses={
                404: {"description": "Contact not found"}
            }
            )
def edit_contact(user_contact:schemas.UpdateContact,id:int=Path(description='the id of the conatact you want to update'),
                 db:Session=Depends(database.get_db),authentication=Depends(oauth2.get_current_user)):
    return contact.update(user_contact,id,db)
