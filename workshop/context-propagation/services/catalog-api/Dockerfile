# syntax=docker/dockerfile:1

FROM node:20-alpine
WORKDIR /app

COPY services/catalog-api/package.json ./
RUN npm install --omit=dev

COPY services/catalog-api/ ./

ENV NODE_ENV=production
EXPOSE 3002

CMD ["npm", "start"]
