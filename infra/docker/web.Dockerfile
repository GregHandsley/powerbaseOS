# Build step
FROM node:20-alpine AS build
WORKDIR /app
COPY apps/web/package*.json ./
RUN npm ci || npm install
COPY apps/web ./
# For dev we’ll run Vite directly; build is optional in Sprint 1
# RUN npm run build

# Dev runtime (bind mounts in compose override app code)
FROM node:20-alpine
WORKDIR /app
COPY --from=build /app /app
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]