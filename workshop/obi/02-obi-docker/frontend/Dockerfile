FROM node:22.23.4-slim
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY server.js .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
