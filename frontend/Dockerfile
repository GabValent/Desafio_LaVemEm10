# Etapa 1 - Build da aplicação
FROM node:20 AS builder

WORKDIR /app
COPY . . 
RUN npm install
RUN npm run build  # Certificando-se de que o comando de build seja executado corretamente

# Etapa 2 - Servir com NGINX
FROM nginx:stable-alpine

# Copiando os arquivos gerados pelo Vite na pasta dist para o Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf 

EXPOSE 80

# Iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
