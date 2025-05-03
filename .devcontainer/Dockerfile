FROM node:20-alpine

# System vorbereiten
WORKDIR /src/app
COPY . .

# Dependencies installieren
RUN npm install

# Startkommando
CMD ["npm", "start"]
