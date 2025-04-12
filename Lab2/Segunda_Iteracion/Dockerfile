FROM i386/debian:bullseye

RUN apt update && apt install -y \
    python3 python3-venv python3-pip \
    gcc-multilib g++-multilib nasm \
    libfreetype6-dev libpng-dev libjpeg-dev \
    curl

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install flask requests matplotlib numpy plotly

WORKDIR /app

CMD [ "bash" ]
