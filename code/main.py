from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, admin, farmcrop, user, analize
from config import setting

app = FastAPI(
    title="MMC Crop-Type APIs ",
    docs_url="/",
    description="Product by Map My Crop",
    version="0.0.1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Crop-Type Detection",
        version="0.0.1",
        description="Map My Crop's Crop-Type API",
        routes=app.routes,
        servers=[{"url": setting.SERVER}] if setting.SERVER != "" else [],
    )
    openapi_schema["info"]["x-logo"] = {"url": setting.LOGO}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# routes
app.include_router(auth.route)
app.include_router(admin.route)
app.include_router(analize.route)
app.include_router(farmcrop.route)
app.include_router(user.route)
