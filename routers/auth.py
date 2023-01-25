# Importing Python packages
import traceback
from passlib.hash import pbkdf2_sha256

# Importing FastAPI packages
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# Importing from project files
from core.models.database import database
from internal.Token import create_access_token
from api_parameters import SCHEMA, TABLE_USER


# Router Object to Create Routes
router = APIRouter(
    tags=["Log In"]
)


# ---------------------------------------------------------------------------------------------------


@router.post('/login/', summary="Performs authentication")
async def log_in(request: OAuth2PasswordRequestForm = Depends()):
    """
        Performs authentication and returns the authentication token to keep the user
        logged in for longer time.

        Provide **Username** and **Password** to log in.

    """
    print("Calling log_in method")

    try:
        query = f"SELECT * FROM {SCHEMA}.{TABLE_USER} WHERE username = '{request.username.lower()}';"
        user_result = await database.execute_query(query=query)

        if not user_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        
        if not pbkdf2_sha256.verify(request.password, user_result[0]["password"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Password is incorrect")
        
        access_token = create_access_token(data={"sub": user_result[0]["username"],
                                                 "scopes": request.scopes,
                                                 "id": user_result[0]["id"]},
                                           token_type="access")
        
    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error in authorizing credentials, Please try again")
    
    return {"access_token": access_token, "token_type": "bearer"}
