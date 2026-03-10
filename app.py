import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, redirect, flash, session
from tensorflow.keras.preprocessing import image
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)

app.secret_key =""
# Load model once at start
model = tf.keras.models.load_model("model.h5")

REPORT_UPLOAD_FOLDER = "static/report_uploads"
PROFILE_UPLOAD_FOLDER = "static/profile_uploads"
app.config['REPORT_UPLOAD_FOLDER'] = REPORT_UPLOAD_FOLDER     #is a dictionary-like object used to store configuration variables for your application.
app.config['PROFILE_UPLOAD_FOLDER'] = PROFILE_UPLOAD_FOLDER 

# MySQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#creating table Model     
class Doctor(db.Model):         #db.Model is created inside the SQLAlchemy constructor
    __tablename__ = "doctors"   #db.Model is the base class Doctor, Patient,Report
                                #representing tables as classes in python(flask)

    id = db.Column(db.Integer, primary_key=True)    #Column is a class and Integer is a class that define sql datatype  
    name = db.Column(db.String(100))    #db.String(100) → specifies the SQL data type (VARCHAR(100) in SQL)
                                        #db.Column(...) → wraps that data type into a column object with extra info (nullable, primary key,default, etc.)
                                        #id,name,email... are the attributes of Doctor class
    email = db.Column(db.String(100), unique=True)
    specialization = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    license_number = db.Column(db.String(50))
    password = db.Column(db.String(200))
    account_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    about = db.Column(db.String(1000))
    profile_path = db.Column(db.String(200))

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)
    account_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    profile_path = db.Column(db.String(200))    

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient_name = db.Column(db.String(100))
    report_path = db.Column(db.String(255))
    status = db.Column(db.String(20))
    report_type = db.Column(db.String(100))
    confidence = db.Column(db.Float, default=0.0)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)
    report_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class Consultation(db.Model):
    __tablename__ = "consultations"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    report_path = db.Column(db.String(200))
    prediction = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    patient_description = db.Column(db.Text)
    doctor_reply = db.Column(db.Text)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    report_id = db.Column(db.Integer)


#routes
@app.route("/")
def home():
    return render_template("login.html")

#generating unique 5 digit ids for tables
def generate_patient_id():
    while True:
        new_id = random.randint(100000, 999999)
        if not Patient.query.get(new_id):   #this query checks the primary key column. if id already exists there.
            return new_id

def generate_doctor_id():
    while True:
        new_id = random.randint(100000, 999999)
        if not Doctor.query.get(new_id):
            return new_id

def generate_report_id():
    while True:
        new_id = random.randint(100000, 999999)
        if not Report.query.get(new_id):
            return new_id
        
