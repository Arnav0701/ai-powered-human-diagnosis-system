import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, redirect, flash, session
from tensorflow.keras.preprocessing import image
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import re

def validate_text_inputs(name, phone, email):
    if not re.match(r"^[A-Za-z\s]+$", str(name)):
        return False, "Invalid input! Name must contain only alphabetical letters."
    if not str(phone).isdigit():
        return False, "Invalid input! Mobile number must contain only numerical digits."
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", str(email)):
        return False, "Invalid input! Please enter a valid email format."
    return True, ""

app = Flask(__name__)

app.secret_key ="234e3556yg6ut7drdfyf56yfvyxwedscikiurftghj"

# File Validation Setup
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load model once at start
model = tf.keras.models.load_model("model.h5")

REPORT_UPLOAD_FOLDER = "static/report_uploads"
PROFILE_UPLOAD_FOLDER = "static/profile_uploads"
app.config['REPORT_UPLOAD_FOLDER'] = REPORT_UPLOAD_FOLDER     #is a dictionary-like object used to store configuration variables for your application.
app.config['PROFILE_UPLOAD_FOLDER'] = PROFILE_UPLOAD_FOLDER 

# MySQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/diagnosis_system"
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
        if request.form.get("user_type")=="doctor":
            name = request.form.get("name", "")
            email = request.form.get("email", "")
            specialization = request.form.get("specialization", "")
            phone_num = request.form.get("phone", "")
            license_num = request.form.get("license", "")
            about = request.form.get("about", "")
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            # Perform strict text input validation
            is_valid, error_msg = validate_text_inputs(name, phone_num, email)
            if not is_valid:
                flash(error_msg, "fail")
                return render_template("signup.html", name=name, email=email, about=about, phone=phone_num, specialization=specialization, license=license_num)

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

        elif request.form.get("user_type")=="patient":
            name = request.form.get("name", "")
            email = request.form.get("email", "")
            age = request.form.get("age", "")
            phone_num = request.form.get("phone", "")
            gender = request.form.get("gender", "")
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            # Perform strict text input validation
            is_valid, error_msg = validate_text_inputs(name, phone_num, email)
            if not is_valid:
                flash(error_msg, "fail")
                return render_template("signup.html")

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
            if not allowed_file(file.filename):
                flash("Only JPG and PNG images are allowed for profile photos!", "fail")
                return redirect("/patient_dashboard?active_tab=profile")
                
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["PROFILE_UPLOAD_FOLDER"], filename)

            file.save(filepath)

            existing_user.profile_path = "profile_uploads/" + filename
            db.session.commit()
            return redirect("/patient_dashboard?active_tab=profile")

    reports = Report.query.filter_by(patient_id=existing_user.id).all()
    doctors = Doctor.query.all()
    
    # Intelligently determine which tab should be active
    active_tab = request.args.get('active_tab', 'home')
    if request.args.get('edit_mode') == 'true':
        active_tab = 'profile'

    return render_template(
        "patient_dashboard.html",
        name=existing_user.name,
        age=existing_user.age,
        email=existing_user.email,
        phone=existing_user.phone_number,
        id=existing_user.id,
        profile_path=existing_user.profile_path,
        reports=reports,
        doctors=doctors,
        active_tab=active_tab
    )

@app.route("/update_patient_profile", methods=["POST"])
def update_patient_profile():
    if "email" not in session or session.get("user_type") != "patient":
        flash("Unauthorized access", "fail")
        return redirect("/login")
        
    email = session["email"]
    patient = Patient.query.filter_by(email=email).first()
    if not patient:
        flash("Patient not found", "fail")
        return redirect("/login")
        
    verify_password = request.form.get("verify_password", "")
    if not check_password_hash(patient.password, verify_password):
        flash("Incorrect password. Profile update aborted for your security.", "fail")
        return redirect("/patient_dashboard?edit_mode=true&active_tab=profile")

    new_name = request.form.get("name", patient.name)
    new_age = request.form.get("age", patient.age)
    new_email = request.form.get("email", patient.email)
    new_phone = request.form.get("phone", patient.phone_number)
    
    is_valid, error_msg = validate_text_inputs(new_name, new_phone, new_email)
    if not is_valid:
        flash(error_msg, "fail")
        return redirect("/patient_dashboard?edit_mode=true&active_tab=profile")
        
    # Check if they changed their email to one that already exists
    if new_email != email:
        existing_patient = Patient.query.filter_by(email=new_email).first()
        if existing_patient:
            flash("That email is already registered to another user.", "fail")
            return redirect("/patient_dashboard?edit_mode=true&active_tab=profile")
        session["email"] = new_email
        
    patient.name = new_name
    patient.age = new_age
    patient.email = new_email
    patient.phone_number = new_phone
    
    db.session.commit()
    flash("Profile updated safely and successfully!", "success")
    return redirect("/patient_dashboard?active_tab=profile")

