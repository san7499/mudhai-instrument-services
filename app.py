```python
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

import os
from datetime import datetime

# --------------------------------------------------
# LOAD ENV VARIABLES
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# APP CONFIG
# --------------------------------------------------

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# --------------------------------------------------
# MONGODB CONNECTION
# --------------------------------------------------

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["mudhai_db"]

products_collection = db["products"]
blogs_collection = db["blogs"]
certifications_collection = db["certifications"]
enquiries_collection = db["enquiries"]
users_collection = db["users"]

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    featured_products = list(
        products_collection.find().limit(3)
    )

    latest_blogs = list(
        blogs_collection.find().sort(
            "created_at", -1
        ).limit(3)
    )

    return render_template(
        "home.html",
        products=featured_products,
        blogs=latest_blogs
    )

# --------------------------------------------------
# ABOUT
# --------------------------------------------------

@app.route("/about")
def about():
    return render_template("about.html")

# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

@app.route("/products")
def products():

    all_products = list(
        products_collection.find()
    )

    return render_template(
        "products.html",
        products=all_products
    )

# --------------------------------------------------
# PRODUCT DETAILS
# --------------------------------------------------

@app.route("/product/<product_id>")
def product_details(product_id):

    product = products_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    if not product:
        flash("Product not found", "danger")
        return redirect(url_for("products"))

    return render_template(
        "product_details.html",
        product=product
    )

# --------------------------------------------------
# BLOGS
# --------------------------------------------------

@app.route("/blogs")
def blogs():

    all_blogs = list(
        blogs_collection.find().sort(
            "created_at", -1
        )
    )

    return render_template(
        "blogs.html",
        blogs=all_blogs
    )

# --------------------------------------------------
# BLOG DETAILS
# --------------------------------------------------

@app.route("/blog/<blog_id>")
def blog_details(blog_id):

    blog = blogs_collection.find_one(
        {"_id": ObjectId(blog_id)}
    )

    if not blog:
        flash("Blog not found", "danger")
        return redirect(url_for("blogs"))

    return render_template(
        "blog_details.html",
        blog=blog
    )

# --------------------------------------------------
# CERTIFICATIONS
# --------------------------------------------------

@app.route("/certifications")
def certifications():

    all_certifications = list(
        certifications_collection.find()
    )

    return render_template(
        "certifications.html",
        certifications=all_certifications
    )

# --------------------------------------------------
# CONTACT
# --------------------------------------------------

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        enquiry_data = {

            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "message": request.form.get("message"),

            "status": "new",

            "created_at": datetime.utcnow()
        }

        enquiries_collection.insert_one(
            enquiry_data
        )

        flash(
            "Your enquiry has been submitted successfully.",
            "success"
        )

        return redirect(url_for("contact"))

    return render_template("contact.html")

# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        admin = users_collection.find_one(
            {
                "username": username,
                "password": password
            }
        )

        if admin:

            session["admin"] = username

            flash(
                "Login successful",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid credentials",
            "danger"
        )

    return render_template(
        "admin/login.html"
    )

# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------

@app.route("/admin/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(
            url_for("admin_login")
        )

    stats = {

        "products":
        products_collection.count_documents({}),

        "blogs":
        blogs_collection.count_documents({}),

        "certifications":
        certifications_collection.count_documents({}),

        "enquiries":
        enquiries_collection.count_documents({})
    }

    latest_enquiries = list(

        enquiries_collection.find()

        .sort("created_at", -1)

        .limit(5)
    )

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        enquiries=latest_enquiries
    )

# --------------------------------------------------
# ADMIN LOGOUT
# --------------------------------------------------

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(
        url_for("admin_login")
    )

# --------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return render_template(
        "404.html"
    ), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "500.html"
    ), 500

# --------------------------------------------------
# RUN APP
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
```
