import sqlite3

conn = sqlite3.connect("airport.db")
cursor = conn.cursor()

def search_flight():
    flight_no = input("Enter flight number: ")
    cursor.execute("SELECT * FROM FLIGHT WHERE Number=?", (flight_no,))
    result = cursor.fetchall()
    print("\nFlight Info:")
    for row in result:
        print(row)

def search_trip():
    src = input("From airport: ")
    dest = input("To airport: ")

    print("\nDirect Flights:")
    cursor.execute("""
        SELECT * FROM FLIGHT_LEG 
        WHERE Departure_airport=? AND Arrival_airport=?
    """, (src, dest))
    for row in cursor.fetchall():
        print(row)

    print("\nConnecting Flights:")
    cursor.execute("""
        SELECT f1.Flight_no, f1.Departure_airport, f1.Arrival_airport,
               f2.Arrival_airport
        FROM FLIGHT_LEG f1, FLIGHT_LEG f2
        WHERE f1.Arrival_airport = f2.Departure_airport
        AND f1.Departure_airport=? AND f2.Arrival_airport=?
    """, (src, dest))
    for row in cursor.fetchall():
        print(row)

def seat_availability():
    flight_no = input("Flight number: ")
    date = input("Date (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT Available_seats FROM LEG_INSTANCE
        WHERE Flight_no=? AND Date=?
    """, (flight_no, date))

    result = cursor.fetchone()
    if result:
        print("Available seats:", result[0])
    else:
        print("No data found")

def passenger_itinerary():
    name = input("Passenger name: ")

    cursor.execute("""
        SELECT * FROM SEAT WHERE Customer_name=?
    """, (name,))

    print("\nPassenger Flights:")
    for row in cursor.fetchall():
        print(row)

def aircraft_utilization_report():
    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT 
            a.Registration_number,
            a.Aircraft_type,
            COUNT(li.Flight_no) as Total_Flights
        FROM AIRCRAFT a
        LEFT JOIN LEG_INSTANCE li ON a.Registration_number = li.Registration_number
        WHERE li.Date BETWEEN ? AND ?
        GROUP BY a.Registration_number, a.Aircraft_type
        ORDER BY Total_Flights DESC
    """, (start_date, end_date))

    print(f"\n{'Registration #':<20} {'Aircraft Type':<20} {'Total Flights':<15}")
    print("-" * 55)
    
    results = cursor.fetchall()
    if results:
        for row in results:
            reg_num, aircraft_type, total_flights = row
            print(f"{reg_num:<20} {aircraft_type:<20} {total_flights:<15}")
    else:
        print("No data found for the specified period.")

while True:
    print("\nAirport System")
    print("1. Search Flight")
    print("2. Search Trip")
    print("3. Seat Availability")
    print("4. Passenger Itinerary")
    print("5. Aircraft Utilization Report")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        search_flight()
    elif choice == "2":
        search_trip()
    elif choice == "3":
        seat_availability()
    elif choice == "4":
        passenger_itinerary()
    elif choice == "5":
        aircraft_utilization_report()
    elif choice == "6":
        break

conn.close()