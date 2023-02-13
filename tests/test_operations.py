# from httpx import AsyncClient
#
#
# async def test_add_specific_operations(ac: AsyncClient):
#     response = await ac.post("/hotels/location", json={
#         "location_hotel" : "алтай"
#     })
#
#     assert response.status_code == 200
#
# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/booking_hotel", params={
#         "room_id": 5,
#         "date_from": "2023-02-12T15:22:01.163Z",
#         "date_to": "2023-02-12T15:22:01.163Z"
#     })
#
#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1
