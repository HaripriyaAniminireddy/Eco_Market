from flask import Flask, render_template, request, redirect, url_for
from extensions import mongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hanimire:nJhS2FlXq9OGgyZC@ecomarket.1jbtbhh.mongodb.net/ecomarket?retryWrites=true&w=majority&appName=ecomarket"
app.secret_key = "supersecretkey"
mongo.init_app(app)

@app.route('/')
def index():
    products = list(mongo.db.products.find())
    return render_template("dashboard.html", products=products)

@app.route('/add', methods=["POST"])
def add():
    product = {
        "name": request.form["name"],
        "price": float(request.form["price"]),
        "description": request.form["description"]
    }
    mongo.db.products.insert_one(product)
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit(id):
    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    return render_template("edit.html", product=product)

@app.route('/update/<id>', methods=["POST"])
def update(id):
    mongo.db.products.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "name": request.form["name"],
            "price": float(request.form["price"]),
            "description": request.form["description"]
        }
    })
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    mongo.db.products.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)