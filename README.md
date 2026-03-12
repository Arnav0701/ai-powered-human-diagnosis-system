# AI Powered Human Diagnosis System

## Overview

The **AI Powered Human Diagnosis System** is a web-based healthcare assistance platform that uses **Artificial Intelligence and Machine Learning** to help in preliminary medical diagnosis from medical reports and images. The system allows patients to upload medical reports (such as chest X-ray images), receive AI-based predictions, and consult with doctors for further advice.

This project combines **Deep Learning**, **Web Development**, and **Database Management** to create a complete diagnostic workflow that connects patients and doctors in a single platform.

The main goal of this project is to demonstrate how AI can support healthcare professionals by providing **quick preliminary analysis** and assisting in early detection of diseases such as **pneumonia from chest X-ray images**.
<img width="1919" height="1010" alt="Screenshot 2026-03-10 115044" src="https://github.com/user-attachments/assets/85b5d518-f047-450e-8bf3-0f23081e2906" />
<img width="1495" height="882" alt="Screenshot 2026-03-10 114613" src="https://github.com/user-attachments/assets/10b9bf9c-c5f4-4a5d-9789-429b08407101" />
<img width="1397" height="832" alt="Screenshot 2026-03-10 114513" src="https://github.com/user-attachments/assets/bb2c0987-377e-4531-bee2-8c6366a5e26b" />
<img width="914" height="611" alt="Screenshot 2026-03-10 114501" src="https://github.com/user-attachments/assets/218c8fdb-31fd-400a-87c0-065810f7a56d" />
<img width="1919" height="1007" alt="Screenshot 2026-03-10 114448" src="https://github.com/user-attachments/assets/eae8be8f-fb41-40ea-b32f-4fea3e045470" />
<img width="1919" height="1007" alt="Screenshot 2026-03-10 114412" src="https://github.com/user-attachments/assets/dd4460e3-71f7-4759-a6f8-6a2f9c6ff50c" />
<img width="1919" height="995" alt="Screenshot 2026-03-10 114403" src="https://github.com/user-attachments/assets/4d4b3d73-3c42-49c1-a674-6d39eaf5747e" />
<img width="1919" height="1008" alt="Screenshot 2026-03-10 114313" src="https://github.com/user-attachments/assets/c4d0d228-4be0-4e1a-9d5b-a1bc837caab6" />



---

# Key Features

### 1. Patient Registration and Login

* Secure patient authentication system.
* Patients can create accounts and access their personal dashboard.

### 2. Doctor Registration and Login

* Doctors have their own dashboard.
* Doctors can view consultation requests from patients.

### 3. AI Diagnosis System

* Patients can upload chest X-ray images.
* A trained **Convolutional Neural Network (CNN)** predicts whether pneumonia is present.
* The system displays prediction results with confidence score.

### 4. Medical Report Management

* Patients can view their uploaded reports.
* Each report contains:

  * Report ID
  * Date
  * Prediction result
  * Confidence score

### 5. Doctor Consultation System

* Patients can send consultation requests to doctors.
* Doctors can review reports and send medical advice.

### 6. Profile Management

* Both patients and doctors can upload profile images.
* Personal details are displayed in the dashboard.

### 7. Dashboard Interface

Separate dashboards for:

* Patients
* Doctors

Each dashboard contains relevant data and functionalities.

---

# Technologies Used

## Backend

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **TensorFlow / Keras**
* **NumPy**

## Frontend

* **HTML**
* **CSS**
* **JavaScript**
* **Jinja2 Templates**

## Database

* **MySQL**

## Machine Learning

* **Convolutional Neural Network (CNN)**
* Image preprocessing using **NumPy and TensorFlow**

---

# System Architecture

The system follows a **three-layer architecture**:

### 1. Presentation Layer

The frontend interface built using **HTML, CSS, and JavaScript** allows users to interact with the system through dashboards and forms.

### 2. Application Layer

The backend logic built using **Flask** handles authentication, report uploads, AI predictions, and doctor consultations.

### 3. Data Layer

The **MySQL database** stores all system information including:

* Patient records
* Doctor records
* Reports
* Consultation messages

---

# Machine Learning Workflow

The AI component of the project uses a **CNN model trained on chest X-ray images**.

### Preprocessing Steps

1. Upload chest X-ray image.
2. Resize image to **150 × 150 pixels**.
3. Convert image to numerical array.
4. Normalize pixel values by dividing by **255**.
5. Expand dimensions to match model input.
6. Pass image to trained CNN model.

### Prediction

The model outputs:

* **Prediction result** (Pneumonia / Normal)
* **Confidence score**

---

# Directory Structure

```
AI-Powered-Human-Diagnosis-System
│
├── app.py
│
├── model
│   └── pneumonia_model.h5
│
├── static
│   ├── css
│   │   └── style.css
│   │
│   ├── profile_uploads
│   │   └── default.jpg
│   │
│   ├── report_uploads
│   │
│   └── reports
│
├── templates
│   ├── login.html
│   ├── signup.html
│   ├── send_consultation.html
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── predict.html
│   └── logout.html
│
├── requirements.txt
│
└── README.md
```

---

# Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/AI-Powered-Human-Diagnosis-System.git
```

### 2. Navigate to Project Folder

```
cd AI-Powered-Human-Diagnosis-System
```

### 3. Create Virtual Environment

```
python -m venv venv
```

### 4. Activate Virtual Environment

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

### 5. Install Dependencies

```
pip install -r requirements.txt
```

### 6. Setup MySQL Database

Create a database and run the schema file.

### 7. Run the Application

```
python app.py
```

Open browser and go to

```
http://localhost:5000
```

---

# Example Workflow

1. Patient registers and logs in.
2. Patient uploads a chest X-ray image.
3. AI model processes the image.
4. System generates prediction and confidence score.
5. Patient can view report in dashboard.
6. Patient can send report to doctor for consultation.
7. Doctor reviews report and replies with advice.

---

#Tech Stack
##Backend:
Python – Core programming language used for model integration and server logic
Flask – Lightweight web framework used to build the backend and handle routing, requests, and responses
Flask-SQLAlchemy – ORM used to interact with the MySQL database

## Machine Learning / AI:
TensorFlow / Keras – Used to build and load the deep learning model for pneumonia detection
NumPy – Used for numerical operations and image array processing
Keras Image Preprocessing – Used for loading and resizing chest X-ray images

## Database:
MySQL – Stores patient details, doctor details, and generated diagnosis reports

## Frontend:
HTML5 – Structure of web pages
CSS3 – Styling and layout of the application
Jinja2 – Template engine used by Flask to render dynamic HTML pages

## Tools & Libraries:
Werkzeug Security – Used for password hashing and authentication
Pip – Dependency management using requirements.txt

## Image Processing:
TensorFlow Keras Image Utilities – Used for resizing images to 150×150 pixels and converting them into arrays for prediction.

---

# Advantages of the System

* Faster preliminary medical analysis
* Reduces workload for doctors
* Early disease detection
* Centralized patient report management
* AI assisted healthcare support

---

# Limitations

* AI prediction is not a replacement for professional diagnosis.
* Accuracy depends on training dataset quality.
* Currently supports limited medical conditions.

---

# Future Enhancements

* Support for multiple diseases.
* Integration with hospital systems.
* Real-time chat between doctor and patient.
* Mobile application version.
* Improved deep learning models.

---

# License

This project is developed for **academic and research purposes**.


