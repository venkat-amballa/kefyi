from flask_restful import Resource, reqparse
from flask import request

from models.billing import CustomerBill
from models.product import ProductModel

from configs.errors import errors
from constants import STATUS, SALE_TYPES

DB_INSERT_ERROR = errors["DB"]["DB_INSERTION_ERROR"]

class Billing(Resource):
    '''
    
    '''
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("customer_id", type=int, required=True, help="Customer id is required")
    parser.add_argument("store_id", type=int, required=True, help="store id is required")
    parser.add_argument("sale_type", type=str, required=True, help="Sale type is required")
    parser.add_argument("products", type=dict, required=True, help="Products cant be billed if invalid")
    
    def post(self):
        # data = Billing.parser.parse_args()
        data = request.get_json()
        # print(data)
        # TODO:
        # Each item in the producs should be unique, if required more of same item specify quantity.
       
        # customer_id check
        customer_id = data.get('customer_id', None)
        if not customer_id:
            return {"status":False, "message":"customer id cant be empty"}, 400
        
        # store id check
        store_id = data.get('store_id', None)
        if not store_id:
            return {"status":False, "message":"store id cant be empty"}, 400
        
        # products check
        products = data.get('products')
        if products is None or len(products)==0:
            return {"status":False, "message":"Invalid items in the billing"}, 400

        # sale_type check
        sale_type = data.get('sale_type', None)
        if sale_type not in SALE_TYPES:
            return {"status":False, "message":f"sale type should be one of {', '.join(SALE_TYPES)}"}, 400
        
        status = False

        order_valid, response_products, productmodel_list = BillingHelper.is_order_valid(products)
        print("order_valid", order_valid)

        # return product_items
        if order_valid: # TODO
            try:
                # TODO updating and calculating the bill. Change it not recommended
                
                # add an entry in bill
                bill_amount = BillingHelper.calculate_bill(products, sale_type)
                bill = CustomerBillModel(customer_id=customer_id, store_id=store_id, \
                                    sale_type=sale_type, status=STATUS['PENDING'], \
                                    amount = bill_amount)

                bill.products.extend(productmodel_list)
                bill.save_to_db()

                 # update quantity in db
                update_status = BillingHelper.update_items(products)
                print("update status", update_status)
                if not update_status:
                    # return DB_INSERT_ERROR["RESPONSE"], DB_INSERT_ERROR['STATUS_CODE']
                    return {"message":"cant update the quantity in db"}
                status = True
                
                return {"status":status, "bill_id":bill.id, "amount":bill_amount}, 200

            except Exception as error:
                return DB_INSERT_ERROR["RESPONSE"], DB_INSERT_ERROR['STATUS_CODE']
        
        return {"status":status, "products":response_products}, 400
        
    def put(self):
        '''
        To update the status of bill, if amount is received successfully.
        '''
        return {"status":False,  "message":"work in progrss"}

        data = request.get_json()
        bill_id = data.get('bill_id', None)
        bill_status = data.get('status', None)
        # bill of the current customer
        customer_bill = CustomerBillModel.find_by_id(bill_id)
        return_status = False
        message = "Unable to update status of bill"

        if customer_bill and bill_status:
            return_status = True
            message = "bill status updated successfully"
            # Update quantity in db
            # TODO, do this after adding price, quantity in bill_product association model.
            # update the bill status
            customer_bill.status = STATUS['SUCCESS']
            customer_bill.save_to_db()
        
        return {"status":return_status, "message":message}, 200
        

class BillingHelper:
    
    def is_order_valid(products:list)-> tuple:
        '''
        To check the validity of the order
        
        Parameters:
            producs(list): List of ordered items.
        Returns:
            order_valid(bool)       : True, if given quantity in the orders is valid else False.
            response_list(list)     : A list of product dicts, each with a status(True/False). 
                                        status: True, if the order quantity of the product is less than or equals
                                        the quantity in database.
            productmodel_list(list) : List of product models
        '''
        order_valid = True
        response_list = []
        productmodel_list = []
        for product_dict in products:
            status=False
            prod_obj = ProductModel.query.filter_by(id=product_dict.get('id')).first()
            productmodel_list.append(prod_obj)
            # TODO - Given id is not found the table
            if(prod_obj and prod_obj.quantity>=product_dict.get("quantity")):
                status = True
            # Whenever, the status is false it means the product or quantity given is invalid. 
            order_valid &= status
            item = {
                "status":status,
                "id":product_dict.get("id", None),
            }
            response_list.append(item)
            
        return order_valid, response_list, productmodel_list

    def calculate_bill(products: list, sale_type: str):
        bill_amount = 0
        # try:
        for cart_product_dict in products:
            # sale_type:["wholesale", "retail", "custom"]
            
            actual_product = ProductModel.query.filter_by(id=cart_product_dict["id"]).first()
            # Calculating bill amount based on sale type for each product
            if(sale_type == SALE_TYPES[0]):  # retail
                bill_amount += cart_product_dict["quantity"]*actual_product.retail_price
            
            elif(sale_type == SALE_TYPES[1]): # wholesale
                bill_amount += cart_product_dict["quantity"]*actual_product.wholesale_price
            
            elif(sale_type=="custom"):
                bill_amount += cart_product_dict["quantity"]*cart_product_dict.custom_price  
            # else:
            #     raise Exception("Invalid product saletype")
            # pr.quantity -= abs(prods_dict[pr.id])
            # cart_product_dict["wholesale_price"] = actual_product.wholesale_price
            # cart_product_dict["retail_pruce"] = actual_product.retail_price

            # res.append(cart_product_dict)
        return bill_amount

    def update_items(products):
        '''
        Update the item quantity in db, but the ids 
        and quantities should be verified using def order_validity
        verify for:
        - uniqueness of the id
        - the received id's should be present in product table
        - verify that given qty <= available quantity
        '''
        
        # Updating the quantity in the products db
        # TODO: Deduct the quantity in db, only after a valid payment.
 
        try:
            for cart_product in products:
                actual_product = ProductModel.find_by_id(cart_product['id'])
                actual_product.quantity -= cart_product['quantity']
                actual_product.save_to_db()
        except Exception:
            return False
        return True
    
    def update_items_with_bill(bill_id):
        # get all products and their quantities 
        customer_bill = CustomerBillModel.find_by_id(bill_id)
        return {"data":[prod.json() for prod in customer_bill.products]}