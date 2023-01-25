# Importing Python packages
import traceback

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_COMMODITY_GROUP
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema, CommodityGroupInSchema, CommodityGroupSchema, CommodityGroupPatchInSchema, \
    CommodityGroupPatchSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/commodity_group',
    tags=["Commodity Group"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single commodity group in yt_comm_group table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single commodity group",
             response_model=CommodityGroupInSchema,
             response_description="Commodity Group created successfully")
async def create_commodity_group(record: CommodityGroupInSchema,
                                 current_user: UserSchema = Security(get_current_active_user,
                                                                     scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a commodity group with following information:

        - **comm_group_name**: Name of commodity group. (STR) *--Required*

    """
    print("Calling create_commodity_group method")

    try:
        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_COMMODITY_GROUP} (comm_group_name)
                    VALUES ('{record.comm_group_name}')
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

    return {**record.__dict__}


# Gets a single commodity group from yt_comm_group table based on id
@router.get('/{commodity_group_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single commodity group by providing Id",
            response_model=CommodityGroupSchema,
            response_description="Commodity Group fetched successfully")
async def get_commodity_group(commodity_group_id: int,
                              current_user: UserSchema = Security(get_current_active_user,
                                                                  scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single commodity group with following information:

        - **id**: Id of the commodity group. (INT)
        - **comm_group_name**: Name of commodity group. (STR)
        - **created_at**: Datetime of the commodity group creation. (DATETIME)
        - **updated_at**: Datetime of the commodity group updation. (DATETIME)

    """
    print("Calling get_commodity_group method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_COMMODITY_GROUP} WHERE id = {commodity_group_id}"
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


# Get all commodity groups from yt_comm_group table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all commodity groups",
            response_model=Page[CommodityGroupSchema],
            response_description="Commodity Groups fetched successfully")
async def get_all_commodity_groups(current_user: UserSchema = Security(get_current_active_user,
                                                                       scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all commodity groups with following information:

        - **id**: Id of the commodity group. (INT)
        - **comm_group_name**: Name of commodity group. (STR)
        - **created_at**: Datetime of the commodity group creation. (DATETIME)
        - **updated_at**: Datetime of the commodity group updation. (DATETIME)

    """
    print("Calling get_all_commodity_groups method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_COMMODITY_GROUP}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates single commodity group in yt_comm_group table
@router.put('/{commodity_group_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update single commodity group by providing Id",
            response_model=CommodityGroupSchema,
            response_description="Commodity Group updated successfully")
async def update_commodity_group(commodity_group_id: int, record: CommodityGroupInSchema,
                                 current_user: UserSchema = Security(get_current_active_user,
                                                                     scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the commodity group by providing id:

        - **comm_group_name**: Name of commodity group. (STR) *--Required*

    """
    print("Calling update_commodity_group method")

    try:
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_COMMODITY_GROUP}
                    SET comm_group_name = '{record.comm_group_name}'
                    WHERE id = {commodity_group_id}
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

    return {**record.__dict__, "id": commodity_group_id}


# Partial updates single commodity group in yt_comm_group table based on id
@router.patch('/{commodity_group_id}/', status_code=status.HTTP_202_ACCEPTED,
              summary="Partial update a single commodity group by providing Id",
              response_model=CommodityGroupPatchSchema,
              response_description="Commodity Group updated successfully")
async def partial_update_commodity_group(commodity_group_id: int, record: CommodityGroupPatchInSchema,
                                         current_user: UserSchema = Security(get_current_active_user,
                                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the commodity group by providing id:

        - **comm_group_name**: Name of commodity group. (STR) *--Optional*

    """
    print("Calling partial_update_commodity_group method")

    try:
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_COMMODITY_GROUP}
                    SET {query_string}
                    WHERE id = {commodity_group_id}
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

    return {**record.__dict__, "id": commodity_group_id}


# Deletes a single commodity group from yt_comm_group table
@router.delete('/{commodity_group_id}/', status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a single commodity group by providing Id",
               response_description="Commodity Group deleted successfully")
async def delete_commodity_group(commodity_group_id: int,
                                 current_user: UserSchema = Security(get_current_active_user,
                                                                     scopes=[Role.REPORTING_USER['name']])) -> None:
    """
        Removes a single commodity group from the table by providing id

    """
    print("Calling delete_commodity method")

    try:
        # Check if record already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_COMMODITY_GROUP} WHERE id = {commodity_group_id};"
        check_result = await database.execute_query(query=query)

        query = f"DELETE FROM {SCHEMA}.{TABLE_COMMODITY_GROUP} WHERE id = {commodity_group_id}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code = status.HTTP_204_NO_CONTENT)
