# E-Commerce-REST-API

## Description :
This App is general (Create, Read, Update, Delete) REST-API. Each operation except Read item required the crediantial. In C-U-D method authrised user only can do the operations. 

*FOR DETAILS (params) REFER [API DOCS](https://github.com/ojhaanshu87/E-Commerce-REST-API/blob/master/API_Document.md)* <br />

### Basic Installation Setups <br />
A) clone this repo <br />
B) virtualenv venv <br />
C) . venv/bin/activate <br />

### General Dependency installation <br />
sudo pip install flask <br />
sudo pip install passlib <br />
sudo pip freeze > requirements.txt <br />
sudo apt-get install mongodb <br />
sudo pip install mongoengine <br />
sudo pip install mongomock <br />

### Operations : <br />
A) Register user as admin, seller or user <br />
B) For add(CREATE) Item, only Seller or Admin user allowed, login checked in prelim stage. <br />
C) For search(READ) items, the two method (one is by ID and other by any param), login not required <br />
D) For changes (UPDATE) items, only Admin or the seller who add the item previously is allowed, login checked in this stage as well <br />
E) For remove (DELETE) items, only Admin or the seller who add the item previously is allowed for delete, login checked in this stage as well <br />

###TODO <br />
A) Search by regular expression
B) Implement (L)ongest (C)ommon (S)equence based search engine *[like here as in C#](https://github.com/ojhaanshu87/LCS-Problem-With-Percentage-Matching)* <br />
C) cart add option

