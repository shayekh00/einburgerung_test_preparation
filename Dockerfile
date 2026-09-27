FROM nginx:alpine

COPY index.html test-your-knowledge.html style.css study-mode.js missed-questions.js dataset.json /usr/share/nginx/html/
COPY imgs/ /usr/share/nginx/html/imgs/

EXPOSE 80
