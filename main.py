import os
import sqlalchemy
from flask import Flask
from sqlalchemy.dialects import postgresql

app = Flask(__name__)

def postgres_connect() -> sqlalchemy.engine.base.Engine:
    db_host = '10.21.0.3'  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = 'postgres'  # e.g. 'my-db-user'
    db_pass = '123456'   # e.g. 'my-db-password'
    db_name =  'my-db'# e.g. 'my-database'
    db_port = 5432 # e.g. 1433

    db = sqlalchemy.create_engine(
        # Equivalent URL:
        # mssql+pytds://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            database=db_name,
            host=db_host,
            port=db_port,
      ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    ) 
    return db  

@app.route("/")
def querydabase():
    db =postgres_connect()
    try:
        with db.connect() as conn:
            response = conn.execute("SELECT * FROM example").fetchall()

    except Exception as e:
            print(e)
            return 'Error: {}'.format(str(e))
    
    data = []
    for row in response:
         data.append(row)
    print(data)

    return str(data)  





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

#Using pycopg2
# import psycopg2
# import os
# from flask import Flask
# from psycopg2 import sql


# app = Flask(__name__)

# db_host = "10.21.0.3"
# db_name = "guestbook"
# db_user = "postgres"
# db_password = "123456"

# def connect_to_db():
#     conn = psycopg2.connect(
#         dbname=db_name,
#         user=db_user,
#         password=db_password,
#         host=db_host
#     )
#     return conn

# @app.route("/")
# def querydabase():
#     conn = None
#     # Connect to the PostgreSQL server
#     conn = connect_to_db()  # Change this line
#     print('connection stablished')
#     # Create a new cursor
#     cur = conn.cursor()
#     query = sql.SQL("SELECT * FROM entries")
#     cur.execute(query)
#     conn.commit()
#     print(cur.fetchone())
#         # Close communication with the server

#     return str(cur.fetchone())

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
