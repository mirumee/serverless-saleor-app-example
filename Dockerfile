FROM python:3.9
RUN apt-get -y update \
    && apt-get install -y gettext \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY poetry.lock pyproject.toml README.md /app/

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY src/lambda_saleor_app /app/src/lambda_saleor_app
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install ; else poetry install --no-dev ; fi"

# COPY .flake8 alembic.ini docker-entrypoint.sh /app/

EXPOSE 8080
# ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]

CMD python -m lambda_saleor_app
