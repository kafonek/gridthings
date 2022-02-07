FROM gitpod/workspace-full

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH "$PATH:$HOME/.local/bin"