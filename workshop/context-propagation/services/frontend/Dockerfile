# syntax=docker/dockerfile:1

FROM node:20-alpine AS build
WORKDIR /app

ARG SPLUNK_REALM
ARG SPLUNK_RUM_ACCESS_TOKEN
ARG SPLUNK_RUM_APP_NAME=cosmic-observatory-shop
ARG SPLUNK_DEPLOYMENT_ENV=workshop

ENV SPLUNK_REALM=$SPLUNK_REALM
ENV SPLUNK_RUM_ACCESS_TOKEN=$SPLUNK_RUM_ACCESS_TOKEN
ENV SPLUNK_RUM_APP_NAME=$SPLUNK_RUM_APP_NAME
ENV SPLUNK_DEPLOYMENT_ENV=$SPLUNK_DEPLOYMENT_ENV

COPY services/frontend/package.json ./
RUN npm install

COPY services/frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine
COPY deploy/nginx/frontend.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
