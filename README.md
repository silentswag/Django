Django Vendor management system using rest framework

Clone the repository
https://github.com/silentswag/Django.git

Move into project folder
cd .\vendor_system\

Make migrations to apply changes made to models.py
py manage.py makemigrations
py manage.py migrate

Run the app
py manage.py runserver



Try the below list of urls for rendering views
1. http://127.0.0.1:8000/api/vendors
2. http://127.0.0.1:8000/api/vendors/8
3. http://127.0.0.1:8000/api/purchase_orders
4. http://127.0.0.1:8000/api/purchase_orders/8
5. http://127.0.0.1:8000/api/vendors/8/performance
6. http://127.0.0.1:8000/api/purchase_orders/8/acknowledge
