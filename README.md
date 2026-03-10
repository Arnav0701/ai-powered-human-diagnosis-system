# AI Powered Human Diagnosis System

## Overview

The **AI Powered Human Diagnosis System** is a web-based healthcare assistance platform that uses **Artificial Intelligence and Machine Learning** to help in preliminary medical diagnosis from medical reports and images. The system allows patients to upload medical reports (such as chest X-ray images), receive AI-based predictions, and consult with doctors for further advice.

This project combines **Deep Learning**, **Web Development**, and **Database Management** to create a complete diagnostic workflow that connects patients and doctors in a single platform.

The main goal of this project is to demonstrate how AI can support healthcare professionals by providing **quick preliminary analysis** and assisting in early detection of diseases such as **pneumonia from chest X-ray images**.

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

# Database Structure

The project uses **three main database tables**.

### Patients Table

Stores patient information.

Fields include:

* id
* name
* email
* age
* phone
* password
* profile_path

### Doctors Table

Stores doctor information.

Fields include:

* id
* name
* email
* specialization
* phone_number
* password
* profile_path

### Reports Table

Stores AI prediction reports.

Fields include:

* id
* patient_id
* report_type
* report_path
* prediction
* confidence
* report_date
* status

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

# Contributors

* **Arnav Singh**
* **Honey Pal**
* **Luv Tiwari**
* **Krishnanshue Sharma**

---

# License

This project is developed for **academic and research purposes**.

---

# Acknowledgement

We would like to thank our faculty mentors and institution for providing the guidance and resources required to complete this project successfully.
