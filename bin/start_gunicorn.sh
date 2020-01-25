#!/bin/bash
source ~/.virtualenvs/shop/bin/activate
exec gunicorn -c "/root/code/shop/shop/gunicorn_config.py" shop.wsgi

