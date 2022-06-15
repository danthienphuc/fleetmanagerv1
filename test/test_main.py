from typing import Generator
import pytest
from fastapi.testclient import TestClient

from ..src.main import app

# Test client for the main app
@pytest.fixture(scope="module")
def Client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


# Test the main app

# Test Connection
@pytest.mark.main
@pytest.mark.refresh_db
def test_add(Client: TestClient) -> None:
    response = Client.get("/")
    assert response.json() == "Connect successfully"


# Test create object

# Test create fleet
@pytest.mark.main
@pytest.mark.create
@pytest.mark.fleet
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
            "Name": name,
            "Description": description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Description": description}


# Test create fleet with no name
@pytest.mark.main
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize("name,description", [(None, "Test Fleet Description 1")])
def test_create_fleet_with_no_name(
    Client: TestClient, name: str, description: str
) -> None:
    response = Client.post(
        "/fleets/",
        json={
            "Name": name,
            "Description": description,
        },
    )
    assert response.status_code == 422

# Test create fleet with same name
@pytest.mark.main
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize(
    "name,description,id",
    [("Test Fleet 1", "Test Fleet Description 1", 1)]
)
def test_create_fleet_with_same_name(Client: TestClient,name: str, description: str, id: int) -> None:
    response = Client.post(
        "/fleets/",
        json={
            "Name": name,
            "Description": description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Description": description}

# Test create vehicle
@pytest.mark.main
@pytest.mark.create
@pytest.mark.vehicle
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
            "Name": name,
            "Description": description,
            "FleetID": fleet_id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "ID": id,
        "Name": name,
        "Description": description,
        "FleetID": fleet_id,
    }


# Test create driver
@pytest.mark.main
@pytest.mark.create
@pytest.mark.driver
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
            "Name": name,
            "Age": age,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Age": age}


# Test create route
@pytest.mark.main
@pytest.mark.create
@pytest.mark.route
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
            "Name": name,
            "Description": description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Description": description}


# Test create route detail
@pytest.mark.main
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            1,
            1,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
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
    temp = {
            "RouteID": route_id,
            "VehicleID": vehicle_id,
            "DriverID": driver_id,
            "StartTime": start_time.replace("Z", "000"),
            "EndTime": end_time.replace("Z", "000"),
            "StartLocation": start_location,
            "EndLocation": end_location,
            "TicketPrice": ticket_price,
        }
    response = Client.post(
        "/routedetails/",
        json= temp,
    )
    assert response.status_code == 200
    assert response.json() == temp


# Test get all objects

# Test get all fleets
def test_get_all_fleets(Client: TestClient) -> None:
    response = Client.get("/fleets/")
    assert response.status_code == 200
    assert response.json() == [
        {"ID": 1, "Name": "Test Fleet 1", "Description": "Test Fleet Description 1"},
        {"ID": 2, "Name": "Test Fleet 2", "Description": "Test Fleet Description 2"},
        {"ID": 3, "Name": "Test Fleet 3", "Description": "Test Fleet Description 3"},
    ]


# Test get all vehicles
def test_get_all_vehicles(Client: TestClient) -> None:
    response = Client.get("/vehicles/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "ID": 1,
            "Name": "Test Vehicle 1",
            "Description": "Test Vehicle Description 1",
            "FleetID": 1,
        },
        {
            "ID": 2,
            "Name": "Test Vehicle 2",
            "Description": "Test Vehicle Description 2",
            "FleetID": 2,
        },
        {
            "ID": 3,
            "Name": "Test Vehicle 3",
            "Description": "Test Vehicle Description 3",
            "FleetID": 3,
        },
    ]


# Test get all drivers
def test_get_all_drivers(Client: TestClient) -> None:
    response = Client.get("/drivers/")
    assert response.status_code == 200
    assert response.json() == [
        {"ID": 1, "Name": "Test Driver 1", "Age": "1980-01-01"},
        {"ID": 2, "Name": "Test Driver 2", "Age": "1980-01-02"},
        {"ID": 3, "Name": "Test Driver 3", "Age": "1980-01-03"},
    ]


# Test get all routes
def test_get_all_routes(Client: TestClient) -> None:
    response = Client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == [
        {"ID": 1, "Name": "Test Route 1", "Description": "Test Route Description 1"},
        {"ID": 2, "Name": "Test Route 2", "Description": "Test Route Description 2"},
        {"ID": 3, "Name": "Test Route 3", "Description": "Test Route Description 3"},
    ]


