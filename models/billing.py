from models.product import ProductModel
from db import db

class BillingHelper:
    
    def is_order_valid(products:list)-> tuple:
        '''
        To check the validity of the order
        
        Parameters:
            producs(list): List of ordered items.
        Returns:
            order_valid(bool): True, if given quantity in the orders is valid else False.
            response_list(list): A list of product dicts, each with a status(True/False). 
                                 status: True, if the order quantity of the product is less than or equals
                                 the quantity in database.
        '''
        order_valid = True
        response_list = []
        for product_dict in products:
            status=False
            prod_obj = ProductModel.query.filter_by(id=product_dict.get('id')).first()
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
            
        return order_valid, response_list

    def calculate_bill(products):
        bill_amount = 0
        res = []
        # try:
        for cart_product_dict in products:
            # sale_type:["wholesale", "retail", "custom"]
            product_sale_type = cart_product_dict.get("sale_type", "retail")
            actal_product = ProductModel.query.filter_by(id=cart_product_dict["id"]).first()
            # Calculating bill amount based on sale type for each product
            if(product_sale_type=="retail"):
                bill_amount += cart_product_dict["quantity"]*actal_product.retail_price
            elif(product_sale_type=="wholesale"):
                bill_amount += cart_product_dict["quantity"]*actal_product.wholesale_price
            elif(product_sale_type=="custom"):
                bill_amount += cart_product_dict["quantity"]*cart_product_dict.custom_price  
            # else:
            #     raise Exception("Invalid product saletype")
            # pr.quantity -= abs(prods_dict[pr.id])
            cart_product_dict["wholesale_price"] = actal_product.wholesale_price
            cart_product_dict["retail_pruce"] = actal_product.retail_price

            res.append(cart_product_dict)
        return res, bill_amount

    def update_items(products):
        '''
        Update the item quantity in db, but the ids 
        and quantities should be verified using def order_validity
        verify for:
        - uniqueness of the id
        - the received id's should be present in product table
        - verify that given qty <= available quantity
        '''
        # product_ids = [product.get('id', None) for product in products]
        prods_dict = {product['id']:product['quantity'] for product in products}
        product_ids = prods_dict.keys()

        # res = ProductModel.query.filter(ProductModel.id.in_(product_ids)).all()
                                # update({ProductModel.quantity: ProductModel.quantity-db.sql.case(prods_dict, value=ProductModel.id)})
        # Updating the quantity in the products db
        # TODO: Deduct the quantity in db, only after a valid payment.
 
        try:
            for cart_product in prods_dict:
                # sale_type:["wholesale", "retail", "custom"]
                product_sale_type = cart_product.get("sale_type", "retail")
                actal_product = ProductModel.query.filter(id=cart_product.id).first()
                if(product_sale_type=="wholesale"):
                    bill_amount += cart_product["quantity"]*actal_product.wholesale_price
                # pr.quantity -= abs(prods_dict[pr.id])
            db.session.commit()
        except Exception:
            raise Exception("")
        
        
        
        # update({'products.quantity': pr})
        return [res_.json() for res_ in res]
    


    def save_to_db():
        pass