# syntax=docker/dockerfile:1

FROM node:20-alpine AS build
WORKDIR /app

ARG REALM
ARG RUM_TOKEN
ARG RUM_APP_NAME=cosmic-observatory-shop
ARG DEPLOYMENT_ENV=workshop

ENV REALM=$REALM
ENV RUM_TOKEN=$RUM_TOKEN
ENV RUM_APP_NAME=$RUM_APP_NAME
ENV DEPLOYMENT_ENV=$DEPLOYMENT_ENV

COPY services/frontend/package.json ./
RUN npm install

COPY services/frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine
COPY deploy/nginx/frontend.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