def generate_consultation_id():
    while True:
        new_id = random.randint(100000, 999999)
        if not Consultation.query.get(new_id):
            return new_id
        
        
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        if request.form["user_type"]=="doctor":
            name = request.form["name"]
            email = request.form["email"]
            specialization = request.form["specialization"]
            phone_num = request.form["phone"]
            license_num = request.form["license"]
            about = request.form["about"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]
            if password!=confirm_password:
                flash("Password confirmation failed!", "fail")
                return render_template("signup.html",  name=name, email=email, about=about, phone=phone_num, specialization=specialization, license=license_num)
            
            existing_user = Doctor.query.filter_by(email=email).first()   #filter_by() and first() are methods of SQLAlchemy’s BaseQuery class, which you get when you access Model.query. query is an instance of a class (BaseQuery), not a separate class you inherit from like Model.
            existing_user2 = Doctor.query.filter_by(license_number=license_num).first()
            if existing_user or existing_user2:
                flash("Doctor already registered!", "fail")
                return render_template("signup.html")
            else:
                hashed_password = generate_password_hash(password)
                new_doctor = Doctor(id= generate_doctor_id(),
                                    name= name,
                                    email= email,
                                    specialization= specialization,
                                    phone_number= phone_num,
                                    license_number= license_num,
                                    password= hashed_password,
                                    about=about
                                    )
                db.session.add(new_doctor)
                db.session.commit()
                flash("Doctor registered successfully", "success")
                return redirect("/login")

        elif request.form["user_type"]=="patient":
            name = request.form["name"]
            email = request.form["email"]
            age = request.form["age"]
            phone_num = request.form["phone"]
            gender = request.form["gender"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]
            if password!=confirm_password:
                flash("Password confirmed failed!","fail")
                return render_template("signup.html")
            
            existing_user = Patient.query.filter_by(email=email).first()
            if existing_user:
                flash("Patient already registered!","fail")
                return render_template("signup.html")
            else:
                hashed_password = generate_password_hash(password)
                new_patient = Patient(id= generate_patient_id(),
                    name=name,
                    age=age,
                    email=email,
                    phone_number=phone_num,
                    gender=gender,
                    password=hashed_password
                )
                db.session.add(new_patient)
                db.session.commit()
                flash("Patient registered successfully","success")
                return redirect("/login")

    if request.method=="GET":
        return render_template("signup.html")      


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]

        existing_user=Doctor.query.filter_by(email=email).first()
        if existing_user:
            if check_password_hash(existing_user.password, password):
                session["user_type"]="doctor"
                session["email"]=email
                flash("Doctor login successful", "success")
                return redirect("/doctor_dashboard")
            else:
                flash("Incorrect password!","fail")
                return redirect("/login")
            
        existing_user=Patient.query.filter_by(email=email).first()
        if existing_user:
            if check_password_hash(existing_user.password, password):
                session["user_type"]="patient"
                session["email"]=email
                flash("Patient login successful","success")
                return redirect("/patient_dashboard")
            else:
                flash("Incorrect Password!","fail")
                return redirect("/login")
        
        else:
            flash("Email not registered!","fail")
            return redirect("/login")
        
    if request.method=="GET":
        return render_template("login.html")


@app.route("/patient_dashboard", methods=["GET", "POST"])
def patient_dashboard():

    if "user_type" not in session or "email" not in session:
        flash("Session lost! Login first", "fail")
        return redirect("/login")

    if session.get("user_type") != "patient":
        flash("Access denied!", "fail")
        return redirect("/login")

    existing_user = Patient.query.filter_by(email=session["email"]).first()

    if request.method == "POST":
        file = request.files.get("profile_photo")

        if file and file.filename != "":
            filename = file.filename
            filepath = os.path.join(app.config["PROFILE_UPLOAD_FOLDER"], filename)

            file.save(filepath)

            existing_user.profile_path = "profile_uploads/" + filename
            db.session.commit()

    reports = Report.query.filter_by(patient_id=existing_user.id).all()
    doctors = Doctor.query.all()

    return render_template(
        "patient_dashboard.html",
        name=existing_user.name,
        age=existing_user.age,
        email=existing_user.email,
        phone=existing_user.phone_number,
        id=existing_user.id,
        profile_path=existing_user.profile_path,
        reports=reports,
        doctors=doctors
    )

