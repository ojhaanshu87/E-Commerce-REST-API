# E-Commerce-REST-API

## Description : <br />
This App is general (Create, Read, Update, Delete) REST-API. Each operation except Search item requires user credentials. In C-U-D methods authorised user only can do the operations. <br />

## Start API Server <br />
*python /path/to/server.py* <br />


*FOR DETAILS (params) REFER [API DOCS](https://github.com/ojhaanshu87/E-Commerce-REST-API/blob/master/API_Document.md)* <br />

### Mongo DB installation <br />
sudo apt-get install mongodb <br />

### Basic Installation Setups <br />
A) clone this repo <br />
B) cd /path/to/repo <br />
C) virtualenv venv <br />
D) . venv/bin/activate <br />
E) pip install -r requirements.txt <br />


### Operations : <br />
A) Register user as admin, seller or user <br />
B) For add(CREATE) Item, only Seller or Admin user allowed, login checked in prelim stage. <br />
C) For search(READ) items, the two method (one is by ID and other by any param), login not required <br />
D) For changes (UPDATE) items, only Admin or the seller who add the item previously is allowed, login checked in this stage as well <br />
E) For remove (DELETE) items, only Admin or the seller who add the item previously is allowed for delete, login checked in this stage as well <br />

### TODO <br />
A) Search by regular expression <br />
B) Implement (L)ongest (C)ommon (S)equence based search engine *[like here as in C#](https://github.com/ojhaanshu87/LCS-Problem-With-Percentage-Matching)* <br />
C) cart add option <br />

