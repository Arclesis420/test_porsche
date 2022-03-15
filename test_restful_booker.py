import requests
from datetime import date as dt
import jsonschema
from jsonschema import validate

base_url = "https://restful-booker.herokuapp.com/"
bookingSchema = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        },
        "lastname": {
            "type": "string"
        },
        "totalprice": {
            "type": "integer"
        },
        "depositpaid": {
            "type": "boolean"
        },
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {
                    "type": "string"
                },
                "checkout": {
                    "type": "string"
                }
            }
        },
        "additionalneeds": {
            "type": "string"
        }
    }
}


def getToken():
    data = {
        "username": "admin",
        "password": "password123"
    }
    return requests.post(f"{base_url}auth", data=data)


token = getToken()


def getAllBookingIds():
    r = requests.get(f"{base_url}booking")
    return r.json()


def getNameBookingIds(fn, ln):
    payload = {
        "firstname": fn,
        "lastname": ln
    }
    r = requests.get(f"{base_url}booking", params=payload)
    return r.json()


def getInOutBookingIds(ci, co):
    payload = {
        "checkin": ci,
        "checkout": co
    }
    r = requests.get(f"{base_url}booking", params=payload)
    return r.json()


def getBookings(bookingArray):
    resp = []
    for elem in bookingArray:
        r = requests.get(f"{base_url}booking/{elem['bookingid']}")
        resp.append(r.json())
    return resp


def createBooking(data):
    try:
        (validate(instance=data, schema=bookingSchema))
    except jsonschema.exceptions.ValidateError as err:
        return f"booking not valid/n{err}"
    return requests.post(f"{base_url}booking", headers={"Content-Type": "application/json"}, json=data)


def updateBooking(data, id):
    try:
        (validate(instance=data, schema=bookingSchema))
    except jsonschema.exceptions.ValidateError as err:
        return f"booking not valid/n{err}"
    return requests.put(f"{base_url}booking/{id}", json=data, auth=f"Basic {getToken()}")


def partialUpdateBooking(data, id):
    try:
        (validate(instance=data, schema=bookingSchema))
    except jsonschema.exceptions.ValidateError as err:
        return f"booking not valid/n{err}"
    return requests.patch(f"{base_url}booking/{id}", headers={"Content-Type": "application/json"}, json=data, auth=f"Basic {getToken()}")


def deleteBooking(id):
    return requests.delete(f"{base_url}booking/{id}", auth=f"Basic {getToken()}")


updatedBooking = {
    "firstname": "Test",
    "lastname": "Test",
    "totalprice": 7280,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2022-11-21",
        "checkout": "2023-01-06"
    },
    "additionalneeds": "Breakfast"
}

newBooking = {
    "firstname": "Testy",
    "lastname": "McTesterson",
    "totalprice": 7280,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2022-11-21",
        "checkout": "2023-05-06"
    },
    "additionalneeds": ""
}


booking = {
    "firstname": "Mary",
    "lastname": "Brown",
    "totalprice": 728,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2017-11-21",
        "checkout": "2021-05-06"
    }
}
# Testing


def test_getToken():
    assert getToken().status_code == 200
    assert getToken().json()["token"] != ''


def test_BookingIds():
    assert getAllBookingIds()
    assert getNameBookingIds("Mary", "Brown")
    assert getInOutBookingIds("2017-11-21", "2021-05-06")


def test_getBookings():
    assert getBookings(getAllBookingIds())
    assert getBookings(getNameBookingIds("Mary", "Brown"))
    assert getBookings(getInOutBookingIds("2017-11-21", "2021-05-06"))


def test_createBooking():
    assert createBooking(newBooking).status_code in [200, 201, 202]
    assert createBooking(newBooking).json()


def test_updateBooking():
    assert updateBooking(updatedBooking, getNameBookingIds("Testy", "McTesterson")[
                         0]["bookingid"]).status_code in [200, 201, 202]
    assert updateBooking(
        updatedBooking, getNameBookingIds("Testy", "McTesterson")[0]["bookingid"])


def test_partialUpdateBooking():
    assert createBooking(newBooking).status_code in [200, 201, 202]
    assert updateBooking(
        updatedBooking, getNameBookingIds("Testy", "McTesterson")[0]["bookingid"])


def test_deleteBooking():
    assert deleteBooking(getNameBookingIds(
        "Testy", "McTesterson")[0]["bookingid"])