# Test get all route details
def test_get_all_route_details(Client: TestClient) -> None:
    response = Client.get("/routedetails/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "RouteID": 1,
            "DriverID": 1,
            "VehicleID": 1,
            "StartTime": "2022-06-15T09:51:10.025000",
            "EndTime": "2022-06-15T09:51:10.025000",
            "StartLocation": "Test Start Location 1",
            "EndLocation": "Test End Location 1",
            "TicketPrice": 10,
        },
        {
            "RouteID": 2,
            "DriverID": 2,
            "VehicleID": 2,
            "StartTime": "2022-06-15T09:51:10.025000",
            "EndTime": "2022-06-15T09:51:10.025000",
            "StartLocation": "Test Start Location 2",
            "EndLocation": "Test End Location 2",
            "TicketPrice": 20,
        },
        {
            "RouteID": 3,
            "DriverID": 3,
            "VehicleID": 3,
            "StartTime": "2022-06-15T09:51:10.025000",
            "EndTime": "2022-06-15T09:51:10.025000",
            "StartLocation": "Test Start Location 3",
            "EndLocation": "Test End Location 3",
            "TicketPrice": 30,
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
    assert response.status_code == 200
    assert response.json() == [{"ID": id, "Name": name, "Description": description}]


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
    assert response.status_code == 200
    assert response.json() == [{"ID": id, "Name": name, "Description": description}]


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
    assert response.status_code == 200
    assert response.json() == [
        {"ID": id, "Name": name, "Description": description, "FleetID": fleet_id}
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
    assert response.status_code == 200
    assert response.json() == [
        {"ID": id, "Name": name, "Description": description, "FleetID": fleet_id}
    ]


# Test get routes by name
@pytest.mark.parametrize("vehicle_name,route_name,driver_name", [("e", "e", "e")])
def test_get_routes_by_name(
    Client: TestClient,
    vehicle_name: str,
    route_name: str,
    driver_name: str
) -> None:
    response = Client.get(
        f"/routes/?route_name={vehicle_name}&vehicle_name={route_name}&driver_name={driver_name}"
    )
    assert response.status_code == 200
    assert response.json() == [
        {"ID": 1, "Name": "Test Route 1", "Description": "Test Route Description 1"},
        {"ID": 2, "Name": "Test Route 2", "Description": "Test Route Description 2"},
        {"ID": 3, "Name": "Test Route 3", "Description": "Test Route Description 3"},
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
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Description": description}


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
    assert response.status_code == 200
    assert response.json() == {
        "ID": id,
        "Name": name,
        "Description": description,
        "FleetID": fleet_id,
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
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Age": age}


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
    assert response.status_code == 200
    assert response.json() == {"ID": id, "Name": name, "Description": description}


# Test get route detail by id
@pytest.mark.parametrize(
    "route_id, driver_id, vehicle_id, start_time, end_time, start_location, end_location, ticket_price",
    [
        (
            1,
            1,
            1,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
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
    assert response.status_code == 200
    assert response.json() == {
        "RouteID": route_id,
        "DriverID": driver_id,
        "VehicleID": vehicle_id,
        "StartTime": start_time.replace("Z", "000"),
        "EndTime": end_time.replace("Z", "000"),
        "StartLocation": start_location,
        "EndLocation": end_location,
        "TicketPrice": ticket_price,
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
            "Name": name,
            "Description": description,
        },
    )
    assert response.status_code == 200
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
        json={"Name": name, "Description": description, "FleetID": fleet_id},
    )
    assert response.status_code == 200
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
    response = Client.put(f"/drivers/{id}", json={"Name": name, "Age": age})
    assert response.status_code == 200
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
        f"/routes/{id}", json={"Name": name, "Description": description}
    )
    assert response.status_code == 200
    assert response.json() == "Updated Successfully"


# Test update route detail by id
@pytest.mark.parametrize(
    "route_id, driver_id, vehicle_id, start_time, end_time, start_location, end_location, ticket_price",
    [
        (
            1,
            1,
            1,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2022-06-15T09:51:10.025Z",
            "2022-06-15T09:51:10.025Z",
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
            "DriverID": driver_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "StartLocation": start_location,
            "EndLocation": end_location,
            "TicketPrice": ticket_price,
        },
    )
    assert response.status_code == 200
    assert response.json() == "Updated Successfully"


# Test delete object by id

# Test delete route detail by id
@pytest.mark.parametrize("route_id, vehicle_id", [(1, 1), (2, 2), (3, 3)])
def test_delete_route_detail_by_id(
    Client: TestClient, route_id: int, vehicle_id: int
) -> None:
    response = Client.delete(f"/routedetails/{route_id}/{vehicle_id}")
    assert response.status_code == 200
    assert response.json() == "Deleted Successfully"


# Test delete vehicle by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_vehicle_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/vehicles/{id}")
    assert response.status_code == 200
    assert response.json() == "Deleted Successfully"


# Test delete fleet by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_fleet_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/fleets/{id}")
    assert response.status_code == 200
    assert response.json() == "Deleted Successfully"


# Test delete driver by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_driver_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/drivers/{id}")
    assert response.status_code == 200
    assert response.json() == "Deleted Successfully"


# Test delete route by id
@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_route_by_id(Client: TestClient, id: int) -> None:
    response = Client.delete(f"/routes/{id}")
    assert response.status_code == 200
    assert response.json() == "Deleted Successfully"
