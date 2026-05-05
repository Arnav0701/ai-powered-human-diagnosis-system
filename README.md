# 🩺 AI-Powered Human Diagnosis System

An advanced, Flask-based healthcare platform that leverages Artificial Intelligence to assist in medical diagnosis. The system allows patients to upload medical scans (like X-rays) for real-time Pneumonia detection and facilitates seamless communication between patients and healthcare professionals.

---

## 📂 Project Directory Structure

```text
AI-Powered-Human-Diagnosis-System/
├── app.py                  # Main Flask application (Routes, Logic, DB Models)
├── model.h5                # Pre-trained CNN Model for Pneumonia Detection
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Custom styling for the application
│   ├── profile_uploads/    # User profile pictures (Patient/Doctor)
│   └── report_uploads/     # Medical scans uploaded by patients
├── templates/              # HTML Templates (Jinja2)
│   ├── login.html          # Authentication page
│   ├── signup.html         # User registration (Doctor/Patient)
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── predict.html        # AI Prediction interface
│   ├── send_consultation.html # Message/Consultation system
│   └── logout.html         # Session termination
└── venv/                   # Virtual Environment (Generated during setup)
```

---

## ✨ Key Features

### 👤 For Patients
- **AI Diagnosis**: Upload X-ray scans for instant Pneumonia detection with confidence scores.
- **Personal Dashboard**: Manage profile details and track previous reports.
- **Direct Consultation**: Send diagnosis reports to specialized doctors for further review.
- **Secure Authentication**: Password-protected accounts with profile verification.

### ⚕️ For Doctors
- **Doctor Dashboard**: Overview of all consultation requests from patients.
- **Expert Reply**: Review patient scans and descriptions to provide professional medical advice.
- **Profile Management**: Maintain professional details, specialization, and about section.

---

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Deep Learning**: TensorFlow / Keras (CNN Model)
- **Database**: MySQL (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, Jinja2
- **Image Processing**: NumPy, OpenCV, Pillow

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- MySQL Server
- Virtualenv (`pip install virtualenv`)

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/AI-Powered-Human-Diagnosis-System.git
cd AI-Powered-Human-Diagnosis-System
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Configuration
1. Open MySQL and create a database:
   ```sql
   CREATE DATABASE diagnosis_system;
   ```
2. Update the database URI in `app.py`:
   ```python
   app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@localhost/diagnosis_system"
   ```

### 6. Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 🧠 AI Model Details
The system uses a **Convolutional Neural Network (CNN)** model trained on Chest X-ray datasets. It classifies images into two categories:
- **Normal**: Healthy lungs.
- **Pneumonia**: Signs of infection detected.

The model expects an input size of `150x150` pixels and provides a confidence score for each prediction.

---
## images
<img width="1235" height="795" alt="Screenshot 2026-04-30 222702" src="https://github.com/user-attachments/assets/b3eaa85e-4e7e-4416-bb30-be4e9e3366d4" />

<img width="1911" height="884" alt="Screenshot 2026-04-30 222950" src="https://github.com/user-attachments/assets/82f5c0d7-3913-4aad-ae5b-98fce59bebb3" />

<img width="1910" height="879" alt="Screenshot 2026-04-30 223024" src="https://github.com/user-attachments/assets/7d74ab10-2ab1-4346-a17b-3cdd19af1857" />

<img width="1861" height="871" alt="Screenshot 2026-04-30 223832" src="https://github.com/user-attachments/assets/43b8d28d-6345-446a-bad2-de50f2677908" />

<img width="1767" height="852" alt="Screenshot 2026-04-30 224004" src="https://github.com/user-attachments/assets/05940c8c-85cf-483e-a35e-e405c53ef715" />

<img width="1807" height="878" alt="Screenshot 2026-04-30 224104" src="https://github.com/user-attachments/assets/e37ea499-300e-4e6b-9ebd-1288dc5f239d" />

<img width="1783" height="883" alt="Screenshot 2026-04-30 224214" src="https://github.com/user-attachments/assets/a9de6790-3d91-4d26-bf22-1780ce25bcc7" />


## 🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request with your suggested changes.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
