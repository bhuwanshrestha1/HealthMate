Health-Mate: Appointment Booking System
A web-based platform integrating machine learning for intelligent doctor recommendations and streamlined healthcare appointment booking.

🩺 Overview
Health-Mate is a web application designed to bridge the gap between patients and healthcare providers. Powered by the Random Forest Machine Learning algorithm, the system suggests the most appropriate specialist based on user-reported symptoms. It offers seamless appointment booking, electronic health record maintenance, and an intuitive user interface — all developed with the healthcare infrastructure of Nepal in mind.

🚀 Key Features
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

🧠 Machine Learning Model
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

🛠️ Tech Stack
Layer	Technologies
Frontend	HTML, CSS
Backend	Django (Python)
ML Libraries	Scikit-learn, Pandas, NumPy
Database	SQLite (dbSQLite3)
Version Control	Git, GitHub

📸 Screenshots
Include screenshots of:

Patient login/registration

ML symptom input and doctor recommendation

Doctor dashboard

Admin panel

(Add images here using markdown once in the repo, e.g., ![Alt text](screenshots/patient_login.png))

⚙️ Setup Instructions
Clone the repo

bash
Copy
Edit
git clone https://github.com/yourusername/health-mate.git
cd health-mate
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run database migrations

bash
Copy
Edit
python manage.py migrate
Start the server

bash
Copy
Edit
python manage.py runserver
Access the application
Open http://127.0.0.1:8000 in your browser.

🌐 Future Enhancements
Location-based doctor filtering

Email/SMS appointment reminders

Integration with hospital systems (e.g., prescription uploads, EHR sharing)

Role-based analytics dashboard
