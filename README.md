# TestTask
POST /v1/client/orders/create/ - POST request made by client to create new order. All three fields are required. After request is made, if there is not any user with the given phone, new user is created.

{
  "first_name": "string",
  "last_name": "string",
  "phone": "string"
}

GET - /v1/drivers/orders/ - GET request made by drivers to get the list of new orders. 

PUT - /v1/drivers/orders/accept/{id}/ - PUT request made by drivers in order to accept certain order with the given order_id. Parameters - first_name, last_name, phone, car_number. All of them are required. If there is no driver with the given number, system automatically creates new driver(user).

{
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "car_number": "string"
}

PUT - /v1/drivers/orders/update-status/{id}/ - PUT request mad by drivers in order to update the status of the order. Parameters: "status", "total_cost". Status is required field. Available "status" choices are:
"driver_arrived", "client_in_car", "completed". When "status" is "completed", "total_cost" field is required as well.

{
  "status": "string",
  "total_cost": float
}


GET - /v1/orders/{id}/ - GET request in order to get the details of the order.
