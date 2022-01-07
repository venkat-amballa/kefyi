from flask_restful import Resource


class Units(Resource):
    def get(self):
        units = [
            "gm",
            "grams",
            "ml",
            "milli-liters",
            "kg",
            "kilogram",
            "pieces",
            "piece",
            "set",
            "sets"
            "coils",
            "liter",
            "case",
            "rupees",
            "cups",
            "pouch",
            "bundle",
            "packet",
            "bags",
            "medium",
            "big",
            "small",
            "box",
        ]
        return {"units": units}, 200
