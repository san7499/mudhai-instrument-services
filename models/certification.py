from datetime import datetime


class Certification:

    def __init__(
        self,
        name,
        issuing_authority,
        description="",
        logo="",
        certificate_file="",
        certificate_number="",
        issue_date=None,
        expiry_date=None,
        status="Active"
    ):

        self.name = name.strip()

        self.issuing_authority = (
            issuing_authority.strip()
        )

        self.description = description.strip()

        self.logo = logo

        self.certificate_file = certificate_file

        self.certificate_number = (
            certificate_number.strip()
        )

        self.issue_date = issue_date

        self.expiry_date = expiry_date

        self.status = status

        self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    # -----------------------------------
    # CONVERT TO DICTIONARY
    # -----------------------------------

    def to_dict(self):

        return {

            "name":
            self.name,

            "issuing_authority":
            self.issuing_authority,

            "description":
            self.description,

            "logo":
            self.logo,

            "certificate_file":
            self.certificate_file,

            "certificate_number":
            self.certificate_number,

            "issue_date":
            self.issue_date,

            "expiry_date":
            self.expiry_date,

            "status":
            self.status,

            "created_at":
            self.created_at,

            "updated_at":
            self.updated_at
        }

    # -----------------------------------
    # UPDATE CERTIFICATION
    # -----------------------------------

    @staticmethod
    def update_data(data):

        data["updated_at"] = datetime.utcnow()

        return data

    # -----------------------------------
    # STATUS OPTIONS
    # -----------------------------------

    @staticmethod
    def statuses():

        return [
            "Active",
            "Expired",
            "Pending Renewal"
        ]
