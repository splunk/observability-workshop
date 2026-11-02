# syntax=docker/dockerfile:1

FROM node:22.23.4-alpine
WORKDIR /app

COPY services/catalog-api/package.json ./
RUN npm install --omit=dev

COPY services/catalog-api/ ./

ENV NODE_ENV=production
EXPOSE 3002

CMD ["npm", "start"]
