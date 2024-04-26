from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (replace with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your data model (replace with your table structure)
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<UserData {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Create a new user object
        new_user = UserData(name=name, email=email)

        # Add user to the database session
        db.session.add(new_user)

        # Commit changes to the database
        try:
            db.session.commit()
            message = "Data inserted successfully!"
        except Exception as e:
            # Handle database errors
            db.session.rollback()
            message = f"Error: {str(e)}"

        return render_template('index.html', message=message)

    return render_template('index.html')

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
