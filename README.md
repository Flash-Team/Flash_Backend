# Flash

## Main Idea

As we all know that the food is the basic need in every human life. 
We are lucky that we live in time of technological progress, 
where things like online ordering food will not surprise anyone. 
We took such factors as speed and quality as the basis, and this is how 
the idea of our website was born.

## About Flash

Flash is a food delivery service. Our food delivery website is a service 
for clients in which they can order any food which will be delivered
by courier as soon as possible.

### Main Features

Features which can be pointed out with _"what we learned from this course"_

#### Courier search algorithm

* After order created, database search for courier with the least number of active
orders. When such courier found, order now handled with this courier

* Used features: **Django Signals**

#### Rating system

* Entities such Product and Organization have rating system based on two fields: 
sum of all ratings (one rating is between 0 and 5) and count of all ratings.

* Organization can be rated infinitely, however, Product can be rated only via Order 
in which it is. Limit for rating order is one time and only by client who ordered it

* Used features: **@property**, **Django Signals**, **Model Inheritance**

#### Entity logo

* Entities such Product and Organization can have own logo, which is indeed is file.
File can be downloaded while creating objects, or after with changing state of object.

* All files stored in file system of server. Whenever object are deleted or its logo
was changed, old file deleted from file system

* Used features: **FileField**, **Django Signals**, **Model Inheritance**

#### Role division

* All users in system divided by roles. Since system for delivery service, there are 
four different roles:
    1. **Admin** - generally have permission for whole system
    2. **Manager** - manage organizations to which it is attached, can see all processes
    within his organizations
    3. **Client** - client can see organizations and order products from any filial
    of this organization. Also Client can rate organizations and products
    4. **Courier** - courier wait for order assignment. After order completed, he wait
    again
    
* All users must be authorized in the system, because all actions is related 
only for some roles (not all). Users must provide token for authentication

* Used features: **User Roles**, **Django Permissions**, **JWT**

## Other

### Contributors

1. [@MeBr0](https://github.com/MeBr0) - Yergali Azamat
2. [@shynaraaya](https://github.com/shynaraaya) - Ayanbek Shynara

### Database schema
Nothing special - [Here it is!](https://dbdiagram.io/d/5d9859a7ff5115114db4eeb8)
