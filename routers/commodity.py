# Importing Python packages
import traceback

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_COMMODITY
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema, CommodityInSchema, CommoditySchema, CommodityPatchInSchema, CommodityPatchSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/commodity',
    tags=["Commodity"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single commodity in yt_commodity table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single commodity",
             response_model=CommodityInSchema,
             response_description="Commodity created successfully")
async def create_commodity(record: CommodityInSchema,
                           current_user: UserSchema = Security(get_current_active_user,
                                                               scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a commodity with following information:

        - **commodity_name**: Name of commodity. (STR) *--Required*
        - **active**: Whether the commodity is active or not. (BOOL) *--Optional* (Default: False)
        - *group_id**: Foreign key of group table. (INT) *--Required*
    
    """
    print("Calling create_commodity method")

    try:
        # Check if commodity already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_COMMODITY} WHERE commodity_name = '{record.commodity_name}';"
        commodity_result = await database.execute_query(query=query)

        if commodity_result:
            raise Exception("Commodity already exists")

        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_COMMODITY} (commodity_name, active, group_id)
                    VALUES ('{record.commodity_name}', {record.active}, {record.group_id})
                """
        last_record_id = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if commodity_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Commodity already exists")

    if last_record_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.__dict__}


# Gets a single commodity from yt_commodity table based on id
@router.get('/{commodity_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single commodity by providing Id",
            response_model=CommoditySchema,
            response_description="Commodity fetched successfully")
async def get_commodity(commodity_id: int,
                        current_user: UserSchema = Security(get_current_active_user,
                                                            scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single commodity with following information:
        
        - **id**: Id of the commodity. (INT)
        - **commodity_name**: Name of commodity. (STR)
        - **active**: Whether the commodity is active or not. (BOOL)
        - **group_id**: Foreign key of group table. (INT)
        - **created_at**: Datetime of the commodity creation. (DATETIME)
        - **updated_at**: Datetime of the commodity updation. (DATETIME)

    """
    print("Calling get_commodity method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_COMMODITY} WHERE id = '{commodity_id}'"
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


# Get all commodities from yt_commodity table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all commodities",
            response_model=Page[CommoditySchema],
            response_description="Commodities fetched successfully")
async def get_all_commodities(current_user: UserSchema = Security(get_current_active_user,
                                                                  scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all commodities with following information:
            
        - **id**: Id of the commodity. (INT)
        - **commodity_name**: Name of commodity. (STR)
        - **active**: Whether the commodity is active or not. (BOOL)
        - **group_id**: Foreign key of group table. (INT)
        - **created_at**: Datetime of the commodity creation. (DATETIME)
        - **updated_at**: Datetime of the commodity updation. (DATETIME)

    """
    print("Calling get_all_commodities method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_COMMODITY}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates single commodity in yt_commodity table based on id
@router.put('/{commodity_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update single commodity by providing Id",
            response_model=CommoditySchema,
            response_description="Commodity updated successfully")
async def update_commodity(commodity_id: int, record: CommodityInSchema,
                           current_user: UserSchema = Security(get_current_active_user,
                                                               scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the commodity by providing id:

        - **commodity_name**: Name of commodity. (STR) *--Required*
        - **active**: Whether the commodity is active or not. (BOOL) *--Optional* (Default: False)
        - *group_id**: Foreign key of group table. (INT) *--Required*

    """
    print("Calling update_commodity method")

    try:
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_COMMODITY}
                    SET commodity_name = '{record.commodity_name}', active = {record.active}, group_id = {record.group_id}
                    WHERE id = '{commodity_id}'
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

    return {**record.__dict__, "id": commodity_id}


# Partial update single commodity in yt_commodity table based on id
@router.patch('/{commodity_id}/', status_code=status.HTTP_202_ACCEPTED,
              summary="Partial update a single commodity by providing Id",
              response_model=CommodityPatchSchema,
              response_description="Commodity Updated")
async def partial_update_commodity(commodity_id: int, record: CommodityPatchInSchema,
                                   current_user: UserSchema = Security(get_current_active_user,
                                                                       scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the commodity by providing id:

        - **commodity_name**: Name of commodity. (STR) *--Optional*
        - **active**: Whether the commodity is active or not. (BOOL) *--Optional* (Default: False)
        - *group_id**: Foreign key of group table. (INT) *--Optional*

    """
    print("Calling partial_update_commodity method")

    try:
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_COMMODITY}
                    SET {query_string}
                    WHERE id = {commodity_id}
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

    return {**record.__dict__, "id": commodity_id}


# Deletes a single commodity from yt_commodity table based on id
@router.delete('/{commodity_id}/', status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a single commodity by providing Id",
               response_description="Commodity deleted successfully")
async def delete_commodity(commodity_id: int,
                           current_user: UserSchema = Security(get_current_active_user,
                                                               scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Removes a single commodity from the table by providing id

    """
    print("Calling delete_commodity method")

    try:
        # Check if record already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_COMMODITY} WHERE id = {commodity_id};"
        check_result = await database.execute_query(query=query)

        query = f"DELETE FROM {SCHEMA}.{TABLE_COMMODITY} WHERE id = {commodity_id}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code = status.HTTP_204_NO_CONTENT)
