# ----- Stage 1: Build the React App -----
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Build the app for production
# This creates a /app/dist folder with our static files
RUN npm run build

# ----- Stage 2: Serve the App with Nginx -----
FROM nginx:1.25-alpine AS final

COPY --from=build /app/dist /usr/share/nginx/html

# --- CHANGE THIS LINE ---
COPY nginx.prod.conf /etc/nginx/conf.d/default.conf
# --- END CHANGE ---

EXPOSE 80
CMD ["sh", "-c", "sed -i \"s/_PORT_/$PORT/g\" /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]