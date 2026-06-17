import os
from datetime import datetime
from dotenv import load_dotenv

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
from bson.errors import InvalidId

# ==========================================
# ENVIRONMENT
# ==========================================
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mudhai_secret_key")

# ==========================================
# MONGODB
# ==========================================
client = MongoClient(os.getenv("MONGO_URI"))
db = client["mudhai_db"]

products_collection = db["products"]
blogs_collection = db["blogs"]
certifications_collection = db["certifications"]
enquiries_collection = db["enquiries"]

# ==========================================
# HELPERS
# ==========================================
def is_admin():
    return "admin" in session

def safe_object_id(id):
    try:
        return ObjectId(id)
    except InvalidId:
        return None

# ==========================================
# HOME
# ==========================================
@app.route("/")
def home():
    products = list(products_collection.find({"featured": True}).limit(6))
    blogs = list(blogs_collection.find().sort("created_at", -1).limit(3))
    certifications = list(certifications_collection.find().limit(4))
    
    return render_template(
        "home.html",
        products=products,
        blogs=blogs,
        certifications=certifications
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
    products = list(products_collection.find().sort("created_at", -1))
    return render_template("products.html", products=products)

@app.route("/product/<product_id>")
def product_details(product_id):
    obj_id = safe_object_id(product_id)
    if not obj_id:
        flash("Invalid Product", "danger")
        return redirect(url_for("products"))

    product = products_collection.find_one({"_id": obj_id})
    if not product:
        flash("Product Not Found", "danger")
        return redirect(url_for("products"))

    related_products = list(
        products_collection.find({
            "category": product.get("category"),
            "_id": {"$ne": product["_id"]}
        }).limit(3)
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
    blogs = list(blogs_collection.find().sort("created_at", -1))
    return render_template("blogs.html", blogs=blogs)

@app.route("/blog/<blog_id>")
def blog_details(blog_id):
    obj_id = safe_object_id(blog_id)
    if not obj_id:
        flash("Invalid Blog", "danger")
        return redirect(url_for("blogs"))

    blog = blogs_collection.find_one({"_id": obj_id})
    if not blog:
        flash("Blog Not Found", "danger")
        return redirect(url_for("blogs"))

    related_blogs = list(
        blogs_collection.find({
            "category": blog.get("category"),
            "_id": {"$ne": blog["_id"]}
        }).limit(3)
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
    certifications = list(certifications_collection.find().sort("created_at", -1))
    return render_template("certifications.html", certifications=certifications)

# ==========================================
# CONTACT
# ==========================================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        enquiry = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "company": request.form.get("company"),
            "interested_product": request.form.get("interested_product"),
            "message": request.form.get("message"),
            "status": "New",
            "created_at": datetime.utcnow()
        }
        enquiries_collection.insert_one(enquiry)
        flash("Enquiry Submitted Successfully", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# ==========================================
# ADMIN LOGIN
# ==========================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session["admin"] = username
            flash("Login Successful", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid Credentials", "danger")

    return render_template("admin/login.html")

# ==========================================
# ADMIN LOGOUT
# ==========================================
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logged Out Successfully", "success")
    return redirect(url_for("admin_login"))

# ==========================================
# ADMIN DASHBOARD
# ==========================================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not is_admin():
        return redirect(url_for("admin_login"))

    stats = {
        "products": products_collection.count_documents({}),
        "blogs": blogs_collection.count_documents({}),
        "certifications": certifications_collection.count_documents({}),
        "enquiries": enquiries_collection.count_documents({})
    }

    enquiries = list(enquiries_collection.find().sort("created_at", -1).limit(10))

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        enquiries=enquiries
    )

# ==========================================
# ==========================================
# ADMIN PRODUCTS
# ==========================================

@app.route("/admin/products")
def admin_products():
    if not is_admin():
        return redirect(url_for("admin_login"))

    products = list(
        products_collection.find().sort("created_at", -1)
    )

    return render_template(
        "admin/products.html",
        products=products
    )


@app.route("/admin/product/add", methods=["POST"])
def add_product():
    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        product = {

            "name": request.form.get("name", "").strip(),

            "category": request.form.get("category", "").strip(),

            "image_url": request.form.get("image_url", "").strip(),

            "short_description": request.form.get(
                "short_description", ""
            ).strip(),

            "description": request.form.get(
                "description", ""
            ).strip(),

            "featured": "featured" in request.form,

            "created_at": datetime.utcnow()

        }

        products_collection.insert_one(product)

        flash(
            "Product Added Successfully!",
            "success"
        )

    except Exception as e:

        print("ADD PRODUCT ERROR :", e)

        flash(
            "Unable to add product.",
            "danger"
        )

    return redirect(url_for("admin_products"))


@app.route("/admin/product/delete/<id>")
def delete_product(id):

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        obj_id = safe_object_id(id)

        if obj_id:

            result = products_collection.delete_one(
                {
                    "_id": obj_id
                }
            )

            if result.deleted_count:

                flash(
                    "Product Deleted Successfully!",
                    "success"
                )

            else:

                flash(
                    "Product not found.",
                    "warning"
                )

        else:

            flash(
                "Invalid Product ID.",
                "danger"
            )

    except Exception as e:

        print("DELETE PRODUCT ERROR :", e)

        flash(
            "Unable to delete product.",
            "danger"
        )

    return redirect(url_for("admin_products"))
# ==========================================
# ADMIN BLOGS
# ==========================================
@app.route("/admin/blogs")
def admin_blogs():
    if not is_admin():
        return redirect(url_for("admin_login"))

    blogs = list(blogs_collection.find().sort("created_at", -1))
    return render_template("admin/blogs.html", blogs=blogs)

@app.route("/admin/blog/add", methods=["POST"])
def add_blog():
    if not is_admin():
        return redirect(url_for("admin_login"))

    tags = request.form.get("tags", "")
    blogs_collection.insert_one({
        "title": request.form.get("title"),
        "author": request.form.get("author"),
        "category": request.form.get("category"),
        "excerpt": request.form.get("excerpt"),
        "content": request.form.get("content"),
        "featured_image": request.form.get("featured_image"),
        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        "featured": bool(request.form.get("featured")),
        "created_at": datetime.utcnow()
    })

    flash("Blog Added Successfully", "success")
    return redirect(url_for("admin_blogs"))

@app.route("/admin/blog/delete/<id>")
def delete_blog(id):
    if not is_admin():
        return redirect(url_for("admin_login"))

    obj_id = safe_object_id(id)
    if obj_id:
        blogs_collection.delete_one({"_id": obj_id})
        flash("Blog Deleted", "success")

    return redirect(url_for("admin_blogs"))

# ==========================================
# ADMIN CERTIFICATIONS
# ==========================================
@app.route("/admin/certifications")
def admin_certifications():
    if not is_admin():
        return redirect(url_for("admin_login"))

    certifications = list(certifications_collection.find().sort("created_at", -1))
    return render_template("admin/certifications.html", certifications=certifications)

@app.route("/admin/certification/add", methods=["POST"])
def add_certification():
    if not is_admin():
        return redirect(url_for("admin_login"))

    certifications_collection.insert_one({
        "name": request.form.get("name"),
        "description": request.form.get("description"),
        "status": request.form.get("status", "Active"),
        "created_at": datetime.utcnow()
    })

    flash("Certification Added", "success")
    return redirect(url_for("admin_certifications"))

@app.route("/admin/certification/delete/<id>")
def delete_certification(id):
    if not is_admin():
        return redirect(url_for("admin_login"))

    obj_id = safe_object_id(id)
    if obj_id:
        certifications_collection.delete_one({"_id": obj_id})
        flash("Certification Deleted", "success")

    return redirect(url_for("admin_certifications"))

# ==========================================
# ADMIN ENQUIRIES
# ==========================================
@app.route("/admin/enquiries")
def admin_enquiries():
    if not is_admin():
        return redirect(url_for("admin_login"))

    enquiries = list(enquiries_collection.find().sort("created_at", -1))
    return render_template("admin/enquiries.html", enquiries=enquiries)

@app.route("/admin/enquiry/update/<id>", methods=["POST"])
def update_enquiry(id):
    if not is_admin():
        return redirect(url_for("admin_login"))

    obj_id = safe_object_id(id)
    if obj_id:
        enquiries_collection.update_one(
            {"_id": obj_id},
            {"$set": {"status": request.form.get("status")}}
        )
        flash("Enquiry Updated", "success")

    return redirect(url_for("admin_enquiries"))

@app.route("/admin/enquiry/delete/<id>")
def delete_enquiry(id):
    if not is_admin():
        return redirect(url_for("admin_login"))

    obj_id = safe_object_id(id)
    if obj_id:
        enquiries_collection.delete_one({"_id": obj_id})
        flash("Enquiry Deleted", "success")

    return redirect(url_for("admin_enquiries"))

# ==========================================
# ERROR HANDLERS
# ==========================================
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500

# ==========================================
# CONTEXT PROCESSOR
# ==========================================
@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year,
        "is_admin": "admin" in session
    }

# ==========================================
# HEALTH CHECK
# ==========================================
@app.route("/health")
def health():
    return {
        "status": "ok",
        "database": "connected"
    }

# ==========================================
# RUN APPLICATION
# ==========================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )