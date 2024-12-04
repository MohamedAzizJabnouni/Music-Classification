# Use an official Nginx image to serve the static files
FROM nginx:alpine

# Copy the local static files (HTML, CSS, JS) into the Nginx web directory
COPY ./static /usr/share/nginx/html

# Expose port 80 to allow traffic to reach the container
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
