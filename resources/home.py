from flask_restful import Resource

from flask_restful import fields, marshal_with

from models.product import ProductModel
from models.store import StoreModel


class Home(Resource):
    def get(self):
        return {"Status": "Listening"}


rf = dict()
rf['id'] = fields.Integer(attribute='pid')
rf = {
    'name': fields.String,
    'uri': fields.Url('storeproduct'),
}

resource_fields = {
    'name': fields.String,
    'products': fields.Nested(rf),
}


class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        # return ProductModel.find_by_id(1, 1, 3)
        return StoreModel.find_by_id(1,1)