# Importing Python packages
import traceback

# Importing FastAPI packages
from fastapi import APIRouter, Response, status, HTTPException, Security
from fastapi_pagination import Page, paginate

# Importing from project files
from api_parameters import SCHEMA, TABLE_LICENSE
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema, LicenseInSchema, LicenseSchema, LicensePatchInSchema, LicensePatchSchema
from internal.funcs import partial_update_query
from internal.Token import get_current_active_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/license',
    tags=["License"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single license in yt_license table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
             summary="Create a single license",
             response_model=LicenseInSchema,
             response_description="License created successfully")
async def create_license(record: LicenseInSchema,
                         current_user: UserSchema = Security(get_current_active_user,
                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Create a license with following information:

        - **license_type**: Type of license. (INT) *--Optional*
        - **license_issue_date**: Issue date of license. (DATETIME) *--Required*
        - **license_expiry_date**: Expiry date of license. (DATETIME) *--Required*

    """
    print("Calling create_license method")

    try:
        date_flag = False
        print(record.license_issue_date, type(record.license_issue_date))

        if record.license_issue_date > record.license_expiry_date:
            date_flag = True
            raise Exception("Issue date is greater than Expiry date")
        
        query = f"""
                    INSERT INTO {SCHEMA}.{TABLE_LICENSE} (license_type, license_issue_date, license_expiry_date)
                    VALUES ({record.license_type}, '{record.license_issue_date}', '{record.license_expiry_date}')
                """
        last_record_id = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if date_flag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Issue date is greater than Expiry date")

    if last_record_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {**record.__dict__}


# Gets a single license from yt_license table based on id
@router.get('/{license_id}/', status_code=status.HTTP_200_OK,
            summary="Get a single license by providing id",
            response_model=LicenseSchema,
            response_description="License fetched successfully")
async def get_license(license_id: int,
                      current_user: UserSchema = Security(get_current_active_user,
                                                          scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get a single license with following information:

        - **id**: Id of license. (INT)
        - **license_type**: Type of license. (INT)
        - **license_issue_date**: Issue date of license. (DATETIME)
        - **license_expiry_date**: Expiry date of license. (DATETIME)
        - **created_at**: Datetime of the license creation. (DATETIME)
        - **updated_at**: Datetime of the license updation. (DATETIME)

    """
    print("Calling get_license method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_LICENSE} WHERE id = {license_id}"
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


# Gets all licenses from yt_license table
@router.get('/', status_code=status.HTTP_200_OK,
            summary="Get all licenses",
            response_model=Page[LicenseSchema],
            response_description="Licenses fetched successfully")
async def get_all_licenses(current_user: UserSchema = Security(get_current_active_user,
                                                               scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Get all licenses with following information:

        - **id**: Id of license. (INT)
        - **license_type**: Type of license. (INT)
        - **license_issue_date**: Issue date of license. (DATETIME)
        - **license_expiry_date**: Expiry date of license. (DATETIME)
        - **created_at**: Datetime of the license creation. (DATETIME)
        - **updated_at**: Datetime of the license updation. (DATETIME)

    """
    print("Calling get_all_licenses method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_LICENSE}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    return paginate(result)


# Updates single license in yt_license table based on id
@router.put('/{license_id}/', status_code=status.HTTP_202_ACCEPTED,
            summary="Update a single license by providing id",
            response_model=LicenseSchema,
            response_description="License updated successfully")
async def update_license(license_id: int, record: LicenseInSchema,
                         current_user: UserSchema = Security(get_current_active_user,
                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Update the following information of the license by providing id:

        - **license_type**: Type of license. (INT) *--Optional*
        - **license_issue_date**: Issue date of license. (DATETIME) *--Required*
        - **license_expiry_date**: Expiry date of license. (DATETIME) *--Required*
        
    """
    print("Calling update_license method")

    try:
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_LICENSE}
                    SET license_type = {record.license_type}, license_issue_date = '{record.license_issue_date}',
                        license_expiry_date = '{record.license_expiry_date}'
                    WHERE id = {license_id}
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

    return {**record.__dict__, "id": license_id}


# Partial updates single license in yt_license table based on id
@router.patch('/{license_id}/', status_code=status.HTTP_202_ACCEPTED,
              summary="Partial update a single license by providing id",
              response_model=LicensePatchSchema,
              response_description="License updated successfully")
async def partial_update_license(license_id: int, record: LicensePatchInSchema,
                                 current_user: UserSchema = Security(get_current_active_user,
                                                                     scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Partial update the following information of the license by providing id:

        - **license_type**: Type of license. (INT) *--Optional*
        - **license_issue_date**: Issue date of license. (DATETIME) *--Optional*
        - **license_expiry_date**: Expiry date of license. (DATETIME) *--Optional*
        
    """
    print("Calling partial_update_license method")

    try:
        query_string = " ".join(map(partial_update_query, record))
        query_string = query_string.strip()[:-1]
        
        query = f"""
                    UPDATE {SCHEMA}.{TABLE_LICENSE}
                    SET {query_string}
                    WHERE id = {license_id}
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

    return {**record.__dict__, "id": license_id}


# Deletes a single license from yt_license table based on id
@router.delete('/{license_id}/', status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a single license by providing id",
               response_description="License deleted successfully")
async def delete_license(license_id: int,
                         current_user: UserSchema = Security(get_current_active_user,
                                                             scopes=[Role.REPORTING_USER['name']])) -> dict:
    """
        Removes a single license from the table by providing id

    """
    print("Calling delete_license method")

    try:
        # Check if record already exists
        query = f"SELECT id FROM {SCHEMA}.{TABLE_LICENSE} WHERE id = {license_id};"
        check_result = await database.execute_query(query=query)

        query = f"DELETE FROM {SCHEMA}.{TABLE_LICENSE} WHERE id = {license_id}"
        result = await database.execute_query(query=query)

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

    if not check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code = status.HTTP_204_NO_CONTENT)
