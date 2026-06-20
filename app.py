from itertools import product
import os
from datetime import datetime
from unittest import result
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

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
cloudinary.config(

    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),

    api_key=os.getenv("CLOUDINARY_API_KEY"),

    api_secret=os.getenv("CLOUDINARY_API_SECRET"),

    secure=True

)

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
# ==========================================================
# ADMIN PRODUCTS
# ==========================================================

@app.route("/admin/products")
def admin_products():

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        products = list(
            products_collection.find().sort("created_at", -1)
        )

    except Exception as e:

        print("LOAD PRODUCTS ERROR :", e)

        products = []

    return render_template(
        "admin/products.html",
        products=products
    )


# ==========================================================
# ADD PRODUCT
# ==========================================================

@app.route("/admin/product/add", methods=["POST"])
def add_product():

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        # ==========================================
        # IMAGE UPLOAD
        # ==========================================

        image = request.files.get("product_image")

        image_url = ""
        public_id = ""

        if image and image.filename != "":

            upload_result = cloudinary.uploader.upload(

                image,

                folder="mudhai_products"

            )

            image_url = upload_result["secure_url"]

            public_id = upload_result["public_id"]

        # ==========================================
        # PRODUCT DATA
        # ==========================================

        product = {

            "name": request.form.get(
                "name",
                ""
            ).strip(),

            "category": request.form.get(
                "category",
                ""
            ).strip(),

            "image_url": image_url,

            "public_id": public_id,

            "short_description": request.form.get(
                "short_description",
                ""
            ).strip(),

            "description": request.form.get(
                "description",
                ""
            ).strip(),

            "featured": "featured" in request.form,

            "created_at": datetime.utcnow()

        }

        print("========== PRODUCT ==========")
        print(product)

        result = products_collection.insert_one(product)

        print("Inserted ID:", result.inserted_id)
        print("=============================")

        flash(
            "Product Added Successfully!",
            "success"
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        flash(
            f"Error: {str(e)}",
            "danger"
        )

    return redirect(
        url_for("admin_products")
    )
# ==========================================================
# EDIT PRODUCT
# ==========================================================

@app.route("/admin/product/edit/<id>", methods=["GET", "POST"])
def edit_product(id):

    if not is_admin():
        return redirect(url_for("admin_login"))

    obj_id = safe_object_id(id)

    if not obj_id:

        flash(
            "Invalid Product ID.",
            "danger"
        )

        return redirect(url_for("admin_products"))

    product = products_collection.find_one(
        {
            "_id": obj_id
        }
    )

    if not product:

        flash(
            "Product not found.",
            "warning"
        )

        return redirect(url_for("admin_products"))

    if request.method == "POST":

        try:

            # ==========================================
            # KEEP OLD IMAGE
            # ==========================================

            image_url = product.get(
                "image_url",
                ""
            )

            public_id = product.get(
                "public_id",
                ""
            )

            # ==========================================
            # NEW IMAGE
            # ==========================================

            image = request.files.get("product_image")

            if image and image.filename != "":

                # Delete previous Cloudinary image

                if public_id:

                    try:

                        cloudinary.uploader.destroy(
                            public_id
                        )

                    except Exception as delete_error:

                        print(
                            "DELETE OLD IMAGE ERROR :",
                            delete_error
                        )

                # Upload new image

                upload_result = cloudinary.uploader.upload(

                    image,

                    folder="mudhai_products"

                )

                image_url = upload_result["secure_url"]

                public_id = upload_result["public_id"]

            # ==========================================
            # UPDATE DATA
            # ==========================================

            updated_data = {

                "name": request.form.get(
                    "name",
                    ""
                ).strip(),

                "category": request.form.get(
                    "category",
                    ""
                ).strip(),

                "image_url": image_url,

                "public_id": public_id,

                "short_description": request.form.get(
                    "short_description",
                    ""
                ).strip(),

                "description": request.form.get(
                    "description",
                    ""
                ).strip(),

                "featured": "featured" in request.form,

                "modified_at": datetime.utcnow()

            }

            products_collection.update_one(

                {
                    "_id": obj_id
                },

                {
                    "$set": updated_data
                }

            )

            flash(
                "Product Updated Successfully!",
                "success"
            )

            return redirect(
                url_for("admin_products")
            )

        except Exception as e:

            print(
                "UPDATE PRODUCT ERROR :",
                e
            )

            flash(
                "Unable to update product.",
                "danger"
            )

    return render_template(

        "admin/edit_product.html",

        product=product

    )
# ==========================================================
# DELETE PRODUCT
# ==========================================================

@app.route("/admin/product/delete/<id>")
def delete_product(id):

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        obj_id = safe_object_id(id)

        if not obj_id:

            flash(
                "Invalid Product ID.",
                "danger"
            )

            return redirect(
                url_for("admin_products")
            )

        # ==========================================
        # FIND PRODUCT
        # ==========================================

        product = products_collection.find_one(
            {
                "_id": obj_id
            }
        )

        if not product:

            flash(
                "Product Not Found.",
                "warning"
            )

            return redirect(
                url_for("admin_products")
            )

        # ==========================================
        # DELETE IMAGE FROM CLOUDINARY
        # ==========================================

        public_id = product.get(
            "public_id"
        )

        if public_id:

            try:

                cloudinary.uploader.destroy(
                    public_id
                )

            except Exception as cloudinary_error:

                print(
                    "CLOUDINARY DELETE ERROR :",
                    cloudinary_error
                )

        # ==========================================
        # DELETE PRODUCT FROM DATABASE
        # ==========================================

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
                "Unable to delete product.",
                "warning"
            )

    except Exception as e:

        print(
            "DELETE PRODUCT ERROR :",
            e
        )

        flash(
            "Unable to delete product.",
            "danger"
        )

    return redirect(
        url_for("admin_products")
    )
