# pull the latest official nginx image
FROM nginx:stable
EXPOSE 80
COPY static.conf /etc/nginx/conf.d/static.conf
ADD static /usr/share/nginx/html

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
