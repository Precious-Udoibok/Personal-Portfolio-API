from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status

#operations or functions for the Contact router

#function to create a new contact
#we will need the schema and the database instance
def create_contact(user_contact:schemas.Contact,db:Session):
    #create a new project using the sqlalchamey model
    new_contact = models.Contact(email=user_contact.email,phone=user_contact.phone,office=user_contact.office)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {f'The contact has been created successfully'}

#function to view all the contact in the database
def get_all(db:Session):
    contact = db.query(models.Contact).all()
    return contact

#functions to view a single contact by id
def get_by_id(db:Session,id:int):
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    #if blog is not available raise an exception
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The contact with id {id} does not exists")
    return contact


#function to delete a contact by id
def destroy(id:int,db:Session):
    contact = db.query(models.Contact).filter(models.Contact.id == id)
    #if Blog does not exists
    if not contact.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The contact with the id {id} does not exists")
    contact.delete(synchronize_session=False)
    db.commit()
    return f'contact with id {id} has been deleted successfully'


#function to delete all contacts
def destroy_all(db:Session):
    contact = db.query(models.Contact)
    contact.delete(synchronize_session=False)
    db.commit()
    return f'All Blog has been deleted successfully'


#functions to edit or update a blog by id
#passing in the schema to edit the project, id and db
def update(user_contact:schemas.UpdateContact,id:int,db:Session):
    #get the blog by id
    contact = db.query(models.Contact).filter(models.Contact.id == id)
    #if the project is not available
    if not contact.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The contact with the id {id} does not exists")
    
    #incase the user doesn't want to change everything
    #if the user doesn't give any update, set it to the default
    if user_contact.email == None:
        user_contact.email = contact.first().email

    if user_contact.phone == None:
        user_contact.phone = contact.first().phone

    if user_contact.office == None:
        user_contact.office = contact.first().office

    #update the project to the user project
    contact.update(user_contact.dict())
    db.commit()
    return {f'Contact with id {id} updated successfully'}