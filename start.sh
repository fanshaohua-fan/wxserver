docker run --name db -d -p 3306:3306 -v /data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 fanshaohua.fan/mariadb
docker run --name flask -d -v ~/sourcecode/wxserver/webapp/:/app fanshaohua.fan/flask python web.py
docker run --name wx -p 80:8080 --link flask -d fanshaohua.fan/nginx
