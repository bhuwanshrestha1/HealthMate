# Health-Mate: Appointment Booking System
A web-based platform integrating machine learning for intelligent doctor recommendations and streamlined healthcare appointment booking.

# 🩺 Overview
Health-Mate is a web application designed to bridge the gap between patients and healthcare providers. Powered by the Random Forest Machine Learning algorithm, the system suggests the most appropriate specialist based on user-reported symptoms. It offers seamless appointment booking, electronic health record maintenance, and an intuitive user interface — all developed with the healthcare infrastructure of Nepal in mind.

# 🚀 Key Features
🔍 ML-Powered Specialist Recommendation
Uses symptoms entered by patients to suggest the appropriate specialist using a trained Random Forest Classifier.

📅 Appointment Booking System
Patients can book appointments based on doctor availability and receive confirmations instantly.

📁 Medical Record Management
Stores and retrieves patient appointment history and reports.

👨‍⚕️ Role-Based Access

Patient: Register, log in, get recommendations, and book appointments.

Doctor: View and update appointments, provide reports.

Admin: Manage doctors and oversee system operations.

# 🧠 Machine Learning Model
Algorithm Used: Random Forest Classifier

Dataset: Kaggle - Disease Prediction Dataset by Kaushil268

Model Steps:

Data cleaning and encoding

Training/test split (80/20)

Training on symptoms-disease pairs

Mapping diseases to relevant specialists

Accuracy:

Training Accuracy: 100%

Testing Accuracy: 100%

# 🛠️ Tech Stack
Layer	Technologies
Frontend	HTML, CSS
Backend	Django (Python)
ML Libraries	Scikit-learn, Pandas, NumPy
Database	SQLite (dbSQLite3)
Version Control	Git, GitHub

# 📸 Screenshots
![image](https://github.com/user-attachments/assets/774dd617-f6e6-4051-b0ef-cfe283c32b24)
![image](https://github.com/user-attachments/assets/04a07bb3-af4c-4535-bd77-5c606629c0bd)
![image](https://github.com/user-attachments/assets/10839d0e-0d1a-433c-97a5-6d4c11789535)
![image](https://github.com/user-attachments/assets/39fc4007-2ab8-4c94-9633-92660174babd)
![image](https://github.com/user-attachments/assets/5cc9ee89-8bf2-4052-952a-384d971e7660)
![image](https://github.com/user-attachments/assets/7430bd2f-b8aa-4ffe-a795-15a169e67331)
![image](https://github.com/user-attachments/assets/dd8ef75c-fc4a-4d7e-826f-6e332048be80)
![image](https://github.com/user-attachments/assets/bb5ac5fb-7be6-4a05-8339-63b74525b42f)


# ⚙️ Setup Instructions
Clone the repo
git clone https://github.com/yourusername/health-mate.git
cd health-mate

Create a virtual environment
source venv/bin/activate  # For Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Run database migrations
python manage.py migrate

Start the server
python manage.py runserver

Access the application
Open http://127.0.0.1:8000 in your browser.

# 🌐 Future Enhancements
Location-based doctor filtering

Email/SMS appointment reminders

Integration with hospital systems (e.g., prescription uploads, EHR sharing)

Role-based analytics dashboard
