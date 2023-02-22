from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.api.endpoints.hotels.router import get_hotel_locations

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="app/api/endpoints/templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


# @router.get("/search")
# def search(request: Request):
#     return templates.TemplateResponse("search.html", {"request": request})

@router.get("/search/{location_hotel}")
def get_search_page(request: Request, location=Depends(get_hotel_locations)):
    return templates.TemplateResponse("search.html", {"request": request, "operations": location["data"]})
