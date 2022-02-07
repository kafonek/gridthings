FROM gitpod/workspace-full

ENV PATH="$HOME/.poetry/bin:$PATH"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
    poetry install


