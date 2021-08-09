FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
ARG EXTERNAL_PORT
ENV EXTERNAL_PORT=${EXTERNAL_PORT}
RUN echo $EXTERNAL_PORT
RUN sed -i "s/external_port/$EXTERNAL_PORT/" /etc/nginx/conf.d/nginx.conf

