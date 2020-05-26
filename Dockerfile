FROM node:10.13-alpine
ENV NODE_ENV production
WORKDIR /usr/src/map
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent && mv node_modules ../
COPY . .
EXPOSE 5000
CMD npm start