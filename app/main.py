from fastapi import FastAPI

#from app.api.endpoints.auth.router import router as auth_operation

#from app.api.endpoints.auth.router import router as auth_user
from app.api.endpoints.hotels.router import router
from app.api.endpoints.bookings.router import router_booking


app = FastAPI(
    title="Trading App"
)


app.include_router(router)
app.include_router(router_booking)



