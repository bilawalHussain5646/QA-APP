import sqlite3

connection = sqlite3.connect('qa_app.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS users(
    email VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    phone VARCHAR(50),
    street VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    zipCode VARCHAR(50),
    timeDetails VARCHAR(50),
    natureOfTime VARCHAR(50)

  );"""


)
# cursor.execute(
#     """
#   DROP TABLE users;"""


# )


cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS office(
    sno INTEGER PRIMARY KEY AUTOINCREMENT,
    days VARCHAR(50),
    beginTime VARCHAR(50),
    endTime VARCHAR(50),
    email VARCHAR(50)

  );"""


)

cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS syllabus (
    sno INTEGER PRIMARY KEY AUTOINCREMENT,
    course VARCHAR(50),
    section VARCHAR(50),
    courseFile VARCHAR(100),
    email VARCHAR(50)

  );"""


)


# cursor.execute(
#     """
#   DROP TABLE syllabus;"""


# )
# cursor.execute(
#     """
#   DROP TABLE office;"""


# )
