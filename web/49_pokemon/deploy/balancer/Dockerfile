FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 4000
CMD ["nginx", "-c", "/etc/nginx/nginx.conf", "-g", "daemon off;"]