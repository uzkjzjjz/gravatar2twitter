FROM python:alpine

LABEL maintainer="myl7 <myl@myl.moe>"

RUN pip install --no-cache-dir TwitterAPI requests

COPY run.py /run.py

ENTRYPOINT ["python", "/run.py"]
