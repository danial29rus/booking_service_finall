from fastapi import Depends

from app.api.endpoints.auth.router import get_current_user


async def test_post_booking_hotel(user = Depends(get_current_user)):
    response = await user.post("/booking_hotel", params={
        "room_id": 5,
        "date_from": "2023-02-12T15:22:01.163Z",
        "date_to": "2023-02-12T15:22:01.163Z"
    })

    assert response.status_code == 200


async def test_rem_book(user = Depends(get_current_user)):
    response = await user.post("/remoove_booking_hotel", json={
        "room_id": "5"})

    assert response.status_code == 200


async def test_my_booking(user = Depends(get_current_user)):
    response = await user.get("/default/my_bookings")

    assert response.status_code == 200
