###REGISTER_END_POINT <br />

METHOD : POST <br />

localhost:5000/register <br />

Request body <br />
 username <br />
 email <br />
 password <br />
 user_id <br />
 is_admin <br />
 is_seller <br />
 
Sample request <br />
{"username":"anshu_seller", "email":"anshu_seller@gmail.com", "password":"asdfghjkl", "user_id":"3", "is_admin":false, "is_seller":true} <br />

Response Param <br />
{ <br />
  "status": true <br />
} <br />

###LOGIN_END_POINT <br />

METHOD : POST <br />

localhost:5000/login <br />

Request body <br />
username <br />
password <br />

Sample request <br />
{"username" : "anshu_user", "password" : "asdfghjkl" } <br />


Response Param <br />
{ <br />
  "status": true <br />
} <br />


###CREATE_END_POINT:

METHOD : POST <br />

localhost:5000/addProduct <br />

Request body <br />
title <br />
description <br />
price <br />
user_id <br />

IF USER <br />

Sample request <br />
{"title" : "sports", "description" : "batting", "price" : 5000, "user_id" : "f1b3dcb7-83a5-49a8-8d52-6dcf68fbfff5"} <br />

Response Param <br />
{ <br />
  "message": "Operation not permitted",<br />
  "status": false <br />
} <br />

IF ADMIN / SELLER <br />

Sample request <br />
ADMIN <br />
{"title" : "sports", "description" : "batting", "price" : 5000, "user_id" : "0a8aee78-2e9d-491c-8af1-1390ef50586a"} <br />
SELLER <br />
{"title" : "phone", "description" : "nokia", "price" : 15000, "user_id" : "93adf6b3-c38a-4dbd-9092-ba2d42d86690"} <br />

Response Param <br />
{ <br />
  "status": true <br />
} <br />


###READ_END_POINT: <br />

METHOD : GET <br />

Type <br />
 
searchProductById <br />

localhost:5000/searchProductById?prod_id=fb98e6b4-b2cc-414b-92f5-9264ef0a14d4 <br />

Request Body <br />
prod_id <br />

{ <br />
  "products": [ <br />
    { <br />
      "_id": { <br />
        "$oid": "5916b4cc1d41c813b1781c1a" <br />
      }, <br />
      "description": "batting", <br />
      "price": 5000, <br />
      "product_id": "fb98e6b4-b2cc-414b-92f5-9264ef0a14d4", <br />
      "seller_id": "0a8aee78-2e9d-491c-8af1-1390ef50586a", <br />
      "title": "sports" <br />
    } <br />
  ], <br />
  "status": true <br />
} <br />

searchProductByParameters <br />

localhost:5000/searchProductByParameters?title=sports <br />
OR <br />
localhost:5000/searchProductByParameters?description=batting <br />
OR <br />
localhost:5000/searchProductByParameters?price=5000 <br />

Request Body <br />
prod_id  <br />

{
  "products": [ <br />
    { <br />
      "_id": { <br />
        "$oid": "5916b4cc1d41c813b1781c1a" <br />
      }, <br />
      "description": "batting", <br />
      "price": 5000, <br />
      "product_id": "fb98e6b4-b2cc-414b-92f5-9264ef0a14d4", <br />
      "seller_id": "0a8aee78-2e9d-491c-8af1-1390ef50586a", <br />
      "title": "sports" <br />
    } <br />
  ], <br />
  "status": true <br />
} <br />


###UPDATE_END_POINT: <br />

METHOD : POST <br />

localhost:5000/updateProduct <br />

IF USER: <br />

Request body <br />
title <br />
description <br />
price <br />
user_id (which shoud be logged in as creation owner of seller or Admin only ) <br />

Sample Request if User / invalid seller logged in <br />
{"title" : "sports1", "description" : "batting1", "price" : 6000, "user_id" : "f1b3dcb7-83a5-49a8-8d52-6dcf68fbfff5"} <br />

response normal user <br />
{ <br />
  "message": "Opearation not permitted", <br />
  "status": false <br />
} <br />

resplonse if SELLER WITH INVALID creation: <br />
{ <br />
  "message": "Opearation not permitted", <br />
  "status": false <br />
} <br />

ANY OTHER CASES: <br />

Sample Request <br />
{"title" : "sports1", "description" : "batting1", "price" : 6000, "user_id" : "0a8aee78-2e9d-491c-8af1-1390ef50586a", "product_id": "fb98e6b4-b2cc-414b-92f5-9264ef0a14d4"} <br />

response <br />
{ <br />
  "status": true <br />
} <br />


###DELETE_END_POINT: <br />

METHOD : DELETE <br />

localhost:5000/deleteProduct <br />

{"product_id":"fb98e6b4-b2cc-414b-92f5-9264ef0a14d4", "user_id":"f1b3dcb7-83a5-49a8-8d52-6dcf68fbfff5"} <br />

IF USER: <br />


{"product_id":"fb98e6b4-b2cc-414b-92f5-9264ef0a14d4", "user_id":"f1b3dcb7-83a5-49a8-8d52-6dcf68fbfff5"} <br />

{ <br />
  "message": "Opearation not permitted", <br />
  "status": false <br />
} <br />

IF SELLER WITH INVALID creation: <br />

{ <br />
  "message": "Opearation not permitted", <br />
  "status": false <br />
} <br />

ANY OTHER CASES: <br />

{"product_id":"fb98e6b4-b2cc-414b-92f5-9264ef0a14d4", "user_id":"f1b3dcb7-83a5-49a8-8d52-6dcf68fbfff5"} <br />

{ <br />
  "status": true <br />
} <br />













