# ─── Stage 1: Builder ─────────────────────────────────────────────────────
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json & lockfile, install deps
COPY package*.json ./
RUN npm install

# Copy rest of the source code, build the app
COPY . .
RUN npm run build

# ─── Stage 2: Production image ───────────────────────────────────────────
FROM nginx:alpine

# Copy built static files from builder
COPY --from=builder /app/dist /usr/share/nginx/html


# Expose port 80
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
