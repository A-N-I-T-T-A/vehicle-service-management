# Vehicle Service Management System

A custom application built with the Frappe Framework and ERPNext to manage vehicle registrations, service bookings, job cards, technician assignments, and service tasks.

## Features

- **Vehicle Management:** Register vehicles against customers and prevent duplicate registration numbers.
- **Service Booking:** Create bookings with customer, vehicle, date, service type, and status.
- **Job Card Management:** Assign technicians, record multiple service tasks, and calculate estimated service costs.
- **Business Validations:** Prevent past bookings, customer–vehicle mismatches, and conflicting bookings for the same vehicle.
- **Status Management:** Validate booking and Job Card status transitions and update booking status when service progresses or completes.
- **Role-Based Access:** Configure access for Administrator, Service Advisor, and Technician.
- **Technician Assignment Restrictions:** Restrict technicians to Job Cards assigned to their user accounts.
- **REST APIs:** Create service bookings, retrieve booking details, and update booking status.

## Technology Stack

- Frappe Framework
- ERPNext v15
- Python
- MariaDB
- JavaScript
- Postman for API testing

## Installation

From an existing Frappe Bench environment:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench --site $SITE_NAME install-app vehicle_service
bench --site $SITE_NAME migrate
```

Replace `$PATH_TO_YOUR_BENCH`, `$URL_OF_THIS_REPO`, and `$SITE_NAME` with your actual values.

Start the development environment:

```bash
bench start
```

## Application Structure

The application includes the following components:

- `vehicle_service/api.py` — Custom API endpoints and permission helpers.
- `vehicle_service/hooks.py` — Application hooks.
- `vehicle_service/vehicle_service_management/doctype/vehicle/` — Vehicle DocType and validations.
- `vehicle_service/vehicle_service_management/doctype/service_booking/` — Service Booking DocType and validations.
- `vehicle_service/vehicle_service_management/doctype/service_task/` — Child DocType for service tasks.
- `vehicle_service/vehicle_service_management/doctype/vehicle_service_job_card/` — Job Card DocType and lifecycle logic.

## Roles and Permissions

| Role | Responsibilities |
|---|---|
| Administrator | Full system administration |
| Service Advisor | Manage vehicles, bookings, and job cards |
| Technician | Access assigned Job Cards and update service tasks |

Standard DocType permissions and custom assignment-based permission checks are used to restrict access.

## API Documentation

Base path:

`/api/method/vehicle_service.api`

### 1. Create a Service Booking

**Method:** `POST`

**Endpoint:** `/api/method/vehicle_service.api.create_service_booking`

Required parameters:

- `customer`
- `vehicle`
- `booking_date`
- `service_type`

Example JSON body:

```json
{
  "customer": "CUSTOMER-ID",
  "vehicle": "VEHICLE-ID",
  "booking_date": "2026-11-15",
  "service_type": "General Service"
}
```

### 2. Retrieve a Service Booking

**Method:** `GET`

**Endpoint:** `/api/method/vehicle_service.api.get_service_booking?name=BOOKING-ID`

Returns the booking name, customer, vehicle, booking date, service type, and status.

### 3. Update Booking Status

**Method:** `POST`

**Endpoint:** `/api/method/vehicle_service.api.update_booking_status`

Example JSON body:

```json
{
  "name": "BOOKING-ID",
  "status": "Confirmed"
}
```

The endpoint validates status transitions and checks the user's permissions.

### API Authentication

Authenticate using a Frappe API key and secret:

```http
Authorization: token API_KEY:API_SECRET
```

Use credentials belonging to the appropriate test user. Never commit API keys, API secrets, passwords, or other credentials to the repository.

## Testing

Verify the application through:

- Frappe Desk forms and list views.
- Vehicle and booking validation tests.
- Booking and Job Card status-transition tests.
- Role-based and technician assignment permission tests.
- Postman tests for successful requests, invalid inputs, missing records, and unauthorized access.

The Postman collection will be provided separately.

## Development and Contribution

This app can use `pre-commit` for code formatting and linting.

```bash
cd apps/vehicle_service
pre-commit install
```

The project template includes configuration for tools such as Ruff, ESLint, Prettier, and pyupgrade. Run the configured checks before submitting changes.

## License

MIT
