from weasyprint import HTML
from flask import make_response

def generate_pdf(complaints):
    html = "<h1>Complaint Report</h1><ul>"
    for c in complaints:
        html += f"<li><strong>{c.title}</strong> - {c.status}</li>"
    html += "</ul>"

    pdf = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=complaints.pdf'
    return response
