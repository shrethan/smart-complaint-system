# scms_app/routes/complaints.py
import csv 
import io
from flask import Blueprint, render_template, request, redirect, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from scms_app.models import Complaint, User
from scms_app import db
from scms_app.utils.pdf_report import generate_pdf
from flask import make_response 


complaint_bp = Blueprint('complaints', __name__)

@complaint_bp.route('/submit', methods=['GET', 'POST'])
@jwt_required()
def submit_complaint():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        complaint = Complaint(title=title, description=description, user_id=user.id)
        db.session.add(complaint)
        db.session.commit()
        return redirect('/complaints/list')
    return render_template('submit_complaint.html')

@complaint_bp.route('/list')
@jwt_required()
def list_complaints():
    complaints = Complaint.query.all()
    return render_template('complaints.html', complaints=complaints)

@complaint_bp.route('/pdf')
@jwt_required()
def download_pdf():
    complaints = Complaint.query.all()
    return generate_pdf(complaints)

@complaint_bp.route('/export')
@jwt_required()
def export_csv():
    complaints = Complaint.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Status', 'Assigned To'])

    for c in complaints:
        writer.writerow([c.id, c.title, c.status, c.assigned_to or ''])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=complaints.csv"
    response.headers["Content-Type"] = "text/csv"
    return response  # ✅ JUST return response (not a tuple!)



@complaint_bp.route('/admin-only')
@jwt_required()
def admin_only_route():
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != 'admin':
        return {"msg": "Admins only"}, 403
    return {"msg": "Welcome Admin!"}
