from models.product import ProductModel
from configs.constants import SALE_STATUS_CODE, SALE_TYPES


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
                        "ordered_price": product.get("custom_price", None),
                        "orig_product_obj": product_obj,
                    }
                )
        except Exception as error:
            print(error)
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
            product_invalid_msg = "No such product exist in your store"
            quantity_invalid_msg = "Quantity requested is not available"
            price_invalid_msg = "Price mentioned is invalid"

            if prod_obj and prod_obj.quantity >= quantity and \
                    (prod_dict["ordered_price"] is None or prod_dict["ordered_price"] > 0):
                status = True
                item = {"status": status, "id": prod_obj.pid}
            else:
                item = {
                    "status": status,
                    "id": self.order_items[_i].get("id"),
                }
                if prod_obj is None:
                    item["message"]: product_invalid_msg
                elif prod_dict.get("ordered_price") <= 0:
                    item["message"] = price_invalid_msg
                else:
                    item["message"] = quantity_invalid_msg

            # Whenever, the status is false it means the product or quantity given is invalid.
            order_valid &= status

            response_list.append(item)
        self.is_valid = order_valid

        return order_valid, response_list

    def calculate_order_amount(self, sale_type: str) -> tuple:
        order_amount_ = 0
        # try:
        order_list = []
        billing_price_per_unit = None
        order_amount=0
        try:
            for _dict_obj in self.actual_products_list:
                # sale_type:["wholesale", "retail", "custom"]
                actual_product = _dict_obj["orig_product_obj"]
                ordered_quantity = _dict_obj["ordered_quantity"]
                ordered_price = _dict_obj["ordered_price"]
                # Calculating order amount based on sale type for each product

                # if ordered_price or sale_type == SALE_TYPES[2]:  # custom
                #     raise Exception("handle custom price")
                #     order_amount += (
                #             ordered_quantity * ordered_price
                #     )  # TODO - custom price, not implemented
                #     billing_price = ordered_price
                # el
                if sale_type == SALE_TYPES[0]:  # retail
                    if ordered_price:
                        order_amount_ = ordered_quantity * ordered_price
                        billing_price_per_unit = ordered_price
                    else:
                        order_amount_ = ordered_quantity * actual_product.retail_price
                        billing_price_per_unit = actual_product.retail_price

                elif sale_type == SALE_TYPES[1]:  # wholesale
                    if ordered_price:
                        order_amount_ = ordered_quantity * ordered_price
                        billing_price_per_unit = ordered_price
                    else:
                        order_amount_ = ordered_quantity * actual_product.wholesale_price
                        billing_price_per_unit = actual_product.wholesale_price
                order_amount += order_amount_
                order_list.append(
                    {
                        "id": actual_product.pid,
                        "price": order_amount_,
                        "unit_price": billing_price_per_unit,
                        "product": actual_product,
                        "quantity": ordered_quantity,
                    }
                )
        except Exception as e:
            print(e)
            raise Exception("cant calculate bill for the order, calculate_order_amount")

        print("amount calculated")
        return order_amount, order_list

    @staticmethod
    def update_inventory(order):
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
        order_products = order.products
        try:
            for order_obj in order_products:
                actual_product = order_obj.product
                actual_product.quantity -= order_obj.quantity

                actual_product.save_to_db()
            return True
        except Exception as e:
            print(e)
        return False
