FROM python:3.12-slim-trixie AS base

FROM base AS builder_base

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

FROM builder_base AS habushu_builder

ARG UV_DEPENDENCY_GROUP=smsfilter_dependency_group

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv==0.6.2

WORKDIR /work-dir
COPY --chown=1001 target/containerize-support ./containerize-support
RUN find . -type f -name pyproject.toml -exec sed -i 's|develop[[:blank:]]*=[[:blank:]]*true|develop=false|g' {} \;

USER root
WORKDIR /work-dir/containerize-support/backend/api

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR="/.cache/uv"

# Install dependencies into the virtual environment created in builder_base
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --no-editable --no-dev --group ${UV_DEPENDENCY_GROUP}

FROM base AS final_base

ARG APP_USERNAME=appuser
ARG APP_DIR=/app
ARG USER_UID=10001
ARG USER_GID=10001

# Install runtime dependencies
RUN apt-get update && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN true \
    && addgroup --system --gid ${USER_GID} ${APP_USERNAME} \
    && adduser --system --uid ${USER_UID} --gid ${USER_GID} --no-create-home ${APP_USERNAME}

RUN mkdir ${APP_DIR} && chown -R ${APP_USERNAME}:${APP_USERNAME} ${APP_DIR}

FROM final_base AS final

COPY --from=habushu_builder --chown=1001 \
    /work-dir/containerize-support/backend/api/.venv \
    /work-dir/containerize-support/backend/api/.venv
ENV PATH="/work-dir/containerize-support/backend/api/.venv/bin:$PATH"

CMD uvicorn api.webapp:app --host 0.0.0.0 --port ${PORT:-8000} --timeout-keep-alive 1800

USER ${APP_USERNAME}