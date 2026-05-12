import tkinter as tk


def run():
    root = tk.Tk()
    root.title("Airport System")
    root.geometry("550x250")  # Default window size

    # Intro GUI page
    label = tk.Label(root, text="Welcome to the Airport System! Select an activity.")
    label.pack()

    '''List of Buttons for the GUI'''
    # Organize button layout
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Top Row - 3 buttons
    top_frame = tk.Frame(button_frame)
    top_frame.pack()

    # Search Flight Button
    def open_search_flight():
        root.destroy()  # Close the main menu window
        try:
            import search_flight
        except Exception:
            # try relative import when executed as a package
            from . import search_flight
        search_flight.run()  # Open the search flight GUI


    searchflight_button = tk.Button(top_frame, text="Search Flight 🔍✈️", width=18, height=3, command=open_search_flight)
    searchflight_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Search Trip Button
    def open_search_trip():
        root.destroy()
        try:
            import search_trip
        except Exception:
            from . import search_trip
        search_trip.run()

    searchtrip_button = tk.Button(top_frame, text="Search Trip 🔍📍", width=18, height=3, command=open_search_trip)
    searchtrip_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Seat Availability Button
    def open_seat_availability():
        root.destroy()
        try:
            import seat_availiability
        except Exception:
            from . import seat_availiability
        seat_availiability.run()

    seatavailability_button = tk.Button(top_frame, text="Seat Availability 💺", width=18, height=3, command=open_seat_availability)
    seatavailability_button.pack(side=tk.LEFT, padx=5, pady=5)


    """Middle Row"""
    # Middle row frame
    middle_frame = tk.Frame(button_frame)
    middle_frame.pack()

    # Passenger Itinerary Button
    def open_passenger_itinerary():
        root.destroy()
        try:
            import passenger_itinerary
        except Exception:
            from . import passenger_itinerary
        passenger_itinerary.run()

    passengeritinerary_button = tk.Button(middle_frame, text="Passenger Itinerary 👤", width=25, height=3, command=open_passenger_itinerary)
    passengeritinerary_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Aircraft Utilization Report Button
    def open_aircraft_utilization():
        root.destroy()
        try:
            import aircraft_utilization_report
        except Exception:
            from . import aircraft_utilization_report
        aircraft_utilization_report.run()

    aircraftutilizationreport_button = tk.Button(middle_frame, text="Aircraft Utilization Report 📊", width=25, height=3, command=open_aircraft_utilization)
    aircraftutilizationreport_button.pack(side=tk.LEFT, padx=5, pady=5)


    # Exit Button
    exit_button = tk.Button(root, text="Exit 👋", width=18, height=3, command=root.destroy)
    exit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run()