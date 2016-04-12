docker run --name db -d -p 3456:3306 -v /data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=Fsh78978 fanshaohua.fan/mariadb
docker run --name flask --link db -d -v ~/sourcecode/wxserver/webapp/:/app fanshaohua.fan/flask python web.py
docker run --name wx -p 80:8080 --link flask --link api -d fanshaohua.fan/nginx
docker run --name api -d -v ~/sourcecode/wxserver/webapi/:/api fanshaohua.fan/api python3 api.py
