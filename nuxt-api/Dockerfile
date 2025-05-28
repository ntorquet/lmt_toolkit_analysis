FROM node:23-alpine

RUN apk add --no-cache bash

WORKDIR /app

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN dos2unix /entrypoint.sh

EXPOSE 3000

ENTRYPOINT [ "bash", "/entrypoint.sh" ]