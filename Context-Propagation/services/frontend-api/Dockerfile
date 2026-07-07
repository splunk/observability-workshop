# syntax=docker/dockerfile:1

FROM node:20-alpine
WORKDIR /app

COPY services/frontend-api/package.json ./
RUN npm install --omit=dev

COPY services/frontend-api/ ./

ENV NODE_ENV=production
EXPOSE 3007

CMD ["npm", "start"]