# ==========================================
# ==========================================
# ADMIN BLOGS
# ==========================================

@app.route("/admin/blogs")
def admin_blogs():

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        blogs = list(
            blogs_collection.find().sort(
                "created_at",
                -1
            )
        )

    except Exception as e:

        print("BLOG FETCH ERROR :", e)

        blogs = []

        flash(
            "Unable to load blogs.",
            "danger"
        )

    return render_template(

        "admin/blogs.html",

        blogs=blogs

    )


# ==========================================
# ADD BLOG
# ==========================================

@app.route("/admin/blog/add", methods=["POST"])
def add_blog():

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        # ==========================================
        # BASIC DATA
        # ==========================================

        title = request.form.get(
            "title",
            ""
        ).strip()

        author = request.form.get(
            "author",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        excerpt = request.form.get(
            "excerpt",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        tags = request.form.get(
            "tags",
            ""
        ).strip()

        if not title or not author or not category:

            flash(
                "Please fill all required fields.",
                "warning"
            )

            return redirect(
                url_for("admin_blogs")
            )

        # ==========================================
        # CLOUDINARY IMAGE UPLOAD
        # ==========================================

        image = request.files.get(
            "blog_image"
        )

        featured_image = ""

        public_id = ""

        if image and image.filename != "":

            upload_result = cloudinary.uploader.upload(

                image,

                folder="mudhai_blogs"

            )

            featured_image = upload_result[
                "secure_url"
            ]

            public_id = upload_result[
                "public_id"
            ]
                    # ==========================================
        # BLOG DATA
        # ==========================================

        blog = {

            "title": title,

            "author": author,

            "category": category,

            "excerpt": excerpt,

            "content": content,

            "featured_image": featured_image,

            "public_id": public_id,

            "tags": [

                tag.strip()

                for tag in tags.split(",")

                if tag.strip()

            ],

            "featured": "featured" in request.form,

            "created_at": datetime.utcnow()

        }

        # ==========================================
        # SAVE BLOG
        # ==========================================

        result = blogs_collection.insert_one(
            blog
        )

        print("========== BLOG ==========")

        print(blog)

        print(
            "Inserted ID :",
            result.inserted_id
        )

        print("==========================")

        flash(

            "Blog Added Successfully!",

            "success"

        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        flash(

            f"Error : {str(e)}",

            "danger"

        )

    return redirect(

        url_for("admin_blogs")

    )
    # ==========================================
# EDIT BLOG
# ==========================================

@app.route("/admin/blog/edit/<id>", methods=["POST"])
def edit_blog(id):

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        obj_id = safe_object_id(id)

        if not obj_id:

            flash(
                "Invalid Blog ID.",
                "danger"
            )

            return redirect(
                url_for("admin_blogs")
            )

        # ==========================================
        # FIND BLOG
        # ==========================================

        blog = blogs_collection.find_one(

            {
                "_id": obj_id
            }

        )

        if not blog:

            flash(
                "Blog Not Found.",
                "warning"
            )

            return redirect(
                url_for("admin_blogs")
            )

        tags = request.form.get(
            "tags",
            ""
        ).strip()

        # ==========================================
        # KEEP OLD IMAGE
        # ==========================================

        featured_image = blog.get(
            "featured_image",
            ""
        )

        public_id = blog.get(
            "public_id",
            ""
        )

        # ==========================================
        # NEW IMAGE
        # ==========================================

        image = request.files.get(
            "blog_image"
        )

        if image and image.filename != "":

            # Delete previous Cloudinary image

            if public_id:

                try:

                    cloudinary.uploader.destroy(
                        public_id
                    )

                except Exception as delete_error:

                    print(
                        "DELETE OLD BLOG IMAGE ERROR :",
                        delete_error
                    )

            # Upload new image

            upload_result = cloudinary.uploader.upload(

                image,

                folder="mudhai_blogs"

            )

            featured_image = upload_result[
                "secure_url"
            ]

            public_id = upload_result[
                "public_id"
            ]
                    # ==========================================
        # UPDATE DATA
        # ==========================================

        updated_data = {

            "title": request.form.get(
                "title",
                ""
            ).strip(),

            "author": request.form.get(
                "author",
                ""
            ).strip(),

            "category": request.form.get(
                "category",
                ""
            ).strip(),

            "excerpt": request.form.get(
                "excerpt",
                ""
            ).strip(),

            "content": request.form.get(
                "content",
                ""
            ).strip(),

            "featured_image": featured_image,

            "public_id": public_id,

            "tags": [

                tag.strip()

                for tag in tags.split(",")

                if tag.strip()

            ],

            "featured": "featured" in request.form,

            "modified_at": datetime.utcnow()

        }

        # ==========================================
        # UPDATE BLOG
        # ==========================================

        blogs_collection.update_one(

            {
                "_id": obj_id
            },

            {
                "$set": updated_data
            }

        )

        flash(

            "Blog Updated Successfully!",

            "success"

        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        flash(

            f"Error : {str(e)}",

            "danger"

        )

    return redirect(

        url_for("admin_blogs")

    )
    # ==========================================
# DELETE BLOG
# ==========================================

@app.route("/admin/blog/delete/<id>")
def delete_blog(id):

    if not is_admin():
        return redirect(url_for("admin_login"))

    try:

        obj_id = safe_object_id(id)

        if not obj_id:

            flash(
                "Invalid Blog ID.",
                "danger"
            )

            return redirect(
                url_for("admin_blogs")
            )

        # ==========================================
        # FIND BLOG
        # ==========================================

        blog = blogs_collection.find_one(

            {
                "_id": obj_id
            }

        )

        if not blog:

            flash(
                "Blog Not Found.",
                "warning"
            )

            return redirect(
                url_for("admin_blogs")
            )

        # ==========================================
        # DELETE IMAGE FROM CLOUDINARY
        # ==========================================

        public_id = blog.get(
            "public_id"
        )

        if public_id:

            try:

                cloudinary.uploader.destroy(
                    public_id
                )

            except Exception as cloudinary_error:

                print(

                    "CLOUDINARY DELETE ERROR :",

                    cloudinary_error

                )

        # ==========================================
        # DELETE BLOG FROM DATABASE
        # ==========================================

        result = blogs_collection.delete_one(

            {
                "_id": obj_id
            }

        )

        if result.deleted_count:

            flash(

                "Blog Deleted Successfully!",

                "success"

            )

        else:

            flash(

                "Unable to delete blog.",

                "warning"

            )

    except Exception as e:

        import traceback

        traceback.print_exc()

        flash(

            f"Error : {str(e)}",

            "danger"

        )

    return redirect(

        url_for("admin_blogs")

    )
    
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