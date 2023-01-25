# Importing Python packages
from environs import Env
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import ValidationError

# Importing FastAPI packages
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

# Importing from project files
from api_parameters import ACCESS_TOKEN_EXPIRE_MINUTES , SCHEMA, TABLE_ROLE, TABLE_USER, TABLE_USER_SYSTEM_DESCRIPTION
from core.models.database import database
from core.schemas.schemas import TokenData, UserSchema
from core.scopes.set_scope import Role


# ---------------------------------------------------------------------------------------------------


env = Env()
env.read_env()
SECRET_KEY = env("SECRET_KEY")
ALGORITHM = env("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, token_type: str):
    to_encode = data.copy()
    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def assign_scopes(scopes):
    if Role.SUPER_ADMIN['name'] in scopes:
        scopes = [Role.SUPER_ADMIN['name'], Role.ADMIN['name'], Role.MANAGER['name'], Role.USER['name'], Role.REPORTING_USER['name']]
    elif Role.ADMIN['name'] in scopes:
        scopes = [Role.ADMIN['name'], Role.MANAGER['name'], Role.USER['name'], Role.REPORTING_USER['name']]
    elif Role.MANAGER['name'] in scopes:
        scopes = [Role.MANAGER['name'], Role.USER['name'], Role.REPORTING_USER['name']]
    elif Role.USER['name'] in scopes:
        scopes = [Role.USER['name'], Role.REPORTING_USER['name']]
    elif Role.REPORTING_USER['name'] in scopes:
        scopes = [Role.REPORTING_USER['name']]
    return scopes


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Brearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        userid: str = payload.get("id")
        if username is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    query = f"""SELECT {SCHEMA}.{TABLE_USER}.*, {SCHEMA}.{TABLE_ROLE}.role_name, {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}.*
                FROM {SCHEMA}.{TABLE_USER}
                JOIN {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}
                    ON {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}.user_id = {SCHEMA}.{TABLE_USER}.id
                JOIN {SCHEMA}.{TABLE_ROLE}
                    ON {SCHEMA}.{TABLE_USER_SYSTEM_DESCRIPTION}.role_id = {SCHEMA}.{TABLE_ROLE}.id
                WHERE user_id = {userid};
            """
    
    query_result = await database.execute_query(query=query)

    if not query_result:
        raise credentials_exception

    token_scopes = [str(query_result[0]['role_name']).upper()]
    token_scopes = assign_scopes(token_scopes)
    token_data = TokenData(scopes=token_scopes, name=username)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return {**query_result[0], "disabled": False}


async def get_current_active_user(current_user: UserSchema = Security(get_current_user)):
    current_user = UserSchema.parse_obj(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
