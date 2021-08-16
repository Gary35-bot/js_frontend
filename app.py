import hmac
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import redirect
# class for tables


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def get_users():
    with sqlite3.connect('Sales.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[4], data[5]))
    return new_data


users = get_users()


class Tables:
    def __init__(self):
        self.cursor = self.conn.cursor()
        self.conn = sqlite3.connect('Sales.db')

    def init_user_table(self):
        print("Opened database successfully")

        self.conn.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "first_name TEXT NOT NULL,"
                          "last_name TEXT NOT NULL,"
                          "email TEXT NOT NULL,"
                          "username TEXT NOT NULL,"
                          "password TEXT NOT NULL)")
        print("user table created successfully")
        self.conn.close()
        return self.init_user_table()

    def items(self):
        print("opened db")
        self.conn.execute("CREATE TABLE IF NOT EXISTS market(id"
                          " INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "product_name TEXT NOT NULL,"
                          "description TEXT NOT NULL,"
                          "price TEXT NOT NULL)")
        print("sales table created successfully.")
        self.conn.close()
        return self.items()


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# email code
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gafrica851@gmail.com'
app.config['MAIL_PASSWORD'] = 'usqmbazpvhzbftnc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/register/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("Sales.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user("
                           "first_name,"
                           "last_name,"
                           "email,"
                           "username,"
                           "password) VALUES(?, ?, ?, ?, ?)", (first_name, last_name, email, username, password))
            conn.commit()
            response['message'] = "success"
            response["status_code"] = 201

            msg = Message('Hello Message', sender='gafrica851@gmail.com', recipients=[email])
            msg.body = "Welcome " + first_name + " Registration completed, you are ready to start shopping return to homepage :)"
            mail.send(msg)
        return response and redirect("https://bit.ly/2VUJpET")

# adding a product in database


@app.route('/add-product/', methods=["POST"])
def market_place():
    response = {}

    if request.method == "POST":

        product_name = request.form['product_name']
        description = request.form['description']
        price = request.form['price']

        with sqlite3.connect("Sales.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO market("
                           "product_name,"
                           "description,"
                           "price) VALUES(?, ?, ?)", (product_name, description, str('R') + price))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201
        return response

# route for viewing user in database


@app.route('/view-users/', methods=["GET"])
def get_user():
    response = {}
    with sqlite3.connect("Sales.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

        posts = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = posts
    return response


@app.route('/view-products/', methods=["GET"])
def get_product():
    response = {}
    with sqlite3.connect("Sales.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM market")

        posts = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = posts
    return response

# deleting route


@app.route("/delete-product/<int:product_id>")
def delete_product(product_id):
    response = {}
    with sqlite3.connect("Sales.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM market WHERE id=" + str(product_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Product deleted successfully "
    return response

# editing the product database below


@app.route('/edit-product/<int:id>', methods=["PUT"])
# @jwt_required()
def update_product(id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('Sales.db') as conn:
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("product_name") is not None:
                put_data["product_name"] = incoming_data.get("product_name")
                with sqlite3.connect("Sales.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE market SET product_name =? WHERE id=?", (put_data["product_name"], id))
                    conn.commit()
                    response["message"] = "Update was successfully"
                    response["status_code"] = 200

            if incoming_data.get("description") is not None:
                put_data["description"] = incoming_data.get("description")
                with sqlite3.connect("Sales.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE market SET description =? WHERE id=?", (put_data["description"], id))
                    conn.commit()
                    response["message"] = "description updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("price") is not None:
                put_data["price"] = incoming_data.get("price")
                with sqlite3.connect("Sales.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE market SET price =? WHERE id=?", (put_data["price"], id))
                    conn.commit()
                    response["message"] = "price updated successfully"
                    response["status_code"] = 200
    return response


if __name__ == '__main__':
    app.run()
