docker run --name flask -d -v ~/sourcecode/wxserver/webapp/:/app fanshaohua.fan/flask python web.py
docker run --name wx -p 80:80 --link flask -d fanshaohua.fan/nginx
