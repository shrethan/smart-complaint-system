from scms_app import create_app, db

app = create_app()

# Use app context to create all tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
