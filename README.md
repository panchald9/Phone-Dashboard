# 📱 Phone Dashboard

A modern web-based dashboard built with **Flask** and **MySQL** to manage mobile phone specifications. It allows users to upload, view, edit, delete, and export phone data including images.

---

## 🚀 Features

- 🔐 **User Authentication** (optional module)
- 🆕 **Add, Edit & Delete** Phone Details
- 🖼️ **Upload & Preview** Images
- 📊 **View Phone List** with all details
- 🔎 **Search and Filter** Phones by brand, model, or specs
- 📂 **Import & Export** to Excel
- 🌐 **REST API** for frontend integration or mobile apps
- 💾 **Image Uploads** stored in `static/uploads/`

---

## 🛠️ Tech Stack

| Tech         | Usage                         |
|--------------|-------------------------------|
| Python       | Core language                 |
| Flask        | Backend Web Framework         |
| MySQL        | Relational Database           |
| HTML/CSS/JS  | Frontend UI                   |
| Flask-CORS   | Enable cross-origin requests  |
| Pandas       | Excel/CSV processing          |
| Jinja2       | Templating (for HTML rendering) |
| Bootstrap / Tailwind (optional) | UI styling |

---

## 📂 Folder Structure

/phone-dashboard
│
├── app.py # Main Flask application
├── static/
│ └── uploads/ # Uploaded images
├── templates/ # HTML templates (Jinja2)
├── phone_data.xlsx # Sample Excel data
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🧪 API Endpoints

| Method | Endpoint         | Description               |
|--------|------------------|---------------------------|
| GET    | `/phones`        | Retrieve all phones       |
| POST   | `/upload`        | Add a new phone           |
| PUT    | `/phones/<id>`   | Update phone by ID        |
| DELETE | `/phones/<id>`   | Delete phone by ID        |
| POST   | `/import`        | Import phones from Excel  |
| GET    | `/export`        | Export phones to Excel    |

---

## 📸 Screenshot

![image](https://github.com/user-attachments/assets/db6698e1-b05a-4fad-92e4-a580460aa349)


---

## 📝 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/phone-dashboard.git
cd phone-dashboard
2. Create Virtual Environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies

pip install -r requirements.txt
4. Configure Database
Make sure MySQL is installed and running.

Create a database named phones_db.

Use the following SQL to create the table:

CREATE TABLE phones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(100),	
    ram VARCHAR(20),
    storage VARCHAR(20),
    camera VARCHAR(100),
    battery VARCHAR(50),
    price DECIMAL(10,2),
    image TEXT(1000)
);
Update your database credentials in app.py:

app.config['MYSQL_USER'] = 'yourusername'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'phones_db'
5. Run the Flask App

python app.py
Visit http://127.0.0.1:5000 in your browser.

📦 Sample Excel Format
A sample phone_data.xlsx is included with the following columns:

ID | Brand | Model | RAM | Storage | Camera | Battery | Price | Image (URL or filename)
Use it for importing initial data or testing.

💡 Contribution
Want to contribute or enhance features? Follow these steps:

Fork the repository

Create a new branch (git checkout -b feature-branch)

Commit your changes

Push to the branch (git push origin feature-branch)

Open a pull request

📩 Contact
Created with ❤️ by Dhruv Panchal – Founder of PanchalCodeLab

📧 Email: dp148026@gmail.com
🌐 GitHub: @panchald9
