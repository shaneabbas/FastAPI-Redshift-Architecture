# Importing Python packages
import traceback
from passlib.hash import pbkdf2_sha256

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_USER, TABLE_ROLE, TABLE_USER_SYSTEM_DESCRIPTION
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserInSchema, UserSchema, UserPutInSchema, UserPatchInSchema, UserPatchSchema, UserPutInSchema, \
    UserSystemDescriptionInSchema, UserSystemDescriptionPatchInSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user
from routers.user_system_description import create_user_system_description, get_user_system_description, \
    update_user_system_description, partial_update_user_system_description, delete_user_system_description


# Router Object to Create Routes
router = APIRouter(
    prefix='/user',
    tags=["User"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single user in yt_user table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single user",
             response_model=UserSchema,
             response_description="User created successfully")
async def create_user(record: UserInSchema,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a user with following information:

        - **first_name**: First name of user. (STR) *--Required*
        - **last_name**: Last name of user. (STR) *--Required*
        - **contact**: Contact number of user. (STR) *--Optional*
        - **email**: Email address of user. (STR) *--Required*
        - **username**: Username of user. (STR) *--Required*
        - **password**: Password of user. (STR) *--Required*
        - **company_name**: Company name of user. (STR) *--Optional*
        - **address**: Address of user. (STR) *--Optional*
        - **city**: City of user. (STR) *--Optional*
        - **country**: Country of user. (STR) *--Optional*
        - **postal_code**: Postal code of user. (STR) *--Optional*
        - **group_id**: Foreign key of group table. (INT) *--Required*
        - **role_id**: Foreign key to yt_role table. (INT) *--Required*
        - **license_id**: Foreign key to yt_license table. (INT) *--Required*

    """
    print("Calling create_user method")

    try:
        # Check if user already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE username = '{record.username.lower()}';"
        user_result = await database.execute_query(query=query)

        if user_result:
            raise Exception("Username already exists")
            
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE email = '{record.email}';"
        email_result = await database.execute_query(query=query)

        if email_result:
            raise Exception("Email already exists")
        
        # Create user
        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_USER} (first_name, last_name, contact, email, username, password,
                                                       company_name, address, city, country, postal_code)
                    VALUES ('{record.first_name}', '{record.last_name}', '{record.contact}', '{record.email}',
                            '{record.username.lower()}', '{pbkdf2_sha256.hash(record.password)}', '{record.company_name}',
                            '{record.address}', '{record.city}', '{record.country}', '{record.postal_code}');
                """
        last_record_id = await database.execute_query(query=query)

        user_query = f"SELECT * FROM {SCHEMA}.{TABLE_USER} WHERE username = '{record.username.lower()}';"
        user_record = await database.execute_query(query=user_query)

        await create_user_system_description(record=UserSystemDescriptionInSchema(user_id=user_record[0]["id"],
                                                                                  group_id=record.group_id,
                                                                                  role_id=record.role_id,
                                                                                  license_id=record.license_id))
    
    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)
    
    if user_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")
    
    if email_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    if last_record_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")
    
    return {**record.dict(), "id": user_record[0]["id"]}


# Gets a single user from yt_user table based on id
@router.get('/{user_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single user by providing Id",
            response_model=UserSchema,
            response_description="User fetched successfully")
async def get_user(user_id: int,
                   current_user: UserSchema = Security(get_current_active_user,
                                                       scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single user with following information:

        - **id**: Id of the user. (INT)
        - **first_name**: First name of user. (STR)
        - **last_name**: Last name of user. (STR)
        - **contact**: Contact number of user. (STR)
        - **email**: Email address of user. (STR)
        - **username**: Username of user. (STR)
        - **company_name**: Company name of user. (STR)
        - **address**: Address of user. (STR)
        - **city**: City of user. (STR)
        - **country**: Country of user. (STR)
        - **postal_code**: Postal code of user. (STR)
        - **group_id**: Foreign key of group table. (INT)
        - **role_id**: Foreign key to yt_role table. (INT)
        - **license_id**: Foreign key to yt_license table. (INT)
        - **created_at**: Datetime of the user creation. (DATETIME)
        - **updated_at**: Datetime of the user updation. (DATETIME)

    """
    print("Calling get_user method")
    
    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_USER} WHERE id = {user_id};"
        result = await database.execute_query(query=query)

        user_system_desc = await get_user_system_description(user_id=user_id)
        del user_system_desc["user_id"]
        del user_system_desc["created_at"]
        del user_system_desc["updated_at"]

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Id does not exist")

    return {**result[0], **user_system_desc}


# Get all users from yt_user table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all users",
            response_model=Page[UserSchema],
            response_description="Users fetched successfully")
async def get_all_users(current_user: UserSchema = Security(get_current_active_user,
                                                            scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all users with following information:

        - **id**: Id of the user. (INT)
        - **first_name**: First name of user. (STR)
        - **last_name**: Last name of user. (STR)
        - **contact**: Contact number of user. (STR)
        - **email**: Email address of user. (STR)
        - **username**: Username of user. (STR)
        - **company_name**: Company name of user. (STR)
        - **address**: Address of user. (STR)
        - **city**: City of user. (STR)
        - **country**: Country of user. (STR)
        - **postal_code**: Postal code of user. (STR)
        - **group_id**: Foreign key of group table. (INT)
        - **role_id**: Foreign key to yt_role table. (INT)
        - **license_id**: Foreign key to yt_license table. (INT)
        - **created_at**: Datetime of the user creation. (DATETIME)
        - **updated_at**: Datetime of the user updation. (DATETIME)

    """
    print("Calling get_all_users method")
    
    try:
        query = f"""SELECT {SCHEMA}.{TABLE_USER}.*, {SCHEMA}.{TABLE_ROLE}.role_name, {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}.*
                    FROM {SCHEMA}.{TABLE_USER}
                    JOIN {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}
                        ON {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}.user_id = {SCHEMA}.{TABLE_USER}.id
                    JOIN {SCHEMA}.{TABLE_ROLE}
                        ON {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}.role_id = {SCHEMA}.{TABLE_ROLE}.id;
                """
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates single user from yt_user table based on id
@router.put('/{user_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update single user by providing Id",
            response_model=UserSchema,
            response_description="User updated successfully")
async def update_user(user_id: int, record: UserPutInSchema,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the user by providing id:

        - **first_name**: First name of user. (STR) *--Required*
        - **last_name**: Last name of user. (STR) *--Required*
        - **contact**: Contact number of user. (STR) *--Optional*
        - **email**: Email address of user. (STR) *--Required*
        - **username**: Username of user. (STR) *--Required*
        - **company_name**: Company name of user. (STR) *--Optional*
        - **address**: Address of user. (STR) *--Optional*
        - **city**: City of user. (STR) *--Optional*
        - **country**: Country of user. (STR) *--Optional*
        - **postal_code**: Postal code of user. (STR) *--Optional*
        - **group_id**: Foreign key of group table. (INT) *--Required*
        - **role_id**: Foreign key to yt_role table. (INT) *--Required*
        - **license_id**: Foreign key to yt_license table. (INT) *--Required*

    """
    print("Calling update_user method")
    
    try:
        # Check if user exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE id = {user_id};"
        id_query = await database.execute_query(query=query)
        
        if not id_query:
            raise Exception("Id does not exist")

        # Check if username already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE username = '{record.username.lower()}';"
        user_query = await database.execute_query(query=query)

        if user_query:
            raise Exception("Username already exists")
        
        # Check if email already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE email = '{record.email}';"
        email_query = await database.execute_query(query=query)

        if email_query:
            raise Exception("Email already exists")
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_USER}
                    SET first_name = '{record.first_name}', last_name = '{record.last_name}', contact = '{record.contact}',
                        email = '{record.email}', company_name = '{record.company_name}', address = '{record.address}',
                        city = '{record.city}', country = '{record.country}', postal_code = '{record.postal_code}'
                    WHERE id = {user_id}
                """
        result = await database.execute_query(query=query)

        await update_user_system_description(user_id=user_id, record=UserSystemDescriptionInSchema(user_id=user_id,
                                                                                                   group_id=record.group_id,
                                                                                                   role_id=record.role_id,
                                                                                                   license_id=record.license_id))

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not id_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID does not exist")

    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")
    
    if email_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    if result == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.dict(), "id": user_id}


# Partial updates single user from yt_user table based on id
@router.patch('/{user_id}/', status_code=status.HTTP_202_ACCEPTED,
              summary="Partial update a single user by providing Id",
              response_model=UserPatchSchema,
              response_description="User updated successfully")
async def partial_update_user(user_id: int, record: UserPatchInSchema,
                              current_user: UserSchema = Security(get_current_active_user,
                                                                  scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the user by providing id:

        - **first_name**: First name of user. (STR) *--Optional*
        - **last_name**: Last name of user. (STR) *--Optional*
        - **contact**: Contact number of user. (STR) *--Optional*
        - **email**: Email address of user. (STR) *--Optional*
        - **username**: Username of user. (STR) *--Optional*
        - **company_name**: Company name of user. (STR) *--Optional*
        - **address**: Address of user. (STR) *--Optional*
        - **city**: City of user. (STR) *--Optional*
        - **country**: Country of user. (STR) *--Optional*
        - **postal_code**: Postal code of user. (STR) *--Optional*

    """
    print("Calling partial_update_user method")
    
    try:
        # Check if user exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE id = {user_id};"
        id_query = await database.execute_query(query=query)
        
        if not id_query:
            raise Exception("Id does not exist")

        # Check if username already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE username = '{record.username.lower()}';"
        user_query = await database.execute_query(query=query)

        if user_query:
            raise Exception("Username already exists")
        
        # Check if email already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE email = '{record.email}';"
        email_query = await database.execute_query(query=query)

        if email_query:
            raise Exception("Email already exists")
            
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.replace(", group_id=0, role_id=0, license_id=0", "")
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_USER}
                    SET {query_string}
                    WHERE id = {user_id};
                """
        result = await database.execute_query(query=query)

        await partial_update_user_system_description(user_id=user_id, record=UserSystemDescriptionPatchInSchema(user_id=user_id,
                                                                                                                group_id=record.group_id,
                                                                                                                role_id=record.role_id,
                                                                                                                license_id=record.license_id))

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)
    
    if not id_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID does not exist")

    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")
    
    if email_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    if result == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.dict(), "id": user_id}


# Deletes a single user from yt_user table based on id
@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT,
                summary="Delete a single user by providing Id",
                response_description="User deleted successfully")
async def delete_user(user_id: int,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Removes a single user from the table by providing id

    """
    print("Calling delete_user method")
    
    try:
        # Check if user exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER} WHERE id = {user_id};"
        id_query = await database.execute_query(query=query)

        if not id_query:
            raise Exception("Id does not exist")

        query = f"DELETE FROM {SCHEMA}.{TABLE_USER} WHERE id = {user_id}"
        result = await database.execute_query(query=query)
        
        await delete_user_system_description(user_id=user_id)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)
    
    if not id_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID does not exist")
        
    if result == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return Response(status_code = status.HTTP_204_NO_CONTENT)
