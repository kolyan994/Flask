from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Advertisement('{self.title}', '{self.owner}')"