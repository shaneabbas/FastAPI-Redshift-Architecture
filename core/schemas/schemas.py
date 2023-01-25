# Importing Python packages
import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Union


# ----------------------------------------------------------------------------------------------------


# Token Schema
class TokenData(BaseModel):
    name: Optional[str] = None
    scopes: List[str] = []


# Commodity schemas
class CommodityInSchema(BaseModel):
    commodity_name: str
    active: Union[bool, None] = False
    comm_group_id: int


class CommoditySchema(CommodityInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class CommodityPatchInSchema(BaseModel):
    commodity_name: Union[str, None] = None
    active: Union[bool, None] = False
    comm_group_id: Union[int, None] = None


class CommodityPatchSchema(CommodityPatchInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


# CommodityGroup schemas
class CommodityGroupInSchema(BaseModel):
    comm_group_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z0-9_]+$")


class CommodityGroupSchema(BaseModel):
    id: int
    comm_group_name: str
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class CommodityGroupPatchInSchema(BaseModel):
    comm_group_name: Union[str, None] = None


class CommodityGroupPatchSchema(CommodityGroupPatchInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


# Group schemas
class GroupInSchema(BaseModel):
    group_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z0-9_]+$")
    company_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z0-9_]+$")
    group_description: Union[str, None] = None
    active: Union[bool, None] = False


class GroupSchema(BaseModel):
    id: int
    group_name: str
    company_name: str
    group_description: Union[str, None] = None
    active: Union[bool, None] = False
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class GroupPatchInSchema(BaseModel):
    company_name: Union[str, None] = None
    group_description: Union[str, None] = None
    active: Union[bool, None] = False


class GroupPatchSchema(GroupPatchInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


# License schemas
class LicenseInSchema(BaseModel):
    license_type: Union[int, None] = None
    license_issue_date: datetime.datetime
    license_expiry_date: datetime.datetime


class LicenseSchema(LicenseInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class LicensePatchInSchema(BaseModel):
    license_type: Union[int, None] = None
    license_issue_date: Union[datetime.datetime, None] = None
    license_expiry_date: Union[datetime.datetime, None] = None


class LicensePatchSchema(LicensePatchInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


# Role schemas
class RoleInSchema(BaseModel):
    role_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z0-9_.]+$")


class RoleSchema(BaseModel):
    id: int
    role_name: str
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class RolePatchInSchema(BaseModel):
    role_name: Union[str, None] = None


class RolePatchSchema(RolePatchInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


# User Schemas
class UserInSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z]+$")
    last_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z]+$")
    contact: Union[str, None] = None  # Add regex
    email: str = Field(min_length=1, max_length=50,
                       regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9_.]+$")
    username: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z0-9_.]+$")
    password: str
    company_name: Union[str, None] = None  # max length = 30
    address: Union[str, None] = None  # max length = 60
    city: Union[str, None] = None  # max length = 30
    country: Union[str, None] = None  # max length = 30
    postal_code: Union[str, None] = None  # max length = 6
    group_id: int
    role_id: int
    license_id: int


class UserOutSchema(BaseModel):
    first_name: str
    last_name: str
    contact: Union[str, None] = None
    email: str
    username: str
    company_name: Union[str, None] = None
    address: Union[str, None] = None
    city: Union[str, None] = None
    country: Union[str, None] = None
    postal_code: Union[str, None] = None
    group_id: int
    role_id: int
    license_id: int


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact: Union[str, None] = None
    email: str
    username: str
    company_name: Union[str, None] = None
    address: Union[str, None] = None
    city: Union[str, None] = None
    country: Union[str, None] = None
    postal_code: Union[str, None] = None
    group_id: int
    role_id: int
    license_id: int
    disabled: Union[bool, None] = False
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class UserPutInSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z]+$")
    last_name: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z]+$")
    contact: Union[str, None] = None  # Add regex
    email: str = Field(min_length=1, max_length=50,
                       regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    username: str = Field(min_length=1, max_length=50, regex="^[a-zA-Z0-9_]+$")
    company_name: Union[str, None] = None  # max length = 30
    address: Union[str, None] = None  # max length = 60
    city: Union[str, None] = None  # max length = 30
    country: Union[str, None] = None  # max length = 30
    postal_code: Union[str, None] = None  # max length = 6
    group_id: int
    role_id: int
    license_id: int


class UserPatchInSchema(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    contact: Union[str, None] = None
    email: Union[str, None] = None
    username: Union[str, None] = None
    company_name: Union[str, None] = None
    address: Union[str, None] = None
    city: Union[str, None] = None
    country: Union[str, None] = None
    postal_code: Union[str, None] = None
    group_id: Union[int, None] = None
    role_id: Union[int, None] = None
    license_id: Union[int, None] = None


class UserPatchSchema(UserPatchInSchema):
    id: int
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


# UserSystemDescription schemas
class UserSystemDescriptionInSchema(BaseModel):
    user_id: int
    group_id: int
    role_id: int
    license_id: int


class UserSystemDescriptionSchema(UserSystemDescriptionInSchema):
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None


class UserSystemDescriptionPatchInSchema(BaseModel):
    user_id: Union[int, None] = None
    group_id: Union[int, None] = None
    role_id: Union[int, None] = None
    license_id: Union[int, None] = None


class UserSystemDescriptionPatchSchema(UserSystemDescriptionPatchInSchema):
    created_at: Union[datetime.datetime, None] = None
    updated_at: Union[datetime.datetime, None] = None
