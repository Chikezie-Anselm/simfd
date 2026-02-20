FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
COPY . .
RUN npm ci && npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/ .
ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm", "run", "start"]
