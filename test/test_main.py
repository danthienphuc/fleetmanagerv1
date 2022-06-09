from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import null

from ..src.main import app

# Test client for the main app
@pytest.fixture(scope="module")
def Client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


# Test the main app

# Test Connection
def test_add(Client: TestClient) -> None:
    response = Client.get("/")
    assert response.json() == "Connect successfully"


# Test create object

# Test create fleet
@pytest.mark.parametrize(
    "name,description,id",
    [
        ("Test Fleet 1", "Test Fleet Description 1", 1),
        ("Test Fleet 2", "Test Fleet Description 2", 2),
        ("Test Fleet 3", "Test Fleet Description 3", 3),
    ],
)
def test_create_fleet(Client: TestClient, name: str, description: str, id: int) -> None:
    response = Client.post(
        "/fleets/",
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"id": id, "name": name, "description": description}


# Test create fleet with no name
@pytest.mark.parametrize("name,description", [(None, "Test Fleet Description 1")])
def test_create_fleet_with_no_name(
    Client: TestClient, name: str, description: str
) -> None:
    response = Client.post(
        "/fleets/",
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed",
            }
        ]
    }


# Test create vehicle
@pytest.mark.parametrize(
    "name,description,fleet_id,id",
    [
        ("Test Vehicle 1", "Test Vehicle Description 1", 1, 1),
        ("Test Vehicle 2", "Test Vehicle Description 2", 2, 2),
        ("Test Vehicle 3", "Test Vehicle Description 3", 3, 3),
    ],
)
def test_create_vehicle(
    Client: TestClient, name: str, description: str, fleet_id: int, id: int
) -> None:
    response = Client.post(
        "/vehicles/",
        json={
            "name": name,
            "description": description,
            "fleet_id": fleet_id,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": id,
        "name": name,
        "description": description,
        "fleet_id": fleet_id,
    }


# Test create driver
@pytest.mark.parametrize(
    "name,age,id",
    [
        ("Test Driver 1", "1980-01-01", 1),
        ("Test Driver 2", "1980-01-02", 2),
        ("Test Driver 3", "1980-01-03", 3),
    ],
)
def test_create_driver(Client: TestClient, name: str, age: int, id: int) -> None:
    response = Client.post(
        "/drivers/",
        json={
            "name": name,
            "age": age,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"id": id, "name": name, "age": age}


# Test create route
@pytest.mark.parametrize(
    "name,description,id",
    [
        ("Test Route 1", "Test Route Description 1", 1),
        ("Test Route 2", "Test Route Description 2", 2),
        ("Test Route 3", "Test Route Description 3", 3),
    ],
)
def test_create_route(Client: TestClient, name: str, description: str, id: int) -> None:
    response = Client.post(
        "/routes/",
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"id": id, "name": name, "description": description}


# Test create route detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 3",
            "Test End Location 3",
            30,
        ),
    ],
)
def test_create_route_detail(
    Client: TestClient,
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
) -> None:
    response = Client.post(
        "/routedetails/",
        json={
            "route_id": route_id,
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "start_time": start_time,
            "end_time": end_time,
            "start_location": start_location,
            "end_location": end_location,
            "ticket_price": ticket_price,
        },
    )
    assert response.status_code == 200, response.text
    start_time = start_time.replace("Z", "")
    end_time = end_time.replace("Z", "")
    assert response.json() == {
        "route_id": route_id,
        "driver_id": driver_id,
        "vehicle_id": vehicle_id,
        "start_time": start_time,
        "end_time": end_time,
        "start_location": start_location,
        "end_location": end_location,
        "ticket_price": ticket_price,
    }


# Test get all objects

# Test get all fleets
def test_get_all_fleets(Client: TestClient) -> None:
    response = Client.get("/fleets/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": 1, "name": "Test Fleet 1", "description": "Test Fleet Description 1"},
        {"id": 2, "name": "Test Fleet 2", "description": "Test Fleet Description 2"},
        {"id": 3, "name": "Test Fleet 3", "description": "Test Fleet Description 3"},
    ]


