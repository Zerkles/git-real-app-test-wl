from flask import Flask, request

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


@app.route("/room", methods=['POST'])
def add():
    # try:
    data = json.loads(request.data)
    name, available = "'" + str(data["name"]) + "'", data["available"]
    cursor.execute(f"""INSERT INTO Rooms (name,available) VALUES ({name} ,{available})""")
    connection.commit()
    cursor.execute(f"""SELECT MAX(id) FROM Rooms WHERE name={name} AND available={available}""")
    id = cursor.fetchall()[0][0]
    return {"id": id, "name": name, "available": available}, 201


# except (Exception) as error:
# print(error)
# return {"message": error}, 400


@app.route("/room/<room_id>", methods=['DELETE'])
def delete(room_id):
    try:
        cursor.execute(f"SELECT * from Rooms where id={room_id}")
        id, name, available = cursor.fetchall()[0]
        cursor.execute(f"DELETE from Rooms where id={room_id}")
        connection.commit()
        return {"id": id, "name": name, "available": available}
    except (Exception) as error:
        print(error)
        return {"message": error}, 400


@app.route("/room/<room_id>", methods=['GET'])
def get(room_id):
    try:
        cursor.execute(f"SELECT * from Rooms where id={room_id}")
        id, name, available = cursor.fetchall()[0]
        return {"id": id, "name": str(name), "available": str(available)}
    except (Exception) as error:
        print(error)
        return {"message": error}, 400


@app.route("/rooms", methods=['GET'])
def get2():
    try:
        is_available = request.args.get('available')
        if (is_available != None and is_available == "1"):
            cursor.execute("SELECT * from Rooms where available=True")
        elif (is_available != None and is_available == "0"):
            cursor.execute("SELECT * from Rooms where available=False")
        else:
            cursor.execute("SELECT * from Rooms")

        result = cursor.fetchall()
        response = []

        for x in result:
            id, name, available = x
            response.append({"id": id, "name": str(name), "available": str(available)})
        return {"rooms": response}
    except (Exception) as error:
        print(error)
        return {"message": error}, 400


def connect_database():
    try:
        connection = psycopg2.connect(user="admin",
                                      password="admin1234",
                                      host="database",
                                      port="5432",
                                      database="post_db")
        print('Connected with database!')
        return connection
    except (Exception) as error:
        print(error)
        return {"message": error}, 400


if __name__ == "__main__":
    connection = connect_database()
    cursor = connection.cursor()
    app.run(host='0.0.0.0', debug=True, port=8903)
