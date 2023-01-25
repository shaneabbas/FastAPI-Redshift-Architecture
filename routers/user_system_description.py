# Importing Python packages
import traceback

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_USER_SYSTEM_DESCRIPTION
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema, UserSystemDescriptionInSchema, UserSystemDescriptionSchema, \
    UserSystemDescriptionPatchInSchema, UserSystemDescriptionPatchSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/user_system_description',
    tags=["User System Description"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single user_system_description in yt_user_system_description table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single user system description",
             response_model=UserSystemDescriptionInSchema,
             response_description="User System Description created successfully")
async def create_user_system_description(record: UserSystemDescriptionInSchema,
                                         current_user: UserSchema = Security(get_current_active_user,
                                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a user system description with following information:

        - **user_id**: Foreign key to yt_user table. (INT) *--Required*
        - **group_id**: Foreign key to yt_group table. (INT) *--Required*
        - **role_id**: Foreign key to yt_role table. (INT) *--Required*
        - **license_id**: Foreign key to yt_license table. (INT) *--Required*

    """
    print("Calling create_user_system_description method")

    try:
        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION} (user_id, group_id, role_id, license_id)
                    VALUES ({record.user_id}, {record.group_id}, {record.role_id}, {record.license_id})
                """
        last_record_id = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if last_record_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return record.dict()


# Gets a single user_system_description from yt_user_system_description table based on user_id
@router.get('/{user_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single user system description by providing user_id",
            response_model=UserSystemDescriptionSchema,
            response_description="User System Description fetched successfully")
async def get_user_system_description(user_id: int,
                                      current_user: UserSchema = Security(get_current_active_user,
                                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single user system description with following information by providing user_id:

        - **user_id**: Foreign key to yt_user table. (INT)
        - **group_id**: Foreign key to yt_group table. (INT)
        - **role_id**: Foreign key to yt_role table. (INT)
        - **license_id**: Foreign key to yt_license table. (INT)
        - **created_at**: Datetime of the user system description creation. (DATETIME)
        - **updated_at**: Datetime of the user system description updation. (DATETIME)

    """
    print("Calling get_user_system_description method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION} WHERE user_id = {user_id}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Id does not exist")

    return result[0]


# Gets all user_system_description from yt_user_system_description table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all user system descriptions",
            response_model=Page[UserSystemDescriptionSchema],
            response_description="User System Descriptions fetched successfully")
async def get_all_user_system_descriptions(current_user: UserSchema = Security(get_current_active_user,
                                                                               scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all user system descriptions with following information:

        - **user_id**: Foreign key to yt_user table. (INT)
        - **group_id**: Foreign key to yt_group table. (INT)
        - **role_id**: Foreign key to yt_role table. (INT)
        - **license_id**: Foreign key to yt_license table. (INT)
        - **created_at**: Datetime of the user system description creation. (DATETIME)
        - **updated_at**: Datetime of the user system description updation. (DATETIME)

    """
    print("Calling get_all_user_system_descriptions method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates a single user_system_description in yt_user_system_description table based on user_id
@router.put('/{user_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update a single user system description by providing user_id",
            response_model=UserSystemDescriptionSchema,
            response_description="User System Description updated successfully")
async def update_user_system_description(user_id: int, record: UserSystemDescriptionInSchema,
                                         current_user: UserSchema = Security(get_current_active_user,
                                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the user system description by providing user_id:

        - **user_id**: Foreign key to yt_user table. (INT) *--Required*
        - **group_id**: Foreign key to yt_group table. (INT) *--Required*
        - **role_id**: Foreign key to yt_role table. (INT) *--Required*
        - **license_id**: Foreign key to yt_license table. (INT) *--Required*

    """
    print("Calling update_user_system_description method")

    try:
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}
                    SET user_id = {record.user_id}, group_id = {record.group_id},
                        role_id = {record.role_id}, license_id = {record.license_id}
                    WHERE user_id = {user_id}
                """
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if result == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.dict(), "user_id": user_id}


# Partial updates single user_system_description in yt_user_system_description table based on user_id
@router.patch('/{user_id}/', status_code=status.HTTP_202_ACCEPTED,
              summary="Partial update a single user system description by providing user_id",
              response_model=UserSystemDescriptionPatchSchema,
              response_description="User System Description updated successfully")
async def partial_update_user_system_description(user_id: int,
                                                 record: UserSystemDescriptionPatchInSchema,
                                                 current_user: UserSchema = Security(get_current_active_user,
                                                                                     scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the user system description by providing user_id:

        - **user_id**: Foreign key to yt_user table. (INT) *--Optional*
        - **group_id**: Foreign key to yt_group table. (INT) *--Optional*
        - **role_id**: Foreign key to yt_role table. (INT) *--Optional*
        - **license_id**: Foreign key to yt_license table. (INT) *--Optional*

    """
    print("Calling partial_update_user_system_description method")

    try:
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}
                    SET {query_string}
                    WHERE user_id = {user_id}
                """
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if result == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.dict(), "user_id": user_id}


# Deletes a single user_system_description from yt_user_system_description table based on id
@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT,
                summary="Delete a single user system description by providing user_id",
                response_description="User System Description deleted successfully")
async def delete_user_system_description(user_id: int,
                                         current_user: UserSchema = Security(get_current_active_user,
                                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Removes a single user system description from the table by providing id

    """
    print("Calling delete_user_system_description method")

    try:
        # Check if record already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION} WHERE user_id = {user_id};"
        check_result = await database.execute_query(query=query)

        query = f"DELETE FROM {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION} WHERE user_id = {user_id};"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code = status.HTTP_204_NO_CONTENT)