# Test get all vehicles
def test_get_all_vehicles(Client: TestClient) -> None:
    response = Client.get("/vehicles/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": 1,
            "name": "Test Vehicle 1",
            "description": "Test Vehicle Description 1",
            "fleet_id": 1,
        },
        {
            "id": 2,
            "name": "Test Vehicle 2",
            "description": "Test Vehicle Description 2",
            "fleet_id": 2,
        },
        {
            "id": 3,
            "name": "Test Vehicle 3",
            "description": "Test Vehicle Description 3",
            "fleet_id": 3,
        },
    ]


# Test get all drivers
def test_get_all_drivers(Client: TestClient) -> None:
    response = Client.get("/drivers/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": 1, "name": "Test Driver 1", "age": "1980-01-01"},
        {"id": 2, "name": "Test Driver 2", "age": "1980-01-02"},
        {"id": 3, "name": "Test Driver 3", "age": "1980-01-03"},
    ]


# Test get all routes
def test_get_all_routes(Client: TestClient) -> None:
    response = Client.get("/routes/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": 1, "name": "Test Route 1", "description": "Test Route Description 1"},
        {"id": 2, "name": "Test Route 2", "description": "Test Route Description 2"},
        {"id": 3, "name": "Test Route 3", "description": "Test Route Description 3"},
    ]


# Test get all route details
def test_get_all_route_details(Client: TestClient) -> None:
    response = Client.get("/routedetails/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "route_id": 1,
            "driver_id": 1,
            "vehicle_id": 1,
            "start_time": "2020-01-01T00:00:00",
            "end_time": "2020-01-01T00:00:00",
            "start_location": "Test Start Location 1",
            "end_location": "Test End Location 1",
            "ticket_price": 10,
        },
        {
            "route_id": 2,
            "driver_id": 2,
            "vehicle_id": 2,
            "start_time": "2020-01-01T00:00:00",
            "end_time": "2020-01-01T00:00:00",
            "start_location": "Test Start Location 2",
            "end_location": "Test End Location 2",
            "ticket_price": 20,
        },
        {
            "route_id": 3,
            "driver_id": 3,
            "vehicle_id": 3,
            "start_time": "2020-01-01T00:00:00",
            "end_time": "2020-01-01T00:00:00",
            "start_location": "Test Start Location 3",
            "end_location": "Test End Location 3",
            "ticket_price": 30,
        },
    ]


# Test get object by name

# Test get fleet by name
@pytest.mark.parametrize(
    "key,id,name,description",
    [
        ("Test Fleet 1", 1, "Test Fleet 1", "Test Fleet Description 1"),
        ("Test Fleet 2", 2, "Test Fleet 2", "Test Fleet Description 2"),
        ("Test Fleet 3", 3, "Test Fleet 3", "Test Fleet Description 3"),
    ],
)
def test_get_fleet_by_name(
    Client: TestClient, key: str, id: int, name: str, description: str
) -> None:
    response = Client.get(f"/fleets/?name={key}")
    assert response.status_code == 200, response.text
    assert response.json() == [{"id": id, "name": name, "description": description}]


# Test get fleet by characters in name
@pytest.mark.parametrize(
    "key,id,name,description",
    [
        ("Fleet 1", 1, "Test Fleet 1", "Test Fleet Description 1"),
        ("Fleet 2", 2, "Test Fleet 2", "Test Fleet Description 2"),
        ("Fleet 3", 3, "Test Fleet 3", "Test Fleet Description 3"),
    ],
)
def test_get_fleet_by_characters_in_name(
    Client: TestClient, key: str, id: int, name: str, description: str
) -> None:
    response = Client.get(f"/fleets/?name={key}")
    assert response.status_code == 200, response.text
    assert response.json() == [{"id": id, "name": name, "description": description}]


