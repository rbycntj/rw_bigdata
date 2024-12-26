# gunicorn.conf

workers = 4
threads = 2
bind = '0.0.0.0:8000'
daemon = 'false'
worker_class = 'gevent'
worker_connections = 2000
pidfile = '/var/run/gunicorn.pid'
accesslog = '/var/log/gunicorn_acess.log'
errorlog = '/var/log/gunicorn_error.log'
loglevel = 'warning'
