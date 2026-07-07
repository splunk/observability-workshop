# syntax=docker/dockerfile:1

FROM node:20-alpine
WORKDIR /app

COPY services/order-api/package.json ./
COPY services/shared/package.json ./shared/
RUN npm install --omit=dev && npm install --omit=dev --prefix ./shared

COPY services/shared/propagation.js ./shared/
COPY services/order-api/ ./

ENV NODE_ENV=production
EXPOSE 3001

CMD ["npm", "start"]
