from datetime import datetime
from bson import ObjectId
import re


class Product:

    def __init__(
        self,
        name,
        category,
        short_description,
        description,
        images=None,
        specifications=None,
        featured=False,
        seo_title="",
        seo_description=""
    ):

        self.name = name
        self.slug = self.generate_slug(name)

        self.category = category

        self.short_description = short_description

        self.description = description

        self.images = images if images else []

        self.specifications = (
            specifications if specifications else {}
        )

        self.featured = featured

        self.seo_title = seo_title

        self.seo_description = seo_description

        self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    # -----------------------------------
    # GENERATE SEO FRIENDLY SLUG
    # -----------------------------------

    @staticmethod
    def generate_slug(name):

        slug = name.lower()

        slug = re.sub(
            r"[^a-z0-9\s-]",
            "",
            slug
        )

        slug = re.sub(
            r"\s+",
            "-",
            slug
        )

        return slug

    # -----------------------------------
    # CONVERT TO DICTIONARY
    # -----------------------------------

    def to_dict(self):

        return {

            "name": self.name,

            "slug": self.slug,

            "category": self.category,

            "short_description":
            self.short_description,

            "description":
            self.description,

            "images":
            self.images,

            "specifications":
            self.specifications,

            "featured":
            self.featured,

            "seo_title":
            self.seo_title,

            "seo_description":
            self.seo_description,

            "created_at":
            self.created_at,

            "updated_at":
            self.updated_at
        }

    # -----------------------------------
    # UPDATE PRODUCT
    # -----------------------------------

    @staticmethod
    def update_data(data):

        data["updated_at"] = datetime.utcnow()

        return data
