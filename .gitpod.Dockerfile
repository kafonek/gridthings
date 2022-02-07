FROM gitpod/workspace-full

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH "$HOME/.local/bin:$PATH"