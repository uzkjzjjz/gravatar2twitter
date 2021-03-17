FROM python:3.8-alpine

LABEL maintainer="myl7 <myl@myl.moe>"

RUN apk add --no-cache py3-pillow && pip install --no-cache-dir TwitterAPI requests

COPY run.py /run.py

ENTRYPOINT ["python", "/run.py"]
