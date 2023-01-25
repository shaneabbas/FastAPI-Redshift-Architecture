# Importing Python packages
import traceback

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_GROUP
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema, GroupInSchema, GroupSchema, GroupPatchInSchema, GroupPatchSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/group',
    tags=["Group"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single group in yt_group table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single group",
             response_model=GroupInSchema,
             response_description="Group created successfully")
async def create_group(record: GroupInSchema,
                       current_user: UserSchema = Security(get_current_active_user,
                                                           scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a group with following information:
            
        - **group_name**: Name of group. (STR) *--Required*
        - **company_name**: Name of company. (STR) *--Required*
        - **group_description**: Description of group. (STR) *--Optional*
        - **active**: Whether the group is active or not. (BOOL) *--Optional* (Default: False)

    """
    print("Calling create_group method")

    try:
        # Check if group already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_GROUP} WHERE group_name = '{record.group_name}';"
        group_result = await database.execute_query(query=query)

        if group_result:
            raise Exception("Group already exists")

        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_GROUP} (group_name, company_name, group_description, active)
                    VALUES ('{record.group_name}', '{record.company_name}', '{record.group_description}', {record.active})
                """
        last_record_id = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if group_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Group already exists")

    if last_record_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.__dict__}


# Gets a single group from yt_group table based on id
@router.get('/{group_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single group by providing Id",
            response_model=GroupSchema,
            response_description="Group fetched successfully")
async def get_group(group_id: int,
                    current_user: UserSchema = Security(get_current_active_user,
                                                        scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single group with following information:
            
        - **id**: Id of group. (INT)
        - **group_name**: Name of group. (STR)
        - **company_name**: Name of company. (STR)
        - **group_description**: Description of group. (STR)
        - **active**: Whether the group is active or not. (BOOL)
        - **created_at**: Datetime of the group creation. (DATETIME)
        - **updated_at**: Datetime of the group updation. (DATETIME)

    """
    print("Calling get_group method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_GROUP} WHERE id = {group_id}"
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


# Get all groups from yt_group table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all groups",
            response_model=Page[GroupSchema],
            response_description="Groups fetched successfully")
async def get_all_groups(current_user: UserSchema = Security(get_current_active_user,
                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all groups with following information:
        
        - **id**: Id of group. (INT)
        - **group_name**: Name of group. (STR)
        - **company_name**: Name of company. (STR)
        - **group_description**: Description of group. (STR)
        - **active**: Whether the group is active or not. (BOOL)
        - **created_at**: Datetime of the group creation. (DATETIME)
        - **updated_at**: Datetime of the group updation. (DATETIME)

    """
    print("Calling get_all_groups method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_GROUP}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates single group in yt_group table based on id
@router.put('/{group_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update single group by providing Id",
            response_model=GroupSchema,
            response_description="Group updated successfully")
async def update_group(group_id: int, record: GroupInSchema,
                       current_user: UserSchema = Security(get_current_active_user,
                                                           scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the group by providing id:
            
        - **group_name**: Name of group. (STR) *--Required*
        - **company_name**: Name of company. (STR) *--Required*
        - **group_description**: Description of group. (STR) *--Optional*
        - **active**: Whether the group is active or not. (BOOL) *--Optional* (Default: False)

    """
    print("Calling update_group method")

    try:
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_GROUP}
                    SET group_name = '{record.group_name}', company_name = '{record.company_name}',
                        group_description = '{record.group_description}', active = {record.active}
                    WHERE id = {group_id}
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

    return {**record.__dict__, "id": group_id}


# Partial updates single group in yt_group table based on id
@router.patch('/{group_id}/', status_code=status.HTTP_202_ACCEPTED,
                summary="Partial update a single group by providing Id",
                response_model=GroupPatchSchema,
                response_description="Group updated")
async def partial_update_group(group_id: int, record: GroupPatchInSchema,
                               current_user: UserSchema = Security(get_current_active_user,
                                                                   scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the group by providing id:
            
        - **group_name**: Name of group. (STR) *--Optional*
        - **company_name**: Name of company. (STR) *--Optional*
        - **group_description**: Description of group. (STR) *--Optional*
        - **active**: Whether the group is active or not. (BOOL) *--Optional* (Default: False)

    """
    print("Calling partial_update_group method")

    try:
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_GROUP}
                    SET {query_string}
                    WHERE id = {group_id}
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

    return {**record.__dict__, "id": group_id}


# Deletes a single group from yt_group table based on id
@router.delete('/{group_id}/', status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a single group by providing Id",
               response_description="Group deleted successfully")
async def delete_group(group_id: int,
                       current_user: UserSchema = Security(get_current_active_user,
                                                           scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Removes a single group from the table by providing id

    """
    print("Calling delete_group method")

    try:
        # Check if record already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_GROUP} WHERE id = {group_id};"
        check_result = await database.execute_query(query=query)

        query = f"DELETE FROM {SCHEMA}.{TABLE_GROUP} WHERE id = {group_id}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code = status.HTTP_204_NO_CONTENT)
