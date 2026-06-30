# Routes and Modules Mapping

This document serves as a quick reference guide for the directory structure of the **Payment-API** project, along with a detailed mapping of its HTTP endpoints and Socket.IO events.

---

## 1. Module Structure

The project follows a modular structure with a clear separation of concerns. Below is the directory tree of the main workspace, including the test suite:

```
Payment-API/
├── docker-compose.yml       # MySQL database service configuration via Docker
├── requirements.txt         # Python project dependencies (includes pytest)
├── README.md                # Introduction and quickstart guide
├── docs/                    # Detailed system documentation
│   ├── architecture.md      # Architecture, patterns, and data model documentation
│   └── routes_and_modules.md# Endpoints, modules, and events mapping (This file)
├── tests/                   # Automated tests suite (pytest)
│   ├── conftest.py          # Global pytest fixtures (app instance, SQLite memory database)
│   ├── test_routes.py       # Unit and integration tests for HTTP routes
│   └── test_socket.py       # Integration tests for SocketIO events
└── src/                     # Application source code
    ├── run.py               # Entry script to start the API server
    └── app/                 # Main Flask application package
        ├── extensions.py    # Shared Flask extension instances (e.g., SQLAlchemy)
        ├── factory.py       # Application Factory helper (initialization & config)
        ├── models.py        # Database models (entities definition)
        ├── static/          # Static assets (CSS, images, generated QR Codes)
        │   ├── css/
        │   │   └── style.css# Custom styling for the checkout interface
        │   └── img/
        │       └── qrcode/  # Dynamically generated QR Code images
        ├── templates/       # Jinja2 HTML templates
        │   ├── 404.html     # Elegant global page-not-found template
        │   └── payments/
        │       ├── checkout.html  # Checkout page showing payment info (Awaiting payment)
        │       └── confirmed.html # Payment confirmation success page
        ├── payments/        # Payments handling module
        │   ├── events.py    # WebSocket events (Socket.IO)
        │   ├── routes.py    # HTTP routes and controllers
        │   └── schemas.py   # Blueprint definition for payments
        └── strategies/      # Payment processor strategies
            └── pix.py       # Pix payment strategy logic (QR Code generation)
```

### Principal Files Breakdown

*   [run.py](file:///home/jhonny/Git/Payment-API/src/run.py): The entry point of the application. It loads environment variables using `python-dotenv` and starts the combined HTTP + SocketIO server.
*   [extensions.py](file:///home/jhonny/Git/Payment-API/src/app/extensions.py): Instantiates the SQLAlchemy database object `db`, allowing it to be imported across different packages without circular dependency issues.
*   [factory.py](file:///home/jhonny/Git/Payment-API/src/app/factory.py): Contains the factory function `create_app`, which instantiates Flask, reads environment configuration, registers the payments blueprint, registers the global 404 error handler, and automatically runs `db.create_all()` on startup to create database tables.
*   [models.py](file:///home/jhonny/Git/Payment-API/src/app/models.py): Declares the `Payment` model class mapped to the `payments` table in the database.
*   [routes.py](file:///home/jhonny/Git/Payment-API/src/app/payments/routes.py): Defines the route controller actions mapped to the payment blueprint.
*   [events.py](file:///home/jhonny/Git/Payment-API/src/app/payments/events.py): Listens to and manages real-time WebSocket events.
*   [pix.py](file:///home/jhonny/Git/Payment-API/src/app/strategies/pix.py): Implements the `Pix` class strategy to simulate payment creation, returning a unique mock payment ID and generating a QR Code image in the static directory.

---

## 2. HTTP Routes Mapping

The base prefix for all routes defined in this blueprint is `/payment`, configured in [schemas.py](file:///home/jhonny/Git/Payment-API/src/app/payments/schemas.py).

### 2.1. Create Pix Payment
Creates a new payment transaction in the database with a 30-minute validity, triggers QR Code generation, and saves the image file to disk.

-   **Endpoint**: `/payment/pix`
-   **Method**: `POST`
-   **Function**: `create_payment_pix`
-   **Required Headers**: `Content-Type: application/json`
-   **Request Body**:
    ```json
    {
      "value": 150.75
    }
    ```
-   **Success Response (200 OK)**:
    ```json
    {
      "Message": "The payment is been created",
      "Payment": {
        "id": 1,
        "value": 150.75,
        "paid": false,
        "bank_payment_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "qr_code": "qr_code_payment_a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "expiration_date": "2026-06-30T00:21:16"
      }
    }
    ```
-   **Error Responses**:
    -   **400 Bad Request**: If the `value` field is missing from the request payload.
        ```json
        {
          "Message": "Invalid value"
        }
        ```

### 2.2. Confirm Pix Payment
Simulates a payment confirmation webhook coming from the external banking system. It validates the payment transaction, checks the value, updates the database, and triggers real-time WebSocket notification.

-   **Endpoint**: `/payment/pix/confirmation`
-   **Method**: `POST`
-   **Function**: `pix_confirmation`
-   **Required Headers**: `Content-Type: application/json`
-   **Request Body**:
    ```json
    {
      "bank_payment_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "value": 150.75
    }
    ```
-   **Success Response (200 OK)**:
    ```json
    {
      "Message": "Payment is been confirmed."
    }
    ```
-   **Error Responses**:
    -   **400 Bad Request**: Missing fields in payload or payment value mismatch.
    -   **404 Not Found**: Payment transaction not found in database.

### 2.3. Get QR Code Image
Serves the generated QR Code image file for a given payment.

-   **Endpoint**: `/payment/pix/qrcode/<file_name>`
-   **Method**: `GET`
-   **Function**: `get_image`
-   **URL Parameters**:
    -   `file_name` (String): The file name of the saved QR Code image without the `.png` extension.
-   **Success Response (200 OK)**: Returns the raw image data (`image/png`).

### 2.4. Pix Checkout / Confirmation Page
Renders the payment state. If the payment is not completed (`paid = False`), it renders the HTML checkout template where users can scan the QR Code. If it is already completed (`paid = True`), it renders the success confirmation template.

-   **Endpoint**: `/payment/pix/<int:payment_id>`
-   **Method**: `GET`
-   **Function**: `payment_pix_page`
-   **URL Parameters**:
    -   `payment_id` (Integer): The ID of the payment transaction in the database.
-   **Success Response (200 OK)**:
    -   Renders the [checkout.html](file:///home/jhonny/Git/Payment-API/src/app/templates/payments/checkout.html) template (if unpaid).
    -   Renders the [confirmed.html](file:///home/jhonny/Git/Payment-API/src/app/templates/payments/confirmed.html) template (if paid).

---

## 3. Socket.IO Events and Protocols

Real-time notification features utilize the WebSocket protocol to maintain persistent connections.

-   **SocketIO Instance**: `socketio` (configured in [factory.py](file:///home/jhonny/Git/Payment-API/src/app/factory.py))
-   **Connection URL**: Base URL of the API (e.g., `http://127.0.0.1:5000`)
-   **Handled Events**:
    -   **`connect`** (Server-side listener): Triggered when a client connects. Prints `"Client is connected"` to the server log.
    -   **`payment-confirmed-{payment_id}`** (Client-side listener): Emitted from the server upon payment confirmation. When received on the client side, it triggers a page reload (`location.reload()`), causing the `/payment/pix/<payment_id>` endpoint to render the success confirmation page.
