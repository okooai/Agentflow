FROM python:3.13-alpine

ARG DEVELOPMENT=false

LABEL maintainer=achillesrasquinha@gmail.com

ENV AGENTFLOW_PATH=/agentflow

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $AGENTFLOW_PATH && \
    pip install --upgrade pip

COPY . $AGENTFLOW_PATH
COPY ./docker/entrypoint.sh /entrypoint
RUN sed -i 's/\r//' /entrypoint \
	&& chmod +x /entrypoint

WORKDIR $AGENTFLOW_PATH

RUN if [[ "${DEVELOPMENT}" ]]; then \
        pip install -r ./requirements-dev.txt; \
        python setup.py develop; \
    else \
        pip install -r ./requirements.txt; \
        python setup.py install; \
    fi

ENTRYPOINT ["/entrypoint"]

CMD ["agentflow"]