# Vehicle Service Management System

A custom application built with **Frappe Framework and ERPNext v15** to manage vehicle registrations, service bookings, job cards, technician assignments, and service tasks.

## Features

- **Vehicle Management:** Register vehicles and prevent duplicate registration numbers.
- **Service Bookings:** Validate booking dates, customer–vehicle relationships, and conflicting bookings.
- **Job Cards:** Assign technicians, manage service tasks, and calculate estimated costs.
- **Status Management:** Validate booking and job card status transitions.
- **Role-Based Access:** Configure permissions for Administrator, Service Advisor, and Technician.
- **REST APIs:** Create bookings, retrieve booking details, and update booking status.
- **Reports:** View service bookings and job cards with relevant filters.

## Technology Stack

- Frappe Framework
- ERPNext v15
- Python, JavaScript
- MariaDB
- Postman

## Installation

From an existing Frappe Bench environment:

```bash
bench get-app <REPOSITORY_URL> --branch develop
bench --site <SITE_NAME> install-app vehicle_service
bench --site <SITE_NAME> migrate
bench start
```

Replace `<REPOSITORY_URL>` and `<SITE_NAME>` with your repository URL and site name.

## Roles and Permissions

| Role | Access |
|---|---|
| Administrator | Full system administration |
| Service Advisor | Manage vehicles, bookings, and job cards according to permissions |
| Technician | Access assigned job cards and update service tasks |

## API Endpoints

Base path: `/api/method/vehicle_service.api`

### 1. Create Service Booking

**Method:** `POST`

**Endpoint:** `/api/method/vehicle_service.api.create_service_booking`

JSON body:

```json
{
  "customer": "CUSTOMER-ID",
  "vehicle": "VEHICLE-ID",
  "booking_date": "YYYY-MM-DD",
  "service_type": "General Service"
}
```

### 2. Retrieve Service Booking

**Method:** `GET`

**Endpoint:** `/api/method/vehicle_service.api.get_service_booking?name=BOOKING-ID`

Returns booking details, including customer, vehicle, date, service type, and status.

### 3. Update Booking Status

**Method:** `POST`

**Endpoint:** `/api/method/vehicle_service.api.update_booking_status`

JSON body:

```json
{
  "name": "BOOKING-ID",
  "status": "Confirmed"
}
```

### Authentication

Use Frappe API key authentication:

```http
Authorization: token API_KEY:API_SECRET
```

Use credentials belonging to an authorized user. Never commit API secrets or passwords.

## Testing

Run the app's automated tests:

```bash
bench --site <SITE_NAME> run-tests --app vehicle_service
```

Additional verification includes Desk workflows, role-based permissions, and API positive and negative cases using Postman.

**Postman Collection:** Include the corrected collection in the project repository or provide it as a separate assessment attachment.

## License

MIT
