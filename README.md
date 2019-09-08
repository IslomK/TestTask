# TestTask
***POST*** __/v1/client/orders/create/__ - POST request made by client to create new order. All three fields are required. After request is made, if there is not any user with the given phone, new user is created by system automatically.
~~~
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string"
}
~~~

***GET*** - __/v1/drivers/orders/__ - GET request made by drivers to get the list of new orders. 

***PUT*** - __/v1/drivers/orders/accept/{id}/__ - PUT request made by drivers in order to accept certain order with the given __"id"__. Parameters - first_name, last_name, phone, car_number. All of them are required. If there is no driver with the given number, system automatically creates new driver(user).
~~~
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "car_number": "string"
}
~~~

***PUT*** - __/v1/drivers/orders/update-status/{id}/__ - PUT request mad by drivers in order to update the status of the order. __"id"__ is order id. Parameters: "status", "total_cost". Status is required field. Available "status" choices are:
__"driver_arrived"__, __"client_in_car"__, __"completed"__. When "status" is "completed", "total_cost" field is required as well.
~~~
{
  "status": "string",
  "total_cost": float
}
~~~


***GET*** - __/v1/orders/{id}/__ - GET request in order to get the details of the order, where __"id"__ is order id.
