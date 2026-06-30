# Payment-API

This is a payment processing and checkout API that implements the **Pix** payment method. Built using Python and Flask, the application simulates the complete payment lifecycle, from transaction creation in the database to QR Code generation and real-time status rendering on the checkout page.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed.
- Docker & Docker Compose (optional, to run the MySQL database).

### 1. Setting Up the Environment
Clone the repository, create a virtual environment, and install the dependencies listed in [requirements.txt](file:///home/jhonny/Git/Payment-API/requirements.txt):

```bash
# Create and activate virtual environment (Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the configurations from [.env.example](file:///home/jhonny/Git/Payment-API/.env.example) to a new file named `.env` in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your database credentials and security key. Example:
```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=payment_db
MYSQL_USER=user_payment
MYSQL_PASSWORD=payment_password
DB_HOST=127.0.0.1
SECRET_KEY=your_super_secure_secret_key
```

### 3. Spin up the MySQL Database
Use [docker-compose.yml](file:///home/jhonny/Git/Payment-API/docker-compose.yml) to quickly start the MySQL container:

```bash
docker-compose up -d
```

### 4. Start the Application
Run the main script [run.py](file:///home/jhonny/Git/Payment-API/src/run.py) to launch the development server:

```bash
python src/run.py
```

The Flask server will start on its default port: `http://127.0.0.1:5000/`.  
> *Note: Database tables will be automatically created by SQLAlchemy upon the application's first initialization.*

---

## 🛠️ Technology Stack

- **Microframework**: Flask
- **Database & ORM**: MySQL & Flask-SQLAlchemy
- **Real-Time Communication**: Flask-SocketIO (WebSockets)
- **QR Code Generation**: qrcode (Pillow)

---

## 📂 Detailed Documentation

For a deeper understanding of the system's design and features, refer to the files in the `docs/` folder:

1. 🏛️ **[System Architecture](file:///home/jhonny/Git/Payment-API/docs/architecture.md)**
   - Overview of Design Patterns (Application Factory, Strategy, Blueprints).
   - Sequence diagram illustrating the payment generation flow.
   - Database model definition and schemas.