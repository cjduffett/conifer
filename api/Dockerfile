FROM python:3.11-buster

# Install and upgrade base OS libraries, tools
RUN apt update && apt upgrade -y && apt install -y \
    git \
    pipx \
    postgresql-client \
    python3-venv \
    vim

# Create non-root user, switch to user space
ENV USER conifer
ENV HOME=/home/conifer

RUN useradd --user-group --create-home $USER
USER $USER
WORKDIR $HOME

# Install poetry
ARG POETRY_VERSION=1.4.2
ENV PATH="$HOME/.local/bin:$PATH"
RUN pipx install poetry==${POETRY_VERSION} && pipx ensurepath

# Create a python virtual environment for the project. Poetry will
# detect and use this virtual environment to install all dependencies.
ENV PATH="$HOME/.venv/bin:$PATH"
RUN python3 -m venv .venv

# Copy project dependency files
COPY pyproject.toml poetry.lock $HOME/

# Install all Python project dependencies first in a separate, cache-able layer
RUN poetry install --no-root

# Copy the rest of the project source code
COPY . $HOME

# Install 'conifer' Python package
RUN poetry install

ENTRYPOINT ["make"]
