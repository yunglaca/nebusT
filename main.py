from fastapi import FastAPI
from routers import routers_buildings, routers_activities, routers_organizations
from middleware.api import APIKeyMiddleware
from db.config import settings
app = FastAPI()

app.add_middleware(APIKeyMiddleware,api_key=settings.api_key)
# Регистрируем роутеры
app.include_router(routers_buildings.router, prefix="/buildings", tags=["Buildings"])
app.include_router(routers_activities.router, prefix="/activities", tags=["Activities"])
app.include_router(routers_organizations.router, prefix="/organizations", tags=["Organizations"])

