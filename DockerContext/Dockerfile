FROM python:3.15

RUN set -ex \
    && git clone https://github.com/EricBoix/jejune_doc_Zen_Flesh_Zen_Bones.git \
    # Rename archive for clear context when debugging/fixing in container
    && mv jejune_doc_Zen_Flesh_Zen_Bones/ jejune_doc_Zen_Flesh_Zen_Bones.git
    # FIXME: we should be pinning the version with e.g.
    # && cd jejune_doc_Zen_Flesh_Zen_Bones.git \
    # && git checkout 444b50086c

WORKDIR /jejune_doc_Zen_Flesh_Zen_Bones.git/Convert
RUN set -ex && pip install --root-user-action=ignore uv

# Installs the locked dependencies, including the tools for running tests
RUN set -ex && uv sync --frozen

# Systematically run tests at build time (fail often, fail early)
RUN set -ex && uv run --frozen pytest

ENTRYPOINT ["uv", "run", "--frozen", "main.py"]
