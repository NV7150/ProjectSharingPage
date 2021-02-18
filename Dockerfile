FROM caddy:2.2.1-alpine

# Install npm
RUN apk add npm

WORKDIR /code
COPY ./front/project-sharing-page/package*.json ./
RUN npm install
COPY ./front/project-sharing-page .
RUN npm run build

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
