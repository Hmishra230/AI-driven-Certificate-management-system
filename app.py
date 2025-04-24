# from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime, timedelta
# import uuid
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
# from flask import send_file
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy and LoginManager
# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"

# # Load Hugging Face model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
# model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

# # User model
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), nullable=False, default='user')

# # Certificate model
# class CertificateApplication(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
#     certificate_type = db.Column(db.String(100), nullable=False)
#     application_date = db.Column(db.DateTime, default=datetime.utcnow)
#     certificate_number = db.Column(db.String(36), unique=True, nullable=False)

# # Initialize database
# def init_db():
#     with app.app_context():
#         db.create_all()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # Utility functions
# def get_most_active_user():
#     result = db.session.query(
#         CertificateApplication.email, db.func.count(CertificateApplication.email)
#     ).group_by(CertificateApplication.email).order_by(
#         db.func.count(CertificateApplication.email).desc()
#     ).first()
#     return result if result else ("No data available", 0)

# def get_most_common_certificate_type():
#     result = db.session.query(
#         CertificateApplication.certificate_type, db.func.count(CertificateApplication.certificate_type).label('type_count')
#     ).group_by(CertificateApplication.certificate_type).order_by(
#         db.desc('type_count')
#     ).first()
#     return result if result else ("No data available", 0)

# def get_total_certificates():
#     return CertificateApplication.query.count()

# def get_certificates_today():
#     today = datetime.utcnow().date()
#     return CertificateApplication.query.filter(
#         db.func.date(CertificateApplication.application_date) == today
#     ).count()

# @app.route('/ask_gpt', methods=['POST'])
# @login_required
# def ask_gpt():
#     query = request.json.get('query', "").strip().lower()
#     if not query:
#         return jsonify({"error": "Query cannot be empty."}), 400

#     try:
#         # Explicit handling for predefined queries
#         if "most certificates" in query and "user" in query:
#             email, count = get_most_active_user()
#             response = f"The user who generated the most certificates is {email} with {count} certificates."
#         elif "most common" in query and "certificate type" in query:
#             cert_type, count = get_most_common_certificate_type()
#             response = f"The most common type of certificate generated is '{cert_type}' with {count} occurrences."
#         elif "total certificates" in query and "today" in query:
#             total_today = get_certificates_today()
#             response = f"Today, {total_today} certificates have been generated."
#         elif "total certificates" in query:
#             total_certificates = get_total_certificates()
#             response = f"A total of {total_certificates} certificates have been generated till date."
#         else:
#             # GPT fallback for non-predefined queries
#             prompt = f"The user asked: {query}\nAnswer in simple and concise terms."
#             inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
#             outputs = model.generate(inputs.input_ids, max_new_tokens=100, do_sample=True, temperature=0.7)
#             response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     except Exception as e:
#         response = f"An error occurred: {str(e)}"

#     return jsonify({"response": response}), 200

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         role = request.form['role']
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
#         new_user = User(name=name, email=email, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Signed up successfully!", "success")
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             session['role'] = user.role
#             return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'user_dashboard'))
#         flash("Invalid credentials!", "danger")
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     session.pop('role', None)
#     flash("Logged out successfully!", "success")
#     return redirect(url_for('index'))

# @app.route('/generate_certificate', methods=['GET', 'POST'])
# @login_required
# def generate_certificate():
#     if request.method == 'POST':
#         certificate = CertificateApplication(
#             name=request.form['name'],
#             email=current_user.email,
#             certificate_type=request.form['certificate_type'],
#             certificate_number=str(uuid.uuid4())
#         )
#         db.session.add(certificate)
#         db.session.commit()
#         flash("Certificate generated successfully!", "success")
#         return render_template('generate_certificate.html', certificate_number=certificate.certificate_number)
#     return render_template('certificate_form.html')

# @app.route('/download_certificate/<int:certificate_id>')
# @login_required
# def download_certificate(certificate_id):
#     # Fetch certificate details from the database
#     certificate = CertificateApplication.query.filter_by(id=certificate_id, email=current_user.email).first()
#     if not certificate:
#         flash("Certificate not found or unauthorized access!", "danger")
#         return redirect(url_for('user_dashboard'))

#     # Generate PDF
#     pdf_buffer = BytesIO()
#     c = canvas.Canvas(pdf_buffer, pagesize=letter)
#     c.drawString(100, 750, f"Certificate of Achievement")
#     c.drawString(100, 720, f"This certifies that {certificate.name}")
#     c.drawString(100, 690, f"has successfully completed the {certificate.certificate_type}.")
#     c.drawString(100, 660, f"Certificate Number: {certificate.certificate_number}")
#     c.drawString(100, 630, f"Issued on: {certificate.application_date.strftime('%Y-%m-%d')}")
#     c.save()

#     pdf_buffer.seek(0)
#     return send_file(
#         pdf_buffer,
#         as_attachment=True,
#         download_name=f"certificate_{certificate.certificate_number}.pdf",
#         mimetype="application/pdf"
#     )

