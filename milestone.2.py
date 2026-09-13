"""
Smart Event Planning Platform
Milestone 2
- attendee registration and ticket generation
- QR-code ticket creation
- attendee check-in
- vendor management and assignment
- event attendance reports
"""

import os
import re
import qrcode


class Event:
    def __init__(self, event_id, name):
        self.id = event_id
        self.name = name
        self.attendees = []
        self.vendors = []


class Attendee:
    def __init__(self, reg_id, name, email, phone, ticket_id):
        self.reg_id = reg_id
        self.name = name
        self.email = email
        self.phone = phone
        self.ticket_id = ticket_id
        self.status = "Registered"


class Vendor:
    def __init__(self, vendor_id, name, service):
        self.id = vendor_id
        self.name = name
        self.service = service


events = [
    Event(1, "AI Workshop"),
    Event(2, "Python Bootcamp"),
]

vendors = []
ticket_number = 1001


def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


def find_vendor(vendor_id):
    for vendor in vendors:
        if vendor.id == vendor_id:
            return vendor
    return None


def get_number(prompt):
    """Read an integer from the user without crashing on bad input."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None


def valid_email(email):
    """ Email validation."""
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def valid_phone(phone):
    """Phone Number Validation."""
    digits = re.sub(r"\D", "", phone)
    return 7 <= len(digits) <= 15


def view_events():
    print("\nEvents")
    print("-" * 35)
    for event in events:
        print(f"{event.id}. {event.name}")


def generate_qr_code(attendee, event):
    folder = "qr_codes"
    os.makedirs(folder, exist_ok=True)

   
    qr_data = (
        f"{attendee.ticket_id}\n"
        f"Registration ID: {attendee.reg_id}\n"
        f"Name: {attendee.name}\n"
        f"Email: {attendee.email}\n"
        f"Event: {event.name}\n"
        f"Event ID: {event.id}"
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    file_path = os.path.join(folder, f"{attendee.ticket_id}.png")
    qr.make_image().save(file_path)
    return file_path


def registration_id_exists(reg_id):
    for event in events:
        for attendee in event.attendees:
            if attendee.reg_id.lower() == reg_id.lower():
                return True
    return False


def register_attendee():
    global ticket_number

    view_events()
    event_id = get_number("\nEnter event ID: ")

    if event_id is None:
        print("Event ID must be a number.")
        return

    event = find_event(event_id)
    if event is None:
        print("Event not found.")
        return

    print("\nAttendee Registration")
    print("-" * 35)

    reg_id = input("Registration ID: ").strip()
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()

    if not all([reg_id, name, email, phone]):
        print("Please fill in every field.")
        return

    if registration_id_exists(reg_id):
        print("That registration ID is already in use.")
        return

    if not valid_email(email):
        print("Please enter a valid email address.")
        return

    if not valid_phone(phone):
        print("Please enter a valid phone number.")
        return

    for attendee in event.attendees:
        if attendee.email.lower() == email.lower():
            print("This email is already registered for this event.")
            return

    ticket_id = f"TKT{ticket_number}"
    attendee = Attendee(reg_id, name, email, phone, ticket_id)

    try:
        qr_path = generate_qr_code(attendee, event)
    except (OSError, ValueError) as error:
        print(f"Could not create the QR code: {error}")
        return

    event.attendees.append(attendee)
    ticket_number += 1

    print("\nRegistration successful!")
    print(f"Name: {attendee.name}")
    print(f"Event: {event.name}")
    print(f"Ticket ID: {attendee.ticket_id}")
    print(f"Status: {attendee.status}")
    print(f"QR code saved to: {qr_path}")


def choose_event():
    view_events()
    event_id = get_number("\nEnter event ID: ")

    if event_id is None:
        print("Event ID must be a number.")
        return None

    event = find_event(event_id)
    if event is None:
        print("Event not found.")
        return None

    return event


def view_attendees():
    event = choose_event()
    if event is None:
        return

    if not event.attendees:
        print("\nNo registrations found for this event.")
        return

    print(f"\nAttendees for {event.name}")
    print("-" * 45)

    for attendee in event.attendees:
        print(f"Registration ID: {attendee.reg_id}")
        print(f"Name: {attendee.name}")
        print(f"Email: {attendee.email}")
        print(f"Phone: {attendee.phone}")
        print(f"Ticket ID: {attendee.ticket_id}")
        print(f"Status: {attendee.status}")
        print("-" * 45)


def check_in_attendee(attendee, event):
    if attendee.status == "Checked In":
        print(f"{attendee.name} is already checked in.")
        return

    attendee.status = "Checked In"
    print("\nCheck-in successful!")
    print(f"Name: {attendee.name}")
    print(f"Event: {event.name}")
    print(f"Ticket: {attendee.ticket_id}")
    print(f"Status: {attendee.status}")


def mark_attendance():
    event = choose_event()
    if event is None:
        return

    if not event.attendees:
        print("No attendees are registered for this event.")
        return

    ticket_id = input("Enter ticket ID: ").strip()
    if not ticket_id:
        print("Ticket ID cannot be empty.")
        return

    for attendee in event.attendees:
        if attendee.ticket_id.lower() == ticket_id.lower():
            check_in_attendee(attendee, event)
            return

    print("Ticket ID not found for this event.")


def find_attendee_by_ticket(ticket_id):
    for event in events:
        for attendee in event.attendees:
            if attendee.ticket_id.lower() == ticket_id.lower():
                return attendee, event
    return None, None


def qr_check_in():
    print("\nQR Code Check-In")
    print("-" * 35)
    print("Scan the QR code or enter the ticket ID.")

    scanned_value = input("Ticket ID / scan: ").strip()
    if not scanned_value:
        print("Ticket ID cannot be empty.")
        return

    
    ticket_id = scanned_value.splitlines()[0].strip()

    attendee, event = find_attendee_by_ticket(ticket_id)

    if attendee is None:
        print("Ticket not found.")
        return

    check_in_attendee(attendee, event)


def add_vendor():
    print("\nAdd Vendor")
    print("-" * 35)

    vendor_id = get_number("Vendor ID: ")
    if vendor_id is None:
        print("Vendor ID must be a number.")
        return

    if find_vendor(vendor_id) is not None:
        print("That vendor ID already exists.")
        return

    name = input("Vendor name: ").strip()
    service = input("Service: ").strip()

    if not name or not service:
        print("Vendor name and service are required.")
        return

    vendors.append(Vendor(vendor_id, name, service))
    print(f"{name} was added successfully.")


def view_vendors():
    if not vendors:
        print("\nNo vendors are available yet.")
        return

    print("\nVendors")
    print("-" * 35)

    for vendor in vendors:
        print(f"{vendor.id}. {vendor.name} - {vendor.service}")


def assign_vendor():
    if not vendors:
        print("\nNo vendors are available. Add a vendor first.")
        return

    event = choose_event()
    if event is None:
        return

    view_vendors()
    vendor_id = get_number("\nEnter vendor ID: ")

    if vendor_id is None:
        print("Vendor ID must be a number.")
        return

    vendor = find_vendor(vendor_id)
    if vendor is None:
        print("Vendor not found.")
        return

    if any(assigned.id == vendor.id for assigned in event.vendors):
        print("This vendor is already assigned to this event.")
        return

    event.vendors.append(vendor)

    print("\nVendor assigned successfully!")
    print(f"Event: {event.name}")
    print(f"Vendor: {vendor.name}")
    print(f"Service: {vendor.service}")


def report():
    print("\nEvent Report")
    print("=" * 45)

    for event in events:
        registrations = len(event.attendees)
        checked_in = sum(
            attendee.status == "Checked In"
            for attendee in event.attendees
        )

        attendance = (
            (checked_in / registrations) * 100
            if registrations
            else 0
        )

        print(f"\nEvent: {event.name}")
        print(f"Event ID: {event.id}")
        print(f"Registrations: {registrations}")
        print(f"Checked in: {checked_in}")
        print(f"Attendance: {attendance:.1f}%")

        print("Assigned vendors:")
        if event.vendors:
            for vendor in event.vendors:
                print(f"  - {vendor.name} ({vendor.service})")
        else:
            print("  None")

        print("-" * 45)


def show_menu():
    print("\n" + "=" * 48)
    print("Smart Event Planning Platform")
    print("=" * 48)
    print("1. Register attendee")
    print("2. View attendees")
    print("3. Mark attendance")
    print("4. QR code check-in")
    print("5. Add vendor")
    print("6. View vendors")
    print("7. Assign vendor")
    print("8. Event report")
    print("9. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_attendee()
        elif choice == "2":
            view_attendees()
        elif choice == "3":
            mark_attendance()
        elif choice == "4":
            qr_check_in()
        elif choice == "5":
            add_vendor()
        elif choice == "6":
            view_vendors()
        elif choice == "7":
            assign_vendor()
        elif choice == "8":
            report()
        elif choice == "9":
            print("\nThanks for using the Smart Event Planning Platform!")
            break
        else:
            print("Please choose a number from 1 to 9.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")

