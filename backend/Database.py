# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# from pymysql.constants import CLIENT
# import os

# load_dotenv()

# db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'
# # Create engine with support for multiple statements
# engine = create_engine(db_url, connect_args={"client_flag": CLIENT.MULTI_STATEMENTS})
# # Create session
# Session = sessionmaker(bind=engine)
# db = Session()
# # Define all create table queries
# create_table_query = text("""
# CREATE TABLE IF NOT EXISTS user (
#     userid INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL,
#     password VARCHAR(100) NOT NULL
# );
# """),
# create_table_query = text("""
# CREATE TABLE IF NOT EXISTS courses (
#     courseid INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(100) NOT NULL,
#     level VARCHAR(100) NOT NULL
# );
# """),
# create_table_query = text("""
# CREATE TABLE IF NOT EXISTS enrollments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     userid INT,
#     courseid INT,
#     FOREIGN KEY (userid) REFERENCES User(userid),
#     FOREIGN KEY (courseid) REFERENCES courses(courseid)
# );
# """)
# db.execute(create_table_query)
# print("Tables have been created successfully.")


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT
import os

load_dotenv()

db_url = (
    f"mysql+pymysql://{os.getenv('dbuser')}:{os.getenv('dbpassword')}"
    f"@{os.getenv('dbhost')}:{os.getenv('dbport')}/{os.getenv('dbname')}"
)

# Create engine with support for multiple statements
engine = create_engine(db_url, connect_args={"client_flag": CLIENT.MULTI_STATEMENTS})

# Create session
Session = sessionmaker(bind=engine)
db = Session()

try:
    # Create user table
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS user (
            userid INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """))

    # Create courses table
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS courses (
            courseid INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            level VARCHAR(100) NOT NULL
        );
    """))

    # Create enrollments table (after user & courses exist)
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            userid INT,
            courseid INT,
            FOREIGN KEY (userid) REFERENCES user(userid),
            FOREIGN KEY (courseid) REFERENCES courses(courseid)
        );
    """))

    db.commit()
    print("Tables have been created successfully.")

finally:
    db.close()