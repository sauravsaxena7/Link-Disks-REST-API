from alpine:latest


#step 2: install pip and python Dependencies
RUN apk add --no-cache python3-dev \ && pip3 install --upgrade pip


#step 3 Create a Work directory
WORKDIR /app

#step 4 : copy all Project files

COPY . /app


#step 5 
Run set -e; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    ; \
    pip3 --no-cache-dir install -r requirements.txt; \
    apk del .build-deps;


#step 6: run the command to start uWsgi

CMD [ "uwsgi","app.iml" ]