# # @app.route('/user/dashboard')
# # @login_required
# # def user_dashboard():
# #     if current_user.role != 'user':
# #         flash("Unauthorized access!", "danger")
# #         return redirect(url_for('index'))

# #     user_certificates = CertificateApplication.query.filter_by(email=current_user.email).all()
# #     return render_template('user_dashboard.html', certificates=user_certificates)
# @app.route('/user/dashboard')
# @login_required
# def user_dashboard():
#     # Fetch certificates for the logged-in user
#     user_certificates = CertificateApplication.query.filter_by(email=current_user.email).all()
#     return render_template(
#         'user_dashboard.html', 
#         certificates=user_certificates, 
#         user=current_user  # Pass the current user to the template
#     )

# @app.route('/admin/dashboard')
# @login_required
# def admin_dashboard():
#     if current_user.role != 'admin':
#         flash("Unauthorized access!", "danger")
#         return redirect(url_for('index'))

#     # Fetch statistics
#     stats = {
#         "total_users": User.query.count(),
#         "total_certificates": get_total_certificates(),
#         "most_common_type": get_most_common_certificate_type(),
#         "most_active_user": get_most_active_user(),
#         "today_certificates": get_certificates_today(),
#     }

#     # Fetch all certificates
#     certificates = CertificateApplication.query.all()

#     return render_template('admin_dashboard.html', stats=stats, certificates=certificates)
# # @app.route('/admin/dashboard')
# # @login_required
# # def admin_dashboard():
# #     if current_user.role != 'admin':
# #         flash("Unauthorized access!", "danger")
# #         return redirect(url_for('index'))

# #     # Fetch statistics
# #     stats = {
# #         "total_users": User.query.count(),
# #         "total_certificates": get_total_certificates(),
# #         "most_common_type": get_most_common_certificate_type(),
# #         "most_active_user": get_most_active_user(),
# #         "today_certificates": get_certificates_today(),
# #     }

# #     # Fetch all certificates
# #     certificates = CertificateApplication.query.all()

# #     return render_template('admin_dashboard.html', stats=stats, certificates=certificates)


# @app.route('/certificate_preview/<certificate_number>')
# @login_required
# def certificate_preview(certificate_number):
#     # Retrieve the certificate using the certificate_number
#     certificate = CertificateApplication.query.filter_by(certificate_number=certificate_number).first()

#     if not certificate:
#         flash("Certificate not found!", "danger")
#         return redirect(url_for('user_dashboard'))

#     # Render a template or return some response
#     return render_template('certificate_preview.html', certificate=certificate)

# @app.route('/delete_certificate/<int:certificate_id>', methods=['POST'])
# @login_required
# def delete_certificate(certificate_id):
#     if current_user.role != 'admin':
#         flash("Unauthorized access!", "danger")
#         return redirect(url_for('index'))

#     # Find the certificate
#     certificate = CertificateApplication.query.get_or_404(certificate_id)

#     try:
#         db.session.delete(certificate)
#         db.session.commit()
#         flash("Certificate deleted successfully!", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"An error occurred: {str(e)}", "danger")

#     return redirect(url_for('admin_dashboard'))

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True, port=8080)

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and LoginManager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Load Hugging Face model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

# Certificate model
class CertificateApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    certificate_type = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    certificate_number = db.Column(db.String(36), unique=True, nullable=False)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Utility functions
def get_most_active_user():
    result = db.session.query(
        CertificateApplication.email, db.func.count(CertificateApplication.email)
    ).group_by(CertificateApplication.email).order_by(
        db.func.count(CertificateApplication.email).desc()
    ).first()
    return result if result else ("No data available", 0)

def get_most_common_certificate_type():
    result = db.session.query(
        CertificateApplication.certificate_type, db.func.count(CertificateApplication.certificate_type).label('type_count')
    ).group_by(CertificateApplication.certificate_type).order_by(
        db.desc('type_count')
    ).first()
    return result if result else ("No data available", 0)

def get_total_certificates():
    return CertificateApplication.query.count()

def get_certificates_today():
    today = datetime.utcnow().date()
    return CertificateApplication.query.filter(
        db.func.date(CertificateApplication.application_date) == today
    ).count()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Signed up successfully!", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['role'] = user.role
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'user_dashboard'))
        flash("Invalid credentials!", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('role', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))

@app.route('/generate_certificate', methods=['GET', 'POST'])
@login_required
def generate_certificate():
    if request.method == 'POST':
        certificate = CertificateApplication(
            name=request.form['name'],
            email=current_user.email,
            certificate_type=request.form['certificate_type'],
            certificate_number=str(uuid.uuid4())
        )
        db.session.add(certificate)
        db.session.commit()
        flash("Certificate generated successfully!", "success")
        return render_template('generate_certificate.html', certificate_number=certificate.certificate_number)
    return render_template('certificate_form.html')

