# ================================
# SMART EVENT PLANNING PLATFORM WITH RESOURCE COORDINATION SYSTEM - Milestone 1
# ================================

class Event:
    def __init__(self, event_id, name, date, time):
        self.id = event_id
        self.name = name
        self.date = date
        self.time = time
        self.venue = "Not Assigned"
        self.resources = {}
        self.status = "Planning"

events = []
venues = []
resources = {}

# ---------------- Utility ----------------

def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

def get_next_id():
    
    if not events:
        return 1
    return max(event.id for event in events) + 1

def venue_is_busy(event, venue, date=None, time=None):
    # checks if a venue is already taken at some date/time
    
    check_date = date if date else event.date
    check_time = time if time else event.time

    for e in events:
        if e.id == event.id:
            continue
        if e.venue == venue and e.date == check_date and e.time == check_time:
            return True
    return False

def update_status(event):
    if event.venue != "Not Assigned" and event.resources:
        event.status = "Confirmed"
    elif event.venue != "Not Assigned":
        event.status = "Venue Booked"
    else:
        event.status = "Planning"

# ---------------- Event ----------------

def create_event():
    print("\n--- Create Event ---")
    name = input("Event Name : ")
    date = input("Date (DD/MM/YYYY): ")
    time = input("Time : ")

    if name == "" or date == "" or time == "":
        print("Event details cannot be empty.")
        return

    event_id = get_next_id()
    events.append(Event(event_id, name, date, time))
    print("Event Created Successfully!")
    print("Your Event ID is:", event_id)

def view_events():
    print("\n--- Event List ---")
    if not events:
        print("No Events Available.")
        return

    for event in events:
        print(f"""
ID      : {event.id}
Name    : {event.name}
Date    : {event.date}
Time    : {event.time}
Venue   : {event.venue}
Status  : {event.status}
-----------------------------""")

def update_event():
    view_events()
    if not events:
        return

    try:
        event_id = int(input("Enter Event ID : "))
    except:
        print("Invalid Input")
        return

    event = find_event(event_id)

    if event is None:
        print("Event Not Found")
        return

    print("Press Enter to keep the current value.")
    new_name = input(f"New Name ({event.name}): ")
    new_date = input(f"New Date ({event.date}): ")
    new_time = input(f"New Time ({event.time}): ")

    if new_date == "":
        new_date = event.date
    if new_time == "":
        new_time = event.time

   
    if event.venue != "Not Assigned":
        if venue_is_busy(event, event.venue, new_date, new_time):
            print("Warning: That date/time clashes with another booking at the same venue.")
            print("Please choose another date or time.")
            return

    if new_name != "":
        event.name = new_name
    event.date = new_date
    event.time = new_time

    update_status(event)
    print("Event Updated Successfully!")

def delete_event():
    view_events()
    if not events:
        return

    try:
        event_id = int(input("Enter Event ID : "))
    except:
        print("Invalid Input")
        return

    event = find_event(event_id)

    if event:
        # give back whatever resources were allocated to this event
        for r, q in event.resources.items():
            resources[r] = resources.get(r, 0) + q

        events.remove(event)
        print("Event Deleted Successfully!")
        print("Allocated resources have been returned.")
    else:
        print("Event Not Found")

# ---------------- Venue ----------------

def add_venue():
    venue = input("Venue Name : ")

    if venue == "":
        print("Venue name cannot be empty.")
        return

    if venue in venues:
        print("Venue Already Exists")
    else:
        venues.append(venue)
        print("Venue Added Successfully!")

def view_venues():
    print("\n--- Venue List ---")

    if not venues:
        print("No Venues Available.")
        return

    for i, venue in enumerate(venues, 1):
        print(i, ".", venue)

def assign_venue():
    view_events()
    if not events:
        return

    try:
        event_id = int(input("Event ID : "))
    except:
        print("Invalid Input")
        return

    event = find_event(event_id)

    if event is None:
        print("Event Not Found")
        return

    view_venues()

    if not venues:
        return

    try:
        choice = int(input("Venue Number : ")) - 1
        venue = venues[choice]
    except:
        print("Invalid Venue")
        return

    if venue_is_busy(event, venue):
        print("Scheduling Conflict! Venue already booked.")
        return

    event.venue = venue
    update_status(event)
    print("Venue Assigned Successfully!")

# ---------------- Resource ----------------

def add_resource():
    name = input("Resource Name : ")

    if name == "":
        print("Resource name cannot be empty.")
        return

    try:
        quantity = int(input("Quantity : "))
    except:
        print("Invalid Quantity")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    resources[name] = resources.get(name, 0) + quantity
    print("Resource Added Successfully!")

def view_resources():
    print("\n--- Resources ---")

    if not resources:
        print("No Resources Available.")
        return

    for name, quantity in resources.items():
        print(f"{name} : {quantity}")

def allocate_resource():
    view_events()

    if not events:
        return

    try:
        event_id = int(input("Event ID : "))
    except:
        print("Invalid Input")
        return

    event = find_event(event_id)

    if event is None:
        print("Event Not Found")
        return

    view_resources()

    if not resources:
        return

    resource = input("Resource Name : ")

    if resource not in resources:
        print("Resource Not Found")
        return

    try:
        quantity = int(input("Required Quantity : "))
    except:
        print("Invalid Quantity")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    if quantity > resources[resource]:
        print("Not Enough Resources")
        return

    resources[resource] -= quantity

    # if this resource was already given to the event before, just add to it
    # instead of making a second separate entry
    event.resources[resource] = event.resources.get(resource, 0) + quantity

    update_status(event)
    print("Resource Allocated Successfully!")

# ---------------- Report ----------------

def event_report():
    print("\n========== EVENT REPORT ==========")

    if not events:
        print("No Events Available.")
        return

    for event in events:
        print(f"""
Event ID : {event.id}
Name     : {event.name}
Date     : {event.date}
Time     : {event.time}
Venue    : {event.venue}
Status   : {event.status}
Resources:""")

        if not event.resources:
            print("  None")
        else:
            for r, q in event.resources.items():
                print(f"  {r} - {q}")

        print("----------------------------------")

# ---------------- Main Menu ----------------

while True:

    print("""
==============================
 SMART EVENT PLANNING PLATFORM WITH RESOURCE COORDINATION SYSTEM- MILESTONE 1
==============================
1. Create Event
2. View Events
3. Update Event
4. Delete Event
5. Add Venue
6. View Venues
7. Assign Venue
8. Add Resource
9. View Resources
10. Allocate Resource
11. Event Report
12. Exit
==============================
""")

    choice = input("Enter Choice : ")

    if choice == "1":
        create_event()

    elif choice == "2":
        view_events()

    elif choice == "3":
        update_event()

    elif choice == "4":
        delete_event()

    elif choice == "5":
        add_venue()

    elif choice == "6":
        view_venues()

    elif choice == "7":
        assign_venue()

    elif choice == "8":
        add_resource()

    elif choice == "9":
        view_resources()

    elif choice == "10":
        allocate_resource()

    elif choice == "11":
        event_report()

    elif choice == "12":
        print("Thank You!")
        break

    else:
        print("Invalid Choice! Please Try Again.")