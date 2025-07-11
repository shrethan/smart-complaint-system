from flask import Response
import csv
from io import StringIO
from scms_app.models import Complaint

def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Status', 'Created At'])

    for c in Complaint.query.all():
        writer.writerow([c.id, c.title, c.status, c.created_at])

    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=complaints.csv"})
