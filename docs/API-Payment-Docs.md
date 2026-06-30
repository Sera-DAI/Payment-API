# API Payment Documentation (API-Payment)

This documentation provides a detailed reference for all endpoints of the **Payment API** (specifically for the Pix payment flow). The API is built using Flask and supports real-time updates via **Socket.IO**.

A Postman collection has been created and is available in the project's root directory: [API-Payment.postman_collection.json](file:///home/jhonny/Git/Payment-API/API-Payment.postman_collection.json).

---

## 🚀 Global Configuration

* **Base URL Variable**: `{{base_url}}` (default set to `http://127.0.0.1:5000`)
* **Global Route Prefix**: `/payment`

---

## 🛣️ HTTP Routes Details

### 1. Create Pix Payment
Creates a new payment transaction in the database with a 30-minute validity, triggers QR Code generation, and returns transaction details.

* **URL**: `{{base_url}}/payment/pix`
* **Method**: `POST`
* **Description**: Initiates a Pix payment flow.
* **Headers**:
  * `Content-Type`: `application/json`
  * `Accept`: `application/json`
* **Request Body**:
  ```json
  {
    "value": 150.75
  }
  ```
  * *Note*: The `value` field must be a positive decimal/float number representing the payment amount.

* **Success Response (200 OK)**:
  ```json
  {
    "Message": "The payment is been created",
    "Payment": {
      "id": 1,
      "value": 150.75,
      "paid": false,
      "bank_payment_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "qr_code": "qr_code_payment_a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "expiration_date": "2026-06-30T17:02:16"
    }
  }
  ```
* **Error Response (400 Bad Request)**:
  * Occurs if the `value` field is missing from the payload.
  ```json
  {
    "Message": "Invalid value"
  }
  ```

---

### 2. Confirm Pix Payment (Webhook / Simulation)
Simulates a payment confirmation webhook coming from an external banking system. It validates the transaction, checks the value, updates the database, and notifies the client in real-time via Socket.IO.

* **URL**: `{{base_url}}/payment/pix/confirmation`
* **Method**: `POST`
* **Description**: Confirms the settlement of a Pix payment.
* **Headers**:
  * `Content-Type`: `application/json`
  * `Accept`: `application/json`
* **Request Body**:
  ```json
  {
    "bank_payment_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "value": 150.75
  }
  ```
  * *Note*: Both fields are required. The `value` field must match the original value registered.

* **Success Response (200 OK)**:
  ```json
  {
    "Message": "Payment is been confirmed."
  }
  ```
* **Error Responses**:
  * **400 Bad Request** (Invalid payload or payment value mismatch):
    ```json
    {
      "Message": "Invalid payment data"
    }
    ```
    or
    ```json
    {
      "Message": "Invalid payment value"
    }
    ```
  * **404 Not Found** (Payment transaction not found in database):
    ```json
    {
      "Message": "paymeny not found."
    }
    ```

---

### 3. Get QR Code Image
Serves the generated PNG image corresponding to the dynamic QR Code of the created Pix payment.

* **URL**: `{{base_url}}/payment/pix/qrcode/<file_name>`
* **Method**: `GET`
* **Description**: Returns the QR Code image file.
* **Path Variables**:
  * `file_name` (String): The file name of the saved QR Code image on the server, without the `.png` extension (obtained from the `qr_code` field in the creation response).
* **Headers**:
  * No special headers are required.
* **Success Response (200 OK)**:
  * Returns the binary image file with a MIME type of `image/png`.

---

### 4. Pix Checkout / Confirmation Page
Renders the payment state. If unpaid, it renders the HTML checkout template where users can scan the QR Code. If paid, it renders the success confirmation template.

* **URL**: `{{base_url}}/payment/pix/<int:payment_id>`
* **Method**: `GET`
* **Description**: Renders the dynamic web page for checkout or success.
* **Path Variables**:
  * `payment_id` (Integer): The ID of the payment transaction in the database (obtained from the `id` field in the creation response).
* **Headers**:
  * `Accept`: `text/html`
* **Success Response (200 OK)**:
  * Returns the rendered HTML:
    * `checkout.html` if the payment is pending (`paid == False`).
    * `confirmed.html` if the payment is confirmed (`paid == True`).

---

## 🔌 Real-Time Communication (Socket.IO)

To update the checkout screen instantly without polling, the API emits WebSocket events.

* **Connection URL**: Base URL (e.g., `http://127.0.0.1:5000`)
* **Event Emitted by Server**: `payment-confirmed-{payment_id}`
* **Expected Client Behavior**:
  * Upon receiving this event, the client should reload the page (`location.reload()`) to render the updated payment status.

---

## 📥 How to Import the Collection in Postman

1. Open **Postman**.
2. Click the **Import** button in the top-left panel.
3. Select the file located at `file:///home/jhonny/Git/Payment-API/API-Payment.postman_collection.json`.
4. A new collection named `API-Payment` will be added to your active workspace.
5. Check the collection's **Variables** tab to adjust `base_url` if you are using a port other than the default (`5000`).
