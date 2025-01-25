from fastapi import FastAPI
from routers import routers_buildings, routers_activities, routers_organizations

app = FastAPI()


app.include_router(routers_buildings.router, prefix="/buildings", tags=["Buildings"])
app.include_router(routers_activities.router, prefix="/activities", tags=["Activities"])
app.include_router(
    routers_organizations.router, prefix="/organizations", tags=["Organizations"]
)
