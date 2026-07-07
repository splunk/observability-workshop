# syntax=docker/dockerfile:1

FROM node:20-alpine
WORKDIR /app

COPY services/payment-api/package.json ./
COPY services/shared/package.json ./shared/
RUN npm install --omit=dev && npm install --omit=dev --prefix ./shared

COPY services/shared/propagation.js ./shared/
COPY services/payment-api/ ./

ENV NODE_ENV=production
EXPOSE 3005

CMD ["npm", "start"]