# @app.route('/download_certificate/<int:certificate_id>')
# @login_required
# def download_certificate(certificate_id):
#     certificate = CertificateApplication.query.filter_by(id=certificate_id, email=current_user.email).first()
#     if not certificate:
#         flash("Certificate not found or unauthorized access!", "danger")
#         return redirect(url_for('user_dashboard'))
@app.route('/download_certificate/<int:certificate_id>')
@login_required
def download_certificate(certificate_id):
    # Fetch certificate details from the database
    certificate = CertificateApplication.query.filter_by(id=certificate_id, email=current_user.email).first()
    if not certificate:
        flash("Certificate not found or unauthorized access!", "danger")
        return redirect(url_for('user_dashboard'))

    # Generate PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Set up styles
    title_font = "Helvetica-Bold"
    subtitle_font = "Helvetica"
    body_font = "Times-Roman"
    c.setFont(title_font, 24)
    c.setFillColorRGB(0.1, 0.3, 0.7)

    # Add certificate title
    c.drawCentredString(300, 750, "Certificate of Achievement")

    # Draw a border
    c.setStrokeColorRGB(0.1, 0.3, 0.7)
    c.setLineWidth(2)
    c.rect(50, 500, 500, 200, stroke=1, fill=0)

    # Add recipient's name
    c.setFont(subtitle_font, 18)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 680, f"This certifies that")
    c.setFont(body_font, 22)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.drawCentredString(300, 650, f"{certificate.name}")

    # Add certificate details
    c.setFont(subtitle_font, 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 620, f"has successfully completed the")
    c.drawCentredString(300, 600, f"{certificate.certificate_type}.")

    # Add certificate metadata
    c.setFont(body_font, 14)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(100, 550, f"Certificate Number: {certificate.certificate_number}")
    c.drawString(100, 530, f"Issued on: {certificate.application_date.strftime('%Y-%m-%d')}")

    # Signature area
    c.drawString(400, 520, "________________________")
    c.drawString(400, 500, "Authorized Signature")

    # Finish up
    c.save()

    # Return the generated PDF
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"certificate_{certificate.certificate_number}.pdf",
        mimetype="application/pdf"
    )


    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, f"Certificate of Achievement")
    c.drawString(100, 720, f"This certifies that {certificate.name}")
    c.drawString(100, 690, f"has successfully completed the {certificate.certificate_type}.")
    c.drawString(100, 660, f"Certificate Number: {certificate.certificate_number}")
    c.drawString(100, 630, f"Issued on: {certificate.application_date.strftime('%Y-%m-%d')}")
    c.save()
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"certificate_{certificate.certificate_number}.pdf",
        mimetype="application/pdf"
    )

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    user_certificates = CertificateApplication.query.filter_by(email=current_user.email).all()
    return render_template('user_dashboard.html', certificates=user_certificates, user=current_user)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('index'))

    stats = {
        "total_users": User.query.count(),
        "total_certificates": get_total_certificates(),
        "most_common_type": get_most_common_certificate_type(),
        "most_active_user": get_most_active_user(),
        "today_certificates": get_certificates_today(),
    }
    certificates = CertificateApplication.query.all()
    return render_template('admin_dashboard.html', stats=stats, certificates=certificates)

@app.route('/ask_gpt', methods=['POST'])
@login_required
def ask_gpt():
    query = request.json.get('query', "").strip().lower()
    if not query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        if "most certificates" in query and "user" in query:
            email, count = get_most_active_user()
            response = f"The user who generated the most certificates is {email} with {count} certificates."
        elif "most common" in query and "certificate type" in query:
            cert_type, count = get_most_common_certificate_type()
            response = f"The most common type of certificate generated is '{cert_type}' with {count} occurrences."
        elif "total certificates" in query and "today" in query:
            total_today = get_certificates_today()
            response = f"Today, {total_today} certificates have been generated."
        elif "total certificates" in query:
            total_certificates = get_total_certificates()
            response = f"A total of {total_certificates} certificates have been generated till date."
        else:
            prompt = f"The user asked: {query}\nAnswer in simple and concise terms."
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            outputs = model.generate(inputs.input_ids, max_new_tokens=100, do_sample=True, temperature=0.7)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return jsonify({"response": response}), 200

@app.route('/certificate_preview/<certificate_number>')
@login_required
def certificate_preview(certificate_number):
    certificate = CertificateApplication.query.filter_by(certificate_number=certificate_number).first()
    if not certificate:
        flash("Certificate not found!", "danger")
        return redirect(url_for('user_dashboard'))
    return render_template('certificate_preview.html', certificate=certificate)

@app.route('/delete_certificate/<int:certificate_id>', methods=['POST'])
@login_required
def delete_certificate(certificate_id):
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('index'))

    certificate = CertificateApplication.query.get_or_404(certificate_id)
    try:
        db.session.delete(certificate)
        db.session.commit()
        flash("Certificate deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