# Test get vehicle by name
@pytest.mark.parametrize(
    "key,id,name,description,fleet_id",
    [
        ("Test Vehicle 1", 1, "Test Vehicle 1", "Test Vehicle Description 1", 1),
        ("Test Vehicle 2", 2, "Test Vehicle 2", "Test Vehicle Description 2", 2),
        ("Test Vehicle 3", 3, "Test Vehicle 3", "Test Vehicle Description 3", 3),
    ],
)
def test_get_vehicle_by_name(
    Client: TestClient, key: str, id: int, name: str, description: str, fleet_id: int
) -> None:
    response = Client.get(f"/vehicles/?name={key}")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": id, "name": name, "description": description, "fleet_id": fleet_id}
    ]


# Test get vehicle by characters in name
@pytest.mark.parametrize(
    "key,id,name,description,fleet_id",
    [
        ("Vehicle 1", 1, "Test Vehicle 1", "Test Vehicle Description 1", 1),
        ("Vehicle 2", 2, "Test Vehicle 2", "Test Vehicle Description 2", 2),
        ("Vehicle 3", 3, "Test Vehicle 3", "Test Vehicle Description 3", 3),
    ],
)
def test_get_vehicle_by_characters_in_name(
    Client: TestClient, key: str, id: int, name: str, description: str, fleet_id: int
) -> None:
    response = Client.get(f"/vehicles/?name={key}")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": id, "name": name, "description": description, "fleet_id": fleet_id}
    ]


# Test get object by id

# Test get fleet by id
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Fleet 1", "Test Fleet Description 1"),
        (2, "Test Fleet 2", "Test Fleet Description 2"),
        (3, "Test Fleet 3", "Test Fleet Description 3"),
    ],
)
def test_get_fleet_by_id(
    Client: TestClient, id: int, name: str, description: str
) -> None:
    response = Client.get(f"/fleets/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": id, "name": name, "description": description}


# Test get vehicle by id
@pytest.mark.parametrize(
    "id, name, description, fleet_id",
    [
        (1, "Test Vehicle 1", "Test Vehicle Description 1", 1),
        (2, "Test Vehicle 2", "Test Vehicle Description 2", 2),
        (3, "Test Vehicle 3", "Test Vehicle Description 3", 3),
    ],
)
def test_get_vehicle_by_id(
    Client: TestClient, id: int, name: str, description: str, fleet_id: int
) -> None:
    response = Client.get(f"/vehicles/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": id,
        "name": name,
        "description": description,
        "fleet_id": fleet_id,
    }


# Test get driver by id
@pytest.mark.parametrize(
    "id, name, age",
    [
        (1, "Test Driver 1", "1980-01-01"),
        (2, "Test Driver 2", "1980-01-02"),
        (3, "Test Driver 3", "1980-01-03"),
    ],
)
def test_get_driver_by_id(Client: TestClient, id: int, name: str, age: str) -> None:
    response = Client.get(f"/drivers/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": id, "name": name, "age": age}


# Test get route by id
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Route 1", "Test Route Description 1"),
        (2, "Test Route 2", "Test Route Description 2"),
        (3, "Test Route 3", "Test Route Description 3"),
    ],
)
def test_get_route_by_id(
    Client: TestClient, id: int, name: str, description: str
) -> None:
    response = Client.get(f"/routes/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": id, "name": name, "description": description}


# Test get route detail by id
@pytest.mark.parametrize(
    "route_id, driver_id, vehicle_id, start_time, end_time, start_location, end_location, ticket_price",
    [
        (
            1,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 3",
            "Test End Location 3",
            30,
        ),
    ],
)
def test_get_route_detail_by_id(
    Client: TestClient,
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
) -> None:
    response = Client.get(f"/routedetails/{route_id}/{vehicle_id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "route_id": route_id,
        "driver_id": driver_id,
        "vehicle_id": vehicle_id,
        "start_time": start_time,
        "end_time": end_time,
        "start_location": start_location,
        "end_location": end_location,
        "ticket_price": ticket_price,
    }


# Test update object by id

