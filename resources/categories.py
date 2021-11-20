from flask_restful import Resource, reqparse
from flask import request


class Categories(Resource):
    def get(self):
        categories = [
            "sweets",
            "dals",
            "ravva",
            "flours(pindi)",
            "staples",
            "masalalu",
            "oils",
            "dry fruits",
            "dairy",
            "beverages",
            "snacks & branded foods",
            "home care",
            "personal care",
            "baby care",
            "millets/చిరు ధాన్యాలు",
            "puja items",
            "animal feeds",
            "disposables items",
            "aquaculture",
        ]

        return {"categories": categories}, 200