@app.route("/predict", methods=["POST","GET"])
def predict():
    if "user_type" not in session or "email" not in session:
        flash("session lost! login first","fail")
        return redirect("/login")
    
    if request.method=="POST":
        file = request.files["file"]        # request.files behaves like a dictionary. Specifically an ImmutableMultiDict (Flask object that works like a dictionary)

        if file:
            filepath = os.path.join(app.config['REPORT_UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Preprocess image
            img = image.load_img(filepath, target_size=(150, 150))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)[0][0]     #returns the raw output of the model for the batch of images.
            probability = float(prediction) * 100           #[0] → selects the first element of the batch. Now it’s: [0.82]
                                                            #[0] → selects the scalar value inside the array. Now it’s: 0.82 (a float)
            if prediction > 0.5:
                result = "Pneumonia"
                confidence = probability
            else:
                result = "Normal"
                confidence = 100 - probability

            test_status = ""
            if result!="Normal":
                test_status = "Positive"
            else:
                test_status = "Negative"

            db_path = "report_uploads/" + file.filename
            existing_user = Patient.query.filter_by(email=session["email"]).first()
            new_report = Report(id=generate_report_id(),
                patient_id=existing_user.id,
                patient_name=existing_user.name,
                report_path=db_path,   
                status=test_status,
                confidence=confidence,
                report_type=request.form["report_type"],
                )
            db.session.add(new_report)
            db.session.commit()

            return render_template("predict.html",
                                prediction=result,
                                confidence=round(confidence, 2),
                                image_path=filepath)

    return render_template("predict.html")


@app.route("/send_consultation", methods=["POST","GET"])
def send_consultation():
    if "user_type" not in session or "email" not in session:
        flash("Session lost! Login first.", "fail")
        return redirect("/login")
    
    existing_user = Patient.query.filter_by(email=session["email"]).first()
    doctors = Doctor.query.all()

    if request.method == "POST":
        existing_report = Report.query.filter_by(id=request.form["report_id"]).first()
        if not existing_report:
            flash("Report not found. Please enter a valid report ID.", "fail")
            return redirect("/send_consultation")

        consultation = Consultation(id=generate_consultation_id(),
            patient_id=existing_user.id,
            doctor_id=request.form["doctor_id"],
            prediction=existing_report.status,
            confidence_score=existing_report.confidence,
            patient_description=request.form["description"],
            status="pending",
            report_path=existing_report.report_path,
            report_id=request.form["report_id"]
        )
        db.session.add(consultation)

        # Update report with doctor_id
        existing_report.doctor_id = request.form["doctor_id"]

        db.session.commit()
        flash("Request sent to doctor successfully", "success")
        

    # GET or after POST → fetch consultations for current patient
    consultations = Consultation.query.filter_by(patient_id=existing_user.id).order_by(Consultation.created_at.desc()).all()
    return render_template("send_consultation.html", doctors=doctors, consultations=consultations)


# import os
# from werkzeug.utils import secure_filename

@app.route("/doctor_dashboard", methods=["GET","POST"])
def doctor_dashboard():

    if "user_type" not in session or session["user_type"] != "doctor":
        flash("Please login as doctor.", "fail")
        return redirect("/login")

    existing_doctor = Doctor.query.filter_by(email=session["email"]).first()

    consultations = Consultation.query.filter_by(
        doctor_id=existing_doctor.id
    ).order_by(Consultation.created_at.desc()).all()


    if request.method == "POST":

        # PROFILE UPLOAD
        if "profile_photo" in request.files:

            file = request.files["profile_photo"]

            if file.filename != "":

                filepath = os.path.join(app.config["PROFILE_UPLOAD_FOLDER"], file.filename)

                file.save(filepath)

                existing_doctor.profile_path = "profile_uploads/" + file.filename

                db.session.commit()

                flash("Profile photo uploaded successfully","success")

            return redirect("/doctor_dashboard")


        # CONSULTATION REPLY
        consult_id = request.form.get("consult_id")
        reply_text = request.form.get("doctor_reply")

        consultation = Consultation.query.get(consult_id)

        if consultation and consultation.doctor_id == existing_doctor.id:

            consultation.doctor_reply = reply_text
            consultation.status = "replied"

            db.session.commit()

            flash("Reply submitted successfully.","success")

        return redirect("/doctor_dashboard")

    filepath=existing_doctor.profile_path
    return render_template(
        "doctor_dashboard.html",
        doctor=existing_doctor,
        consultations=consultations,
        profile_path=filepath
    )


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        # User clicked Yes → log out
        session.clear()
        flash("logout successful","success")
        return redirect('login')  # Redirect to login page

    # GET request → show logout confirmation page
    return render_template('logout.html')

if __name__ == "__main__":
    app.run(debug=True)