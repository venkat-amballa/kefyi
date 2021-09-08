### Update the PUT method of PRODUCT Resource to handle individual or all or certain combination of values for getting updated.

# SEARCH USING `NOTE-THIS` or `TODO` to see all the places i have a doubt

1. convert the current product to master_product
2. create a partner, and a store for him.
3. save product id from master_prod to store_products


VERSIONING OF API
ENV CONFIGURATION 
HOSTING

* stores:
    Resources:
        - post methond -> is store name the only option to compare whether it's' present ?
        - Model is completed partially..!
        - Resoruce is under progress...!

* /search - to find similar products

users:
username in users
role (kefyi_user / Partner_user), access (R/W/X)

global_store - future
Dashboard for creating stores - configure (stores / products / ) - Future

product table (Update/Delete only admin)
- id
- name
- description
- category
- brand_name (Aachi, Ashirvadh, Tata Salt, Cadbury, Hindustan)
- created_by Kefyi Employee id / 
- created_at Time
- updated_by Kefyi Employee
- updated_at Time
- public # if True, every one can access the name while adding their inventory.
- units (req/not) [jar/packet/pieces/kilgrams] (or) can it be excluded with price.

- variants [1kg, 2kg, 3kg, 5kg, .....] (where in master / specific users)

Store
- id
- name
- owner
- location

store_products
- store_id
- product_id
- price
- quantity

Partners:
- id
- name
- username
- password
- status


BUG FIXES
1. User Resource:
    - Deleting the user without proper confirmation
    - Giving details of the user in get method without proper authentication

## #######
## Hiccups:
## ########

# PRODUCT
- get /product/<id> - Add a measure to get only products from corresponding store
- Not able to add same product across multiple stores in products table.
- updated_on time is not getting updated whenever a product data is updated

# Order
- while changing status of the bill, add athorisation so that one cannot change other bill id.
- when ever we are updating a product data, the product info in all the orders before
     this change, is also getting  changed. 
    Solution:
    -- If no extra data is to be saved in the association table, use db.Table else model
    [link] https://stackoverflow.com/questions/56388707/sqlalchemy-many-to-many-relationship-updating-association-object-with-extra-colu    
- did not handle custom prices while calculating bill and adding the price to Association table created above.

# stores
- anyone can request content of a particular store. Add authorisation check while requesting store data. i.e, only allow the actual user(owner) to access the stores
- one cant add same product in other store

# Commom to both products and stores
- return store products when hitting products api (optional)

/stores

-> POST stores
  REQUEST DATA:
  name
  state
  district
  street
  pincode
  phone no
  email


api.add_resource(Test, "/stores/<int:s_id>/product/<int:p_id")

# DEV
DATABASE_DEV_URL=postgresql://postgres:postgres@localhost:5432/kefyi

# STAGE
set DATABASE_STAGE_URL=postgres://bangfcwl:g2LeY0rRYdSougo5S6YBUvNqevu2c3E3@dumbo.db.elephantsql.com/bangfcwl

# PROD
set DATABASE_URL=postgres://bkfsjolrjonwbh:b14284e4edf8faad5ca9d9692ee5efb2f2a0ddef72ecc9f48ae808b0b842140a@ec2-176-34-105-15.eu-west-1.compute.amazonaws.com:5432/d9oie576iqt1es

postgres://user:password@host:port/database


Breaking Changes:
- POST /customer/register => POST /customer 

1. customer search endpoint:
   - /customer?id=<id>&mobile=<mobile>
	