FROM registry.otrs365.cn/hub/python:3.8.5-alpine3.12

ENV TZ=Asia/Shanghai
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/' /etc/apk/repositories \
    && apk add --no-cache  tzdata gcc g++ 

WORKDIR /app
COPY . /app

RUN pip config set global.index-url  'https://mirrors.aliyun.com/pypi/simple/' \
    && pip config set install.trusted-host= 'mirrors.aliyun.com' \
    && pip install --no-cache-dir -r requirements.txt


CMD ["python", "main.py"]

