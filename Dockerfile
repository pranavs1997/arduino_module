FROM ghcr.io/ad-sdl/wei

LABEL org.opencontainers.image.source=https://github.com/pranavs1997/arduino_module
LABEL org.opencontainers.image.description="A module that allows you to flash Arduino UNO."
LABEL org.opencontainers.image.licenses=MIT

#########################################
# Module specific logic goes below here #
#########################################

RUN apt-get update && \
apt-get install -y curl

RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/local/bin sh

RUN arduino-cli config init

RUN arduino-cli config set library.enable_unsafe_install true

RUN arduino-cli core update-index

# install arduino avr
RUN arduino-cli core install arduino:avr

RUN mkdir -p arduino_module

COPY ./src arduino_module/src
COPY ./README.md arduino_module/README.md
COPY ./pyproject.toml arduino_module/pyproject.toml

RUN --mount=type=cache,target=/root/.cache \
    pip install ./arduino_module


CMD ["python", "arduino_module/src/arduino_rest_node.py"]

#########################################
