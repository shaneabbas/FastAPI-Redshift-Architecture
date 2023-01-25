# Importing Python packages
from environs import Env
from sqlalchemy import (
    Column,
    Integer,
    Float,
    MetaData,
    String,
    Table,
    DateTime,
    ForeignKey,
    Boolean
    )

# Importing from project files
from core.models import db


# ----------------------------------------------------------------------------------------------------


# Reading env variables
env = Env()
env.read_env()
user = env("USER_")
password = env("PASSWORD")
host = env("HOST")
dbname = env("DBNAME")
port = env("PORT")

# Database connection
metadata = MetaData()
database = db.Database(user, password, host, dbname, port)


# Commodity table
Commodity = Table(
        "yt_commodity",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
        Column("commodity_name", String(255), nullable=False),
        Column("active", Boolean, nullable=True, default=False),
        Column("comm_group_id", Integer, ForeignKey("yt_comm_group.id"), nullable=False),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)


# CommodityGroup table
CommodityGroup = Table(
        "yt_comm_group",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
        Column("comm_group_name", String(255), nullable=False),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)


# Group table
Group = Table(
        "yt_group",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
        Column("group_name", String(255), nullable=False), 
        Column("company_name", String(255), nullable=False), 
        Column("group_description", String(255), nullable=True, default=None),
        Column("active", Boolean, nullable=True, default=False),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)


# License table
License = Table(
        "yt_license",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
        Column("license_type", Integer, nullable=True, default=None),
        Column("license_issue_date", DateTime, nullable=False),
        Column("license_expiry_date", DateTime, nullable=False),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)


# Role table
Role = Table(
        "yt_role",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
        Column("role_name", String(255), nullable=False),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)


# User table
User = Table(
        "yt_user",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
        Column("first_name", String(255), nullable=False),
        Column("last_name", String(255), nullable=False),
        Column("contact", String(127), nullable=True, default=None),
        Column("email", String(255), unique=True, nullable=False),
        Column("username", String(255), unique=True, nullable=False),
        Column("password", String(255), nullable=False),
        Column("company_name", String(255), nullable=True, default=None),
        Column("address", String(511), nullable=True, default=None),
        Column("city", String(127), nullable=True, default=None),
        Column("country", String(127), nullable=True, default=None),
        Column("postal_code", String(255), nullable=True, default=None),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)


# UserSystemDescription table
UserSystemDescription = Table(
        "yt_user_system_description",
        metadata,
        Column("user_id", Integer, ForeignKey("yt_user.id"), nullable=False),
        Column("group_id", Integer, ForeignKey("yt_group.id"), nullable=False),
        Column("role_id", Integer, ForeignKey("yt_role.id"), nullable=False),
        Column("license_id", Integer, ForeignKey("yt_license.id"), nullable=False),
        Column("created_at", DateTime),
        Column("updated_at", DateTime)
)
