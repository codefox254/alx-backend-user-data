#!/usr/bin/env python3
"""
Main file to display the structure of the User table.
"""

from user import User

# Print the name of the table associated with the User model
print(User.__tablename__)

# Iterate through each column in the User table and print its name and type
for column in User.__table__.columns:
    print(f"{column.name}: {column.type}")
