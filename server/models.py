from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name or Author.query.filter_by(name=name).first() is not None:
            raise ValueError("Must have a unique name")
        return name
    
    @validates('phone_number')
    def validates_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone number must be 10 digits")
        return number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validates_title(self, key, title):
        if not title:
            raise ValueError("Must have title")
        
        required_phrases = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(phrase in title for phrase in required_phrases):
            raise ValueError(f"Invalid value for title: {title}. Title must contain one of the following phrases: {', '.join(required_phrases)}")

        return title
    @validates('content')
    def validates_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Must be at least 250 chars")
        return content
    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Summary must be less than 250 chars.")
        return summary
    @validates('category')
    def validates_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category incorrect")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
