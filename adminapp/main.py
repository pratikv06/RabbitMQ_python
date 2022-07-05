from dataclasses import dataclass
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
import requests
from flask import abort
import producer


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+pymysql://root:root@db/adminapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app) 


# Models
@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    db.UniqueConstraint(user_id, product_id, name='user_product_unique')


@app.route("/api/products/")
def index():
    return jsonify(Product.query.all())

@app.route("/api/products/<int:id>/like", methods=['POST'])
def like(id):
    # req = requests.get("http://host.docker.internal:8000/api/user")
    req = requests.get("http://172.17.0.1:8000/api/user")
    json = req.json()
    try:
        productuser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productuser)
        db.session.commit()
        producer.publish("product_liked", id)
        msg = "liked successfully"
    except:
        # abort(400, f"You `{json['id']}` already liked this product")
        db.session.rollback()
        productuser = ProductUser.query.filter_by(user_id=json['id'], product_id=id).first()
        db.session.delete(productuser)
        db.session.commit()
        producer.publish("product_unliked", id)
        msg = "unliked successfully"
    return jsonify({
        "message": msg
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')