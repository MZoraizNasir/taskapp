# ─── Stage 1: Build React App ───────────────────────────────────
FROM registry.access.redhat.com/ubi8/nodejs-20 AS builder

WORKDIR /app

# Switch to root to allow writing to node_modules
USER root

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the code and build the app
COPY . .
RUN npm run build

# ─── Stage 2: Serve with UBI Nginx ──────────────────────────────
FROM registry.access.redhat.com/ubi8/nginx-120

# Copy the built React app to Nginx root directory
COPY --from=builder /app/dist /opt/app-root/src

# Run as non-root for security
USER 1001

# Expose default Nginx port
EXPOSE 8080

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
