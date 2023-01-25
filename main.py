# Importing Python packages
from environs import Env
import logging

# Importing FastAPI packages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_pagination import add_pagination
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

# Importing from project files
from core.models.database import database
from routers import route


# Router Object to Create Routes
app = FastAPI(
    docs_url=None, redoc_url=None,
    title="Tradex APIs",
    description="Tradex API Documentation",
    version="0.1a",
)


# ---------------------------------------------------------------------------------------------------


logger = logging.getLogger('foo-logger')

app.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

env = Env()
env.read_env()
cors_origin_all = env("CORS_ORIGIN_ALL")
allow_methods = env("CORS_ALLOW_METHODS")
allow_headers = env("CORS_ALLOW_HEADERS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin_all],
    allow_credentials=True,
    allow_methods=[allow_methods],
    allow_headers=[allow_headers],
)


@app.on_event("startup")
async def startup():
    await database.connect()
    app.state.db = database
    logger.info("Server Startup")


@app.on_event("shutdown")
async def shutdown():
    if not app.state.db:
        await app.state.db.close()
    logger.info("Server Shutdown")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " ",
        swagger_favicon_url='',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


app.include_router(route.router)


# Adding Pagination
add_pagination(app)
