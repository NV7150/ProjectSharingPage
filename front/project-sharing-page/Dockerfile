FROM node:lts-alpine

WORKDIR /code
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

EXPOSE 8080
CMD [ "npm", "run", "serve" ]
