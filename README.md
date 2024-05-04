Django Vendor management system using rest framework

1.	Clone the repository
https://github.com/silentswag/Django.git

2.	Move into project folder
cd .\vendor_system\

3.	Make migrations to apply changes made to models.py
py manage.py makemigrations
py manage.py migrate

4.	Run the app
py manage.py runserver



Try the below list of urls for rendering views
http://127.0.0.1:8000/api/vendors
http://127.0.0.1:8000/api/vendors/8
http://127.0.0.1:8000/api/purchase_orders
http://127.0.0.1:8000/api/purchase_orders/8
http://127.0.0.1:8000/api/vendors/8/performance
http://127.0.0.1:8000/api/purchase_orders/8/acknowledge