@app.route("/predict", methods=["POST","GET"])
def predict():
    if "user_type" not in session or session.get("user_type") != "patient":
        flash("Access denied! Login as patient first.","fail")
        return redirect("/login")
    
    existing_user = Patient.query.filter_by(email=session["email"]).first()
    if not existing_user:
        session.clear()
        flash("Session invalid. Please login again.","fail")
        return redirect("/login")
    
    if request.method=="POST":
        file = request.files.get("file")
        
        if not file or file.filename == "":
            flash("No file was attached for prediction.", "fail")
            return redirect("/predict")
            
        if not allowed_file(file.filename):
            flash("Invalid file type! Please upload a valid medical scan (JPG, PNG).", "fail")
            return redirect("/predict")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['REPORT_UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess image safely
        try:
            img = image.load_img(filepath, target_size=(150, 150))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)[0][0]
            probability = float(prediction) * 100
        except Exception as e:
            flash("Failed to read image data. The file might be corrupted.", "fail")
            return redirect("/predict")

        # Result Logic (Corrected Indentation)
        if prediction > 0.5:
            result = "Pneumonia"
            confidence = probability
        else:
            result = "Normal"
            confidence = 100 - probability

        test_status = "Positive" if result != "Normal" else "Negative"

        db_path = "report_uploads/" + file.filename
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
    
    # Attach doctor details to each consultation for the template
    for c in consultations:
        doc = Doctor.query.get(c.doctor_id)
        c.doctor_name = doc.name if doc else "Unknown Doctor"
        c.doctor_spec = doc.specialization if doc else "N/A"

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

            if file and file.filename != "":
                if not allowed_file(file.filename):
                    flash("Only JPG and PNG images are allowed for profile photos!", "fail")
                    return redirect("/doctor_dashboard?active_tab=profile")
                    
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["PROFILE_UPLOAD_FOLDER"], filename)

                file.save(filepath)

                existing_doctor.profile_path = "profile_uploads/" + filename
                db.session.commit()

                flash("Profile photo uploaded successfully","success")
                return redirect("/doctor_dashboard?active_tab=profile")

            return redirect("/doctor_dashboard?active_tab=profile")


        # CONSULTATION REPLY
        consult_id = request.form.get("consult_id")
        reply_text = request.form.get("doctor_reply")

        consultation = Consultation.query.get(consult_id)

        if consultation and consultation.doctor_id == existing_doctor.id:

            consultation.doctor_reply = reply_text
            consultation.status = "replied"

            db.session.commit()

            flash("Reply submitted successfully.","success")

        return redirect("/doctor_dashboard?active_tab=messages")

    # Intelligently determine which tab should be active
    active_tab = request.args.get('active_tab', 'profile')
    if request.args.get('edit_mode') == 'true':
        active_tab = 'profile'

    filepath=existing_doctor.profile_path
    return render_template(
        "doctor_dashboard.html",
        doctor=existing_doctor,
        consultations=consultations,
        profile_path=filepath,
        active_tab=active_tab
    )

@app.route("/update_doctor_profile", methods=["POST"])
def update_doctor_profile():
    if "email" not in session or session.get("user_type") != "doctor":
        flash("Unauthorized access", "fail")
        return redirect("/login")
        
    email = session["email"]
    doctor = Doctor.query.filter_by(email=email).first()
    if not doctor:
        flash("Doctor not found", "fail")
        return redirect("/login")
        
    verify_password = request.form.get("verify_password", "")
    if not check_password_hash(doctor.password, verify_password):
        flash("Incorrect password. Profile update aborted for your security.", "fail")
        return redirect("/doctor_dashboard?edit_mode=true&active_tab=profile")

    new_name = request.form.get("name", doctor.name)
    new_email = request.form.get("email", doctor.email)
    new_phone = request.form.get("phone", doctor.phone_number)
    new_spec = request.form.get("specialization", doctor.specialization)
    new_about = request.form.get("about", doctor.about)
    
    # Validation
    is_valid, error_msg = validate_text_inputs(new_name, new_phone, new_email)
    if not is_valid:
        flash(error_msg, "fail")
        return redirect("/doctor_dashboard?edit_mode=true&active_tab=profile")
        
    # Email unique check
    if new_email != email:
        existing_doc = Doctor.query.filter_by(email=new_email).first()
        if existing_doc:
            flash("That email is already registered to another user.", "fail")
            return redirect("/doctor_dashboard?edit_mode=true&active_tab=profile")
        session["email"] = new_email
        
    doctor.name = new_name
    doctor.email = new_email
    doctor.phone_number = new_phone
    doctor.specialization = new_spec
    doctor.about = new_about
    
    db.session.commit()
    flash("Doctor profile updated successfully!", "success")
    return redirect("/doctor_dashboard?active_tab=profile")


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