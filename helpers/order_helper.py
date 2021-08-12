from models.product import ProductModel
from configs.constants import STATUS_CODE, SALE_TYPES


class OrderHelper:
    def __init__(self, order_items, user_id, store_id):
        self.order_items = order_items
        self.is_valid = False
        self.actual_products_list = list()
        self.user_id = user_id
        self.store_id = store_id
        try:

            for product in self.order_items:
                product_obj = ProductModel.find_by_id(
                    user_id, store_id, product.get("id")
                )
                # TODO - for `custom` saletype add the custom price aswell for the  below obj.
                self.actual_products_list.append(
                    {
                        "ordered_quantity": product.get("quantity"),
                        "orig_product_obj": product_obj,
                    }
                )
        except Exception as error:
            raise Exception(
                "DB_Error while accessing Product Model from `OrderHelper` init"
            )

    def is_order_valid(self) -> tuple:
        """
        To check the validity of the order, by comparing the ordered quantity with available quantity
        Parameters:
            products(list): List of ordered items.
        Returns:
            order_valid(bool)       : True, if given quantity in the orders is valid else False.
            response_list(list)     : A list of product dicts, each with a status(True/False).
                                        status: True, if the order quantity of the product is less than or equals
                                        the quantity in database.
        """
        order_valid = True
        response_list = []
        for _i, prod_dict in enumerate(self.actual_products_list):
            status = False
            prod_obj = prod_dict["orig_product_obj"]
            quantity = prod_dict["ordered_quantity"]
            # TODO -    Given id is not found the table
            # DONE -    below => it will be saved as none in self.actual_products_list,
            #           based on that we send a message
            if prod_obj and prod_obj.quantity >= quantity:
                status = True
                item = {"status": status, "id": prod_obj.id}
            else:
                item = {
                    "status": status,
                    "id": self.order_items[_i].get("id"),
                    "message": "Quantity requested is not available",
                }
                if prod_obj is None:
                    item["message"] = "No such item exist in your store"

            # Whenever, the status is false it means the product or quantity given is invalid.
            order_valid &= status

            response_list.append(item)
        self.is_valid = order_valid

        return order_valid, response_list

    def calculate_order_amount(self, sale_type: str) -> tuple:
        order_amount = 0
        # try:
        order_list = []
        billing_price = None
        try:
            for _dict_obj in self.actual_products_list:
                # sale_type:["wholesale", "retail", "custom"]
                actual_product = _dict_obj["orig_product_obj"]
                ordered_quantity = _dict_obj["ordered_quantity"]
                # Calculating order amount based on sale type for each product
                if sale_type == SALE_TYPES[0]:  # retail
                    order_amount += ordered_quantity * actual_product.retail_price
                    billing_price = actual_product.retail_price

                elif sale_type == SALE_TYPES[1]:  # wholesale
                    order_amount += ordered_quantity * actual_product.wholesale_price
                    billing_price = actual_product.wholesale_price

                elif sale_type == SALE_TYPES[2]:  # custom
                    order_amount += (
                            ordered_quantity * _dict_obj.custom_price
                    )  # TODO - custom price, not implemented
                    billing_price = actual_product.custom_price

                order_list.append(
                    {
                        "price": billing_price,
                        "product": actual_product,
                        "quantity": ordered_quantity,
                    }
                )
        except Exception as e:
            raise Exception("cant calculate bill for the order, calculate_order_amount")

        print("amount calculated")
        return order_amount, order_list

    def update_items(self):
        """
        Update the item quantity in db, but the ids
        and quantities should be verified using def order_validity
        verify for:
        - uniqueness of the id
        - the received id's should be present in product table
        - verify that given qty <= available quantity
        """

        # Updating the quantity in the products db
        # TODO: Deduct the quantity in db, only after a valid payment.

        try:
            for order_obj in self.actual_products_list:
                actual_product = order_obj.get("orig_product_obj", None)
                actual_product.quantity -= order_obj.get("ordered_quantity", None)

                actual_product.save_to_db()
            return True
        except Exception:
            raise Exception(
                "Cant update the quantity ordered in the db, in def update_items"
            )
        return False
