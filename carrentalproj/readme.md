# 🚗 Sona Premium Car Rental System

A full-stack web application for renting cars, built using **Django** and **JavaScript**, with dynamic car listings, real-time pricing, custom admin panel, and integrated **M-Pesa Daraja API** for secure mobile payments.

---

## 📌 Features

- 🏎️ **Car Listing Page**: Dynamic swiper with auto-scrolling and live pricing from backend.
- 🧾 **Checkout System**: Users can select cars, rental duration, and make payments via M-Pesa.
- 💳 **M-Pesa Daraja Integration**: Secure and direct mobile money payments from the frontend.
- 📊 **Custom Admin Panel**: View all rentals, payment status, customer info, and vehicle details.
- 🧮 **Dynamic Calculations**: Subtotal, VAT, discounts, and grand total are automatically computed.
- 📋 **Receipts and Records**: Full transaction and rental records are stored and viewable in a dashboard.

---

## 💻 Technologies Used

| Frontend  | Backend   | Payments  | Database   |
|-----------|-----------|-----------|------------|
| HTML, CSS, JavaScript | Django | M-Pesa Daraja API | SQLite |

---

## 📁 Project Structure

carrentalproj/ │ ├── mainapp/ │ ├── templates/ │ │ ├── cars.html │ │ ├── checkout.html │ │ ├── receipt.html │ │ └── all_rentals.html │ ├── static/ │ │ └── js/ │ │ ├── index.js │ │ └── checkout.js │ ├── models.py │ ├── views.py │ └── urls.py │ ├── carrentalproj/ │ ├── settings.py │ └── urls.py │ ├── manage.py └── README.md

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/whatistech-tec/Final-year-university-project.git
   cd Final-year-university-project

2. Create a virtual environment
    python -m venv env
    source env/bin/activate  # For Linux/macOS
    env\Scripts\activate     # For Windows

3. Install dependencies
    pip install -r requirements.txt

4. Apply migrations
python manage.py makemigrations
python manage.py migrate

5. Run the development server
    python manage.py runserver
    Access the app Visit http://127.0.0.1:8000 in your browser.


## 📲 M-Pesa Daraja API Setup

To enable mobile payments via M-Pesa:

1. Create an account at Safaricom Daraja Portal.

2. Generate Consumer Key and Secret.

3. Add them to your Django settings or .env file:


MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey


## 🧑‍💻 Author
[Hesborn Anyandarua]
Fullstack Developer from Nairobi, Kenya
📧 anyandarhesbon@gmail.com

## 📜 License
This project is licensed under the MIT License.

## 🙌 Contributions
Pull requests and feedback are welcome! If you'd like to contribute:

1. Fork this repo

2. Create a feature branch

3. Submit a PR