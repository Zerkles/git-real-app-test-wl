from flask import Flask, request
import json
import logging
import re
import psycopg2
import redis
import time
import os

app = Flask(__name__)

cache = redis.Redis(host="redis", port=6379)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/count")
def visit():
    count = get_hit_count()
    return "Hello World! I have been seen {} times.\n".format(count)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/room", methods=["POST"])
def post():
    try:
        connection.reset()
        data = json.loads(request.data)
        name, available = "'" + data["name"] + "'", "'" + data["available"] + "'"
        check_for_special_characters(data["name"])
        query = f"""INSERT INTO Rooms (name,available) VALUES ({name}, {bool(available)})"""
        logging.info("POST_QUERY: " + query)
        cursor.execute(query)
        connection.commit()
        cursor.execute(
            f"""SELECT MAX(id) AS id,name,available FROM Rooms 
            WHERE name={name} AND available={available} GROUP BY name, available"""
        )
        id2, name2, available2 = cursor.fetchall()[0]
        return {"id": id2, "name": name2, "available": str(available2)}, 201
    except Exception as error:
        if 'query' in locals():
            logging.info("POST_QUERY: " + query)
        logging.error(error)
        return {"message": str(error)}, 400


@app.route("/room/<room_id>", methods=["DELETE"])
def delete(room_id):
    try:
        connection.reset()
        cursor.execute(f"SELECT * from Rooms where id={int(room_id)}")
        id, name, available = cursor.fetchall()[0]
        query = f"DELETE from Rooms where id={int(room_id)}"
        cursor.execute(query)
        connection.commit()
        return {"id": id, "name": name, "available": available}
    except Exception as error:
        if 'query' in locals():
            logging.info("DELETE_QUERY: " + query)
        logging.error(error)
        return {"message": str(error)}, 400


@app.route("/room/<room_id>", methods=["GET"])
def get(room_id):
    try:
        connection.reset()
        query = f"SELECT * from Rooms where id={int(room_id)}"
        cursor.execute(query)
        id, name, available = cursor.fetchall()[0]
        return {"id": id, "name": str(name), "available": str(available)}
    except Exception as error:
        if 'query' in locals():
            logging.info("GET_QUERY: " + query)
        logging.error(error)
        return {"message": str(error)}, 400


@app.route("/rooms", methods=["GET"])
def get2():
    try:
        connection.reset()
        is_available = request.args.get("available")
        if is_available is not None:
            if string_to_bool(is_available):
                cursor.execute("SELECT * from Rooms where available=True")
            else:
                cursor.execute("SELECT * from Rooms where available=False")
        else:
            cursor.execute("SELECT * from Rooms")

        response = []

        for x in cursor.fetchall():
            id, name, available = x
            response.append({"id": id, "name": name, "available": str(available)})
        return {"rooms": response}
    except Exception as error:
        logging.error(error)
        return {"message": str(error)}, 400


def check_for_special_characters(string):
    regex = re.compile('[,@_!#$%^&*()<>?/;.|}{~:]')
    if regex.search(string) is not None:
        raise ValueError(f"Variable contains special characters!: {string}")


def string_to_bool(string):
    if string in ["True", "true", "1"]:
        return True
    return False


def connect_database():
    try:
        connection = psycopg2.connect(
            user=str(os.environ.get("DB_USER")),
            password=str(os.environ.get("DB_PASSWORD")),
            host=str(os.environ.get("DB_HOST")),
            port=str(os.environ.get("DB_PORT")),
            database=str(os.environ.get("DB_NAME")),
        )
        logging.info("Connected with database!")
        return connection
    except Exception as error:
        logging.error(error)
        return {"message": str(error)}, 400


if __name__ == "__main__":
    try:
        connection = connect_database()
        cursor = connection.cursor()
    except Exception as error:
        logging.error(error)
    app.run(
        host=os.environ.get("HOST"),
        debug=string_to_bool(os.environ.get("DEBUG")),
        port=os.environ.get("WEB_PORT"),
    )
