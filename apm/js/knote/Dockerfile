FROM node:12.0-slim
WORKDIR /app
COPY /app/package*json ./
RUN npm install
COPY /app .
CMD [ "node", "index.js" ]
