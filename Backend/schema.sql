CREATE TABLE AIRPORT (
    Airport_code TEXT PRIMARY KEY,
    City TEXT,
    State TEXT,
    Name TEXT
);

CREATE TABLE FLIGHT (
    Number TEXT PRIMARY KEY,
    Airline TEXT,
    Weekdays TEXT
);

CREATE TABLE FLIGHT_LEG (
    Flight_no TEXT,
    Leg_no INTEGER,
    Departure_airport TEXT,
    Arrival_airport TEXT,
    Dep_time TEXT,
    Arr_time TEXT
);

CREATE TABLE AIRPLANE_TYPE (
    Type_name TEXT PRIMARY KEY,
    Total_seats INTEGER
);

CREATE TABLE AIRPLANE (
    Airplane_id INTEGER PRIMARY KEY,
    Type_name TEXT
);

CREATE TABLE LEG_INSTANCE (
    Flight_no TEXT,
    Date TEXT,
    Leg_no INTEGER,
    Airplane_id INTEGER,
    Available_seats INTEGER
);

CREATE TABLE SEAT (
    Seat_no TEXT,
    Flight_no TEXT,
    Date TEXT,
    Leg_no INTEGER,
    Customer_name TEXT,
    Phone TEXT
);