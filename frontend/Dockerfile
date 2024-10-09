FROM node:alpine as build

WORKDIR /src

RUN npm install -g @angular/cli

COPY frontend/package.json .
RUN npm install --legacy-peer-deps

COPY ./frontend /src/frontend

WORKDIR /src/frontend

RUN npm run build

RUN ls -la /src/frontend/dist/portfolio

FROM nginx:alpine

COPY --from=build /src/frontend/dist/portfolio/browser/ /usr/share/nginx/html

COPY frontend/nginx.conf /etc/nginx/nginx.conf

FROM node:alpine AS ssr-server
COPY --from=build /src/frontend/dist /src/frontend/dist/
COPY frontend/package.json  /src/frontend/package.json
WORKDIR /src/frontend
EXPOSE 4000
CMD npm run serve:ssr:portfolio

