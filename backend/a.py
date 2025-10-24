# # ...existing code...
# engine = create_engine(
#     db_url,
#     connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}
# )

# Session = sessionmaker(bind=engine)
# db = Session()

# create_table_user = text("""
# CREATE TABLE IF NOT EXISTS `user` (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL UNIQUE
# );
# """)

# create_table_courses = text("""
# CREATE TABLE IF NOT EXISTS courses (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(100) NOT NULL,
#     level VARCHAR(100) NOT NULL,
#     description TEXT NOT NULL
# );
# """)

# create_table_enrollments = text("""
# CREATE TABLE IF NOT EXISTS enrollments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     course_id INT,
#     FOREIGN KEY (user_id) REFERENCES `user`(id),
#     FOREIGN KEY (course_id) REFERENCES courses(id)
# );
# """)

# for ddl in (create_table_user, create_table_courses, create_table_enrollments):
#     db.execute(ddl)

# db.commit()
# db.close()

# print("Tables created successfully.")
# # ...existing code...

# ...existing code...
@app.post("/signup")
def signUp(input:simple):
    try:
        duplicate_query=text(""" SELECT * FROM users WHERE email=:email """)
         check for an existing row
+        existing = db.execute(duplicate_query, {"email": input.email}).first()
+        if existing is not None:
+            raise HTTPException(status_code=400, detail="Email already exists")
        query= text("""
            INSERT INTO users (name, email, password)
        VALUES(:name, :email, :password);
        """)
        # hashing password
        salt=bcrypt.gensalt()
-        hashedpassword=bcrypt.hashpw(input.password.encode('utf-8'), salt)
-        print(hashedpassword)
+        # store as a utf-8 string (not raw bytes)
+        hashedpassword = bcrypt.hashpw(input.password.encode('utf-8'), salt).decode('utf-8')
+        print(hashedpassword)
        # mapping data
-        data= {"name":input.name, "email":input.email, "password":hashedpassword}
+        data= {"name":input.name, "email":input.email, "password":hashedpassword}
        db.execute(query,data)
        db.commit()
        return {"Message": "User created sucessfuly", "data":{"name":input.name, "email":input.email}}
-    except Exception as e:
-        raise HTTPException(status_code=500, detail=e)
+    except Exception as e:
+        # pass a serializable message to FastAPI
+        raise HTTPException(status_code=500, detail=str(e))
if __name__=="__main__":
-     uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))
+     uvicorn.run(
+         app,
+         host=os.getenv("HOST", "127.0.0.1"),
+         port=int(os.getenv("PORT", "8000"))
+     )
# ...existing code...