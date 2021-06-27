## Update the PUT method of PRODUCT Resource to handle individual or all or certain combination of values for getting updated.

# SEARCH USING `NOTE-THIS` or TODO to see all the places i have a doubt

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

On 
2. Consolidate the json responses in a single file from configs

## #######
## Hiccups:
## ########

# PRODUCT
- get /product/<id> - Add a measure to get only products from corresponding store
- Not able to add same product across multiple stores in products table.
 
/user
-> get /user
 - remove body, get user id from acces token
 - RESPONSE format:
-> {
    "status": true,
    "user": {
        "id": 3,
        "first_name": "naidu",
        "last_name": "aa",
        "username": "galli99",
        "mobileno": ******345,
        "email": "ke****fyi@gmail.com"
    }
}

/stores

->   GET stores/
    RESPONSE:
    {
        "status":True/False,
        "stores": []
    }
 
-> POST stores
  REQUEST DATA:
  name
  state
  district
  street
  pincode
  phone no
  email

 -> 

 /products


 /transactions

 - transaction_id
 