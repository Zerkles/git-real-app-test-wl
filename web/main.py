from flask import Flask,request
app = Flask(__name__)
import time
import redis
import psycopg2
import json

cache = redis.Redis(host='redis', port=6379)


@app.route("/")
def hello():
        return "Hello World!"
@app.route("/count")
def visit():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
#-------------------------------------------------------------------------------------
@app.route("/rooms", methods=['POST']) #dodawanie pokoju
def add():
    try:
        data=json.loads(request.data)
        cursor.execute("""INSERT INTO Rooms VALUES (%s,%s,%s)""", (data["id"],data["name"], data["available"]))
        connection.commit()
        return 'Succesfully added new room!'
    except (Exception, psycopg2.Error) as error :
        return ("Error PostgreSQL:", error), 406

@app.route("/rooms/<room_id>", methods=['DELETE']) #usuwanie pokoju
def delete(room_id):
    try:
        cursor.execute("DELETE from Rooms where id="+room_id)
        connection.commit()
        return 'Succesfully deleted room!'
    except (Exception, psycopg2.Error) as error :
        return ("Error PostgreSQL:", error), 406

@app.route("/rooms/<room_id>", methods=['GET']) #pobieranie pokoju o <id>
def get2(room_id):
    try:
        cursor.execute("SELECT * from Rooms where id= "+str(room_id))
        id,name,available = cursor.fetchall()[0]
        return {"id":id,"name":str(name),"available":str(available)}
    except (Exception, psycopg2.Error) as error :
        return ("Error PostgreSQL:", error), 406

@app.route("/rooms", methods=['GET']) #pobieranie wszystkich pokoi
def get():
    try:
        is_available = request.args.get('available')
        if(is_available != None and is_available == "1"):
            cursor.execute("SELECT * from Rooms where available=True")
        elif(is_available != None and is_available == "0"):
            cursor.execute("SELECT * from Rooms where available=False")
        else:
            cursor.execute("SELECT * from Rooms")

        result = cursor.fetchall()
        response=[]

        for x in result:
            id,name,available= x
            response.append({"id":id,"name":str(name),"available":str(available)})
        return {"rooms":response}
    except (Exception, psycopg2.Error) as error :
        return ("Error PostgreSQL:", error), 406

def connect_database():
    try:
        connection = psycopg2.connect(user = "admin",
            password = "admin1234",
            host = "database",
            port = "5432",
            database = "post_db")
        print('Connected with database!')
        return connection
    except (Exception, psycopg2.Error) as error :
        print ("Error PostgreSQL:", error)

if __name__ == "__main__":
    connection = connect_database()
    cursor = connection.cursor()
    app.run(host='0.0.0.0',debug=True, port=8903)

