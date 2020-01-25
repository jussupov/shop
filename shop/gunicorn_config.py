command = '/root/.virtualenvs/shop/bin/gunicorn'
pythonpath = '/root/code/shop/shop'
bind = '127.0.0.1:8001'
workers = 5
user = 'root'
limit_requests_fields = 32000
limit_requests_field_size = 0
