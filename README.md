## Some status codes used
    200 - success, updated resource in the body. 
    201 - created, Body data optional.
    204 - No content, No content in the body.
    
    4xx - Bad Request
    400 - Missing required field
    5xx - Issue in processing 
    503 - Database unreachable


## Callbacks to override default responses in callbacks
 - When ever there is some unexpected behaviour, the flask sends its defaut responses. But,
    incase of you want to override those. You can use these callback functions.
 [reference] https://flask-jwt-extended.readthedocs.io/en/stable/api/

    1. @jwt.expired_token_loader        -       when the token had expired, 
                                                instead of default respopnse, the decorated method response will be sent
                                                
    2. @jwt.invalid_token_loader        -       When JWT Token is invalid
    3. @jwt.unauthorized_loader         -       when there is no JWT in Authorisation header, 
                                                Default Response:
                                                {
                                                    "msg": "Missing Authorization Header"
                                                }
                                                
    4. @jwt.needs_fresh_token_loader    -       This decorator sets the callback function for returning a custom response
                                                when a valid and non-fresh token is used on an endpoint that is marked as `fresh=True`.
    5. @jwt.revoked_token_loader        -       This decorator sets the callback function for returning a custom response when a revoked token is encountered.
    6. @jwt.token_in_blocklist_loader   -       # Callback function to check if a JWT exists in a persistent db blocklist, Ex: redis, sqlite, etc


## Sites for telugu translations scraping:

* https://www.nriol.com/resources/grocery/telugu.asp

* https://haringo.com/telugu-grocery-product-names-from-english-to-telugu/

* https://pdfdrivefiles.files.wordpress.com/2020/08/kirana-products-list.pdf

[comment]: <> (API services :)

* https://api.mymemory.translated.net/get?q=red%20lentils&langpair=en|te

* https://mymemory.translated.net/doc/spec.php

