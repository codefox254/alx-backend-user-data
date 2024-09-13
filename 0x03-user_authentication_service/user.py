#!/usr/bin/env python3
"""
This module defines the SQLAlchemy model for the User table.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    """
    User model for the users table in the database.
    Attributes:
        id (int): The integer primary key.
        email (str): A non-nullable string for the user's email (max length 250).
        hashed_password (str): A non-nullable string for the hashed password (max length 250).
        session_id (str): A nullable string for the session ID (max length 250).
        reset_token (str): A nullable string for the password reset token (max length 250).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

# Example engine setup (you'll need to adjust this for your actual database)
engine = create_engine('sqlite:///users.db')  # Replace with your database URL
Base.metadata.create_all(engine)

# Example session setup (for testing and interactions)
Session = sessionmaker(bind=engine)
session = Session()

# Example of adding a user (for testing purposes)
if __name__ == "__main__":
    new_user = User(email="test@example.com", hashed_password="hashed_password")
    session.add(new_user)
    session.commit()
