# Importing Python packages
import traceback

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_ROLE
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema, RoleInSchema, RoleSchema, RolePatchInSchema, RolePatchSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/role',
    tags=["Role"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single role in yt_role table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single role",
             response_model=RoleInSchema,
             response_description="Role created successfully")
async def create_role(record: RoleInSchema,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a role with following information:

        - **role_name**: Name of role. (STR) *--Required*

    """
    print("Calling create_role method")

    try:
        # Check if role already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_ROLE} WHERE role_name = '{record.role_name.lower()}';"
        role_result = await database.execute_query(query=query)

        if role_result:
            raise Exception("Role already exists")

        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_ROLE} (role_name)
                    VALUES ('{record.role_name.lower()}');
                """
        last_record_id = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if role_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Role already exists")

    if last_record_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.__dict__}


# Gets a single role from yt_role table based on id
@router.get('/{role_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single role by providing id",
            response_model=RoleSchema,
            response_description="Role fetched successfully")
async def get_role(role_id: int,
                   current_user: UserSchema = Security(get_current_active_user,
                                                       scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single role with following information:

        - **id**: Id of role. (INT)
        - **role_name**: Name of role. (STR)
        - **created_at**: Datetime of the role creation. (DATETIME)
        - **updated_at**: Datetime of the role updation. (DATETIME)

    """
    print("Calling get_role method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_ROLE} WHERE id = {role_id};"
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


# Get all roles from yt_role table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all roles",
            response_model=Page[RoleSchema],
            response_description="Roles fetched successfully")
async def get_all_roles(current_user: UserSchema = Security(get_current_active_user,
                                                            scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all roles with following information:

        - **id**: Id of role. (INT)
        - **role_name**: Name of role. (STR)
        - **created_at**: Datetime of the role creation. (DATETIME)
        - **updated_at**: Datetime of the role updation. (DATETIME)

    """
    print("Calling get_all_roles method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_ROLE};"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates a single role in yt_role table based on id
@router.put('/{role_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update a single role by providing id",
            response_model=RoleSchema,
            response_description="Role updated successfully")
async def update_role(role_id: int, record: RoleInSchema,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the role by providing id:

        - **role_name**: Name of role. (STR) *--Required*

    """
    print("Calling update_role method")

    try:
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_ROLE}
                    SET role_name = '{record.role_name}'
                    WHERE id = {role_id};
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

    return {**record.__dict__, "id": role_id}


# Partial updates single role in yt_role table based on id
@router.patch('/{role_id}/', status_code=status.HTTP_202_ACCEPTED,
                summary="Partial update a single role by providing id",
                response_model=RolePatchSchema,
                response_description="Role updated successfully")
async def partial_update_role(role_id: int, record: RolePatchInSchema,
                              current_user: UserSchema = Security(get_current_active_user,
                                                                  scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the role by providing id:

        - **role_name**: Name of role. (STR) *--Optional*
            
    """
    print("Calling partial_update_role method")

    try:
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_ROLE}
                    SET {query_string}
                    WHERE id = {role_id};
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

    return {**record.__dict__, "id": role_id}


# Deletes a single role from yt_role table based on id
@router.delete('/{role_id}/', status_code=status.HTTP_204_NO_CONTENT,
                summary="Delete a single role by providing id",
                response_description="Role deleted successfully")
async def delete_role(role_id: int,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Removes a single role from the table by providing id

    """
    print("Calling delete_role method")

    try:
        # Check if record already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_ROLE} WHERE id = {role_id};"
        check_result = await database.execute_query(query=query)

        if not check_result:
            raise Exception("Record does not exist")

        query = f"DELETE FROM {SCHEMA}.{TABLE_ROLE} WHERE id = {role_id};"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)
    
    if not check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code = status.HTTP_204_NO_CONTENT)
