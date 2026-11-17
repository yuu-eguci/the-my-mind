FROM node:26-slim

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve"]