# Test update fleet by id
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Fleet 1", "Test Fleet Description 1"),
        (2, "Test Fleet 2", "Test Fleet Description 2"),
        (3, "Test Fleet 3", "Test Fleet Description 3"),
    ],
)
def test_update_fleet_by_id(
    Client: TestClient, id: int, name: str, description: str
) -> None:
    name = name + " Updated"
    description = description + " Updated"
    response = Client.put(
        f"/fleets/{id}",
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == "Updated Successfully"


# Test update vehicle by id
@pytest.mark.parametrize(
    "id, name, description, fleet_id",
    [
        (1, "Test Vehicle 1", "Test Vehicle Description 1", 1),
        (2, "Test Vehicle 2", "Test Vehicle Description 2", 2),
        (3, "Test Vehicle 3", "Test Vehicle Description 3", 3),
    ],
)
def test_update_vehicle_by_id(
    Client: TestClient, id: int, name: str, description: str, fleet_id: int
) -> None:
    name = name + " Updated"
    description = description + " Updated"
    response = Client.put(
        f"/vehicles/{id}",
        json={"name": name, "description": description, "fleet_id": fleet_id},
    )
    assert response.status_code == 200, response.text
    assert response.json() == "Updated Successfully"


# Test update driver by id
@pytest.mark.parametrize(
    "id, name, age",
    [
        (1, "Test Driver 1", "1980-01-01"),
        (2, "Test Driver 2", "1980-01-02"),
        (3, "Test Driver 3", "1980-01-03"),
    ],
)
def test_update_driver_by_id(Client: TestClient, id: int, name: str, age: str) -> None:
    name = name + " Updated"
    response = Client.put(f"/drivers/{id}", json={"name": name, "age": age})
    assert response.status_code == 200, response.text
    assert response.json() == "Updated Successfully"


# Test update route by id
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Route 1", "Test Route Description 1"),
        (2, "Test Route 2", "Test Route Description 2"),
        (3, "Test Route 3", "Test Route Description 3"),
    ],
)
def test_update_route_by_id(
    Client: TestClient, id: int, name: str, description: str
) -> None:
    name = name + " Updated"
    description = description + " Updated"
    response = Client.put(
        f"/routes/{id}", json={"name": name, "description": description}
    )
    assert response.status_code == 200, response.text
    assert response.json() == "Updated Successfully"


# Test update route detail by id
@pytest.mark.parametrize(
    "route_id, driver_id, vehicle_id, start_time, end_time, start_location, end_location, ticket_price",
    [
        (
            1,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 3",
            "Test End Location 3",
            30,
        ),
    ],
)
def test_update_route_detail_by_id(
    Client: TestClient,
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
) -> None:
    start_time = start_time.replace("Z", "")
    end_time = end_time.replace("Z", "")
    start_location = start_location + " Updated"
    end_location = end_location + " Updated"
    response = Client.put(
        f"/routedetails/{route_id}/{vehicle_id}",
        json={
            "driver_id": driver_id,
            "start_time": start_time,
            "end_time": end_time,
            "start_location": start_location,
            "end_location": end_location,
            "ticket_price": ticket_price,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == "Updated Successfully"


# Test delete object by id

# Test delete route detail by id
@pytest.mark.parametrize("route_id, vehicle_id", [(1, 1), (2, 2), (3, 3)])
def test_delete_route_detail_by_id(
    Client: TestClient, route_id: int, vehicle_id: int
) -> None:
    response = Client.delete(f"/routedetails/{route_id}/{vehicle_id}")
    assert response.status_code == 200, response.text
    assert response.json() == "Deleted Successfully"


# Test delete vehicle by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_vehicle_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/vehicles/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == "Deleted Successfully"


# Test delete fleet by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_fleet_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/fleets/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == "Deleted Successfully"


# Test delete driver by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_driver_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/drivers/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == "Deleted Successfully"


# Test delete route by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_route_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/routes/{id}")
    assert response.status_code == 200, response.text
    assert response.json() == "Deleted Successfully"
