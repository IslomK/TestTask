# TestTask

The following project is considered to be little client-order system in taxi service. For developing the project, Python/Django framework (v2.2.5) is used. All the required libraries are placed in the document - requirements.txt. In order to install them, write the following command after activating your python virtual enviroment:
~~~
pip install -r requirements.txt
~~~
For the database, PostgreSQL is used. In order to start project, create the database __"my_taxi"__, with the role __"my_taxi"__, password - __"my_taxi"__. Or, if you want to use your own database without creating new one, just go the _settings/base.py_ and change database options.


The project structure:
~~~
my_taxi:
  apps/
  project/
  manage.py
~~~
where _apps/_ is the directory where all the applications are stored. "account" app - application where all the models related to user are located (Client, Driver). "restful" - main part of the project. "store" - orders.

According to the fact, that the project is test task, I decided not to use user authentication.

To create new order:
***POST*** __/v1/client/orders/create/__ - POST request made by client to create new order. All three fields are required. After request is made, if there is not any user with the given phone, new user is created by system automatically.
~~~
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string"
}
~~~

To get new orders:
***GET*** - __/v1/drivers/orders/__ - GET request made by drivers to get the list of new orders. 

To accept order:
***PUT*** - __/v1/drivers/orders/accept/{id}/__ - PUT request made by drivers in order to accept certain order with the given __"id"__. Parameters - first_name, last_name, phone, car_number. All of them are required. If there is no driver with the given number, system automatically creates new driver(user).
~~~
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "car_number": "string"
}
~~~

To update status:
***PUT*** - __/v1/drivers/orders/update-status/{id}/__ - PUT request mad by drivers in order to update the status of the order. __"id"__ is order id. Parameters: "status", "total_cost". Status is required field. Available "status" choices are:
__"driver_arrived"__, __"client_in_car"__, __"completed"__. When "status" is "completed", "total_cost" field is required as well.
~~~
{
  "status": "string",
  "total_cost": float
}
~~~

To get the order details(status and etc):
***GET*** - __/v1/orders/{id}/__ - GET request in order to get the details of the order, where __"id"__ is order id.
