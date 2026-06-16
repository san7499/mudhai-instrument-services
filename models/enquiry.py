from datetime import datetime


class Enquiry:

    def __init__(
        self,
        name,
        email,
        phone,
        message,
        company="",
        interested_product="",
        status="New",
        notes=""
    ):

        self.name = name.strip()

        self.email = email.strip().lower()

        self.phone = phone.strip()

        self.company = company.strip()

        self.interested_product = interested_product.strip()

        self.message = message.strip()

        self.status = status

        self.notes = notes

        self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    # -----------------------------------
    # CONVERT TO DICTIONARY
    # -----------------------------------

    def to_dict(self):

        return {

            "name": self.name,

            "email": self.email,

            "phone": self.phone,

            "company": self.company,

            "interested_product":
            self.interested_product,

            "message": self.message,

            "status": self.status,

            "notes": self.notes,

            "created_at":
            self.created_at,

            "updated_at":
            self.updated_at
        }

    # -----------------------------------
    # UPDATE ENQUIRY
    # -----------------------------------

    @staticmethod
    def update_data(data):

        data["updated_at"] = datetime.utcnow()

        return data

    # -----------------------------------
    # AVAILABLE STATUS TYPES
    # -----------------------------------

    @staticmethod
    def statuses():

        return [
            "New",
            "Contacted",
            "Quotation Sent",
            "Negotiation",
            "Converted",
            "Closed"
        ]
