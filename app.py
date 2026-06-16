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
from datetime import datetime
from dotenv import load_dotenv

import os

# ==========================================
# ENVIRONMENT
# ==========================================

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "mudhai_secret_key"
)

# ==========================================
# MONGODB
# ==========================================

client = MongoClient(
    os.getenv("MONGO_URI")
)

db = client["mudhai_db"]

products_collection = db["products"]
blogs_collection = db["blogs"]
certifications_collection = db["certifications"]
enquiries_collection = db["enquiries"]

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    products = list(
        products_collection.find(
            {"featured": True}
        ).limit(6)
    )

    blogs = list(
        blogs_collection.find()
        .sort("created_at", -1)
        .limit(3)
    )

    return render_template(
        "home.html",
        products=products,
        blogs=blogs
    )

# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")

# ==========================================
# PRODUCTS
# ==========================================

@app.route("/products")
def products():

    products = list(
        products_collection.find()
    )

    return render_template(
        "products.html",
        products=products
    )

@app.route("/product/<product_id>")
def product_details(product_id):

    product = products_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    if not product:
        return redirect(
            url_for("products")
        )

    related_products = list(

        products_collection.find(
            {
                "category":
                product["category"],

                "_id":
                {
                    "$ne":
                    product["_id"]
                }
            }
        ).limit(3)

    )

    return render_template(
        "product_details.html",
        product=product,
        related_products=related_products
    )

# ==========================================
# BLOGS
# ==========================================

@app.route("/blogs")
def blogs():

    blogs = list(
        blogs_collection.find()
        .sort("created_at", -1)
    )

    return render_template(
        "blogs.html",
        blogs=blogs
    )

@app.route("/blog/<blog_id>")
def blog_details(blog_id):

    blog = blogs_collection.find_one(
        {"_id": ObjectId(blog_id)}
    )

    if not blog:
        return redirect(
            url_for("blogs")
        )

    related_blogs = list(

        blogs_collection.find(
            {
                "category":
                blog["category"],

                "_id":
                {
                    "$ne":
                    blog["_id"]
                }
            }
        ).limit(3)

    )

    return render_template(
        "blog_details.html",
        blog=blog,
        related_blogs=related_blogs
    )

# ==========================================
# CERTIFICATIONS
# ==========================================

@app.route("/certifications")
def certifications():

    certifications = list(
        certifications_collection.find()
    )

    return render_template(
        "certifications.html",
        certifications=certifications
    )

# ==========================================
# CONTACT
# ==========================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":

        enquiry = {

            "name":
            request.form.get("name"),

            "email":
            request.form.get("email"),

            "phone":
            request.form.get("phone"),

            "company":
            request.form.get("company"),

            "interested_product":
            request.form.get(
                "interested_product"
            ),

            "message":
            request.form.get(
                "message"
            ),

            "status":
            "New",

            "created_at":
            datetime.utcnow()
        }

        enquiries_collection.insert_one(
            enquiry
        )

        flash(
            "Enquiry submitted successfully!",
            "success"
        )

        return redirect(
            url_for("contact")
        )

    return render_template(
        "contact.html"
    )

# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        if (
            username ==
            os.getenv("ADMIN_USERNAME")

            and

            password ==
            os.getenv("ADMIN_PASSWORD")
        ):

            session["admin"] = username

            return redirect(
                url_for(
                    "admin_dashboard"
                )
            )

        flash(
            "Invalid Credentials",
            "danger"
        )

    return render_template(
        "admin/login.html"
    )

# ==========================================
# LOGOUT
# ==========================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )

# ==========================================
# DASHBOARD
# ==========================================

@app.route("/admin/dashboard")
def admin_dashboard():

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

    enquiries = list(
        enquiries_collection.find()
        .sort("created_at", -1)
        .limit(10)
    )

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        enquiries=enquiries
    )

# ==========================================
# ADMIN PRODUCTS
# ==========================================

@app.route("/admin/products")
def admin_products():

    if "admin" not in session:
        return redirect(
            url_for("admin_login")
        )

    products = list(
        products_collection.find()
    )

    return render_template(
        "admin/products.html",
        products=products
    )

@app.route(
    "/admin/product/add",
    methods=["POST"]
)
def add_product():

    products_collection.insert_one({

        "name":
        request.form.get("name"),

        "category":
        request.form.get("category"),

        "short_description":
        request.form.get(
            "short_description"
        ),

        "description":
        request.form.get(
            "description"
        ),

        "featured":
        bool(
            request.form.get(
                "featured"
            )
        ),

        "created_at":
        datetime.utcnow()
    })

    flash(
        "Product Added",
        "success"
    )

    return redirect(
        url_for("admin_products")
    )

@app.route(
    "/admin/product/delete/<id>"
)
def delete_product(id):

    products_collection.delete_one(
        {
            "_id":
            ObjectId(id)
        }
    )

    return redirect(
        url_for("admin_products")
    )

# ==========================================
# ADMIN BLOGS
# ==========================================

@app.route("/admin/blogs")
def admin_blogs():

    if "admin" not in session:
        return redirect(
            url_for("admin_login")
        )

    blogs = list(
        blogs_collection.find()
    )

    return render_template(
        "admin/blogs.html",
        blogs=blogs
    )

@app.route(
    "/admin/blog/add",
    methods=["POST"]
)
def add_blog():

    tags = request.form.get(
        "tags",
        ""
    )

    blogs_collection.insert_one({

        "title":
        request.form.get("title"),

        "author":
        request.form.get("author"),

        "category":
        request.form.get("category"),

        "excerpt":
        request.form.get("excerpt"),

        "content":
        request.form.get("content"),

        "tags":
        [
            tag.strip()
            for tag in tags.split(",")
        ],

        "featured":
        bool(
            request.form.get(
                "featured"
            )
        ),

        "created_at":
        datetime.utcnow()
    })

    return redirect(
        url_for("admin_blogs")
    )

@app.route(
    "/admin/blog/delete/<id>"
)
def delete_blog(id):

    blogs_collection.delete_one(
        {
            "_id":
            ObjectId(id)
        }
    )

    return redirect(
        url_for("admin_blogs")
    )

# ==========================================
# ADMIN ENQUIRIES
# ==========================================

@app.route("/admin/enquiries")
def admin_enquiries():

    if "admin" not in session:
        return redirect(
            url_for("admin_login")
        )

    enquiries = list(

        enquiries_collection.find()
        .sort("created_at", -1)

    )

    return render_template(
        "admin/enquiries.html",
        enquiries=enquiries
    )

@app.route(
    "/admin/enquiry/update/<id>",
    methods=["POST"]
)
def update_enquiry(id):

    enquiries_collection.update_one(

        {
            "_id":
            ObjectId(id)
        },

        {
            "$set": {

                "status":
                request.form.get(
                    "status"
                )

            }
        }
    )

    return redirect(
        url_for("admin_enquiries")
    )

@app.route(
    "/admin/enquiry/delete/<id>"
)
def delete_enquiry(id):

    enquiries_collection.delete_one(
        {
            "_id":
            ObjectId(id)
        }
    )

    return redirect(
        url_for("admin_enquiries")
    )

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404

@app.errorhandler(500)
def server_error(error):

    return render_template(
        "500.html"
    ), 500

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )