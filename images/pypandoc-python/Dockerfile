ARG PANDOC_IMAGE_NAME=pandoc/latex
ARG PANDOC_IMAGE_TAG=edge-ubuntu

FROM ${PANDOC_IMAGE_NAME}:${PANDOC_IMAGE_TAG} AS pypandoc

RUN apt-get update && \
    apt-get install -y \ 
    unzip python3 python3.12-venv python3-pip -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install pypandoc pypandoc-binary \ 
    --break-system-packages

ENTRYPOINT ["python3"]
