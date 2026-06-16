from datetime import datetime
import re


class Blog:

    def __init__(
        self,
        title,
        content,
        author="Mudhai Instrument Services",
        category="General",
        featured_image="",
        excerpt="",
        tags=None,
        featured=False,
        seo_title="",
        seo_description=""
    ):

        self.title = title

        self.slug = self.generate_slug(title)

        self.content = content

        self.author = author

        self.category = category

        self.featured_image = featured_image

        self.excerpt = excerpt

        self.tags = tags if tags else []

        self.featured = featured

        self.seo_title = seo_title

        self.seo_description = seo_description

        self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    # -----------------------------------
    # GENERATE SEO FRIENDLY SLUG
    # -----------------------------------

    @staticmethod
    def generate_slug(title):

        slug = title.lower()

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

            "title": self.title,

            "slug": self.slug,

            "content": self.content,

            "author": self.author,

            "category": self.category,

            "featured_image":
            self.featured_image,

            "excerpt":
            self.excerpt,

            "tags":
            self.tags,

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
    # UPDATE BLOG
    # -----------------------------------

    @staticmethod
    def update_data(data):

        data["updated_at"] = datetime.utcnow()

        return data
