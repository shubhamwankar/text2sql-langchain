from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date
import random

# Create the SQLite database engine
engine = create_engine('sqlite:///employee_database.db', echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Employee table
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")

# Define the Department table
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    employees = relationship("Employee", back_populates="department")

# Define the Position table
class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)

    employees = relationship("Employee", back_populates="position")

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert dummy data
departments = ["HR", "IT", "Finance", "Marketing", "Sales"]
# for dept_name in departments:
#     department = Department(name=dept_name)
#     session.add(department)

positions = ["Manager", "Senior Developer", "Junior Developer", "Analyst", "Coordinator"]
# for pos_title in positions:
#     position = Position(title=pos_title)
#     session.add(position)

# # Commit the changes to the database
# session.commit()

# Generate dummy employee data
first_names = ["John", "Jane", "Mike", "Emily", "David", "Sarah", "Chris", "Lisa"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

used_emails = set()

for i in range(50):  # Generate 50 dummy employees
    while True:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
        
        if email not in used_emails:
            used_emails.add(email)
            break

    hire_date = date(random.randint(2010, 2023), random.randint(1, 12), random.randint(1, 28))
    salary = round(random.uniform(30000, 100000), 2)
    department_id = random.randint(1, len(departments))
    position_id = random.randint(1, len(positions))

    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hire_date=hire_date,
        salary=salary,
        department_id=department_id,
        position_id=position_id
    )
    session.add(employee)

# Commit the changes to the database
session.commit()

session.close()

print("Dummy database created successfully!")