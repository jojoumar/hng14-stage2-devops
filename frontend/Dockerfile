# -------- Stage 1: Build --------
FROM node:18-alpine AS builder

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app

COPY package*.json ./
RUN npm install --only=production

COPY . .

# -------- Stage 2: Runtime --------
FROM node:18-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && apk add --no-cache wget

COPY --from=builder /app /app

# Change ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

# Healthcheck (checks if server responds)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

CMD ["node", "app.js"]