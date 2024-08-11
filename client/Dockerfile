# BASE OS
FROM node:20.10-alpine3.19 AS base
RUN apk --no-cache add curl

# CODEBASE
FROM base AS codebase
WORKDIR /app
COPY . .

# DEPS
FROM codebase AS deps
RUN npm i

# DEVELOPMENT
FROM deps AS development
EXPOSE 3000
CMD npm run start -- --host 0.0.0.0 --port 3000

# BUILDER
FROM deps AS builder
RUN npm run build

# PRODUCTION TARGET
FROM nginx AS production
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80