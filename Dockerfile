FROM python:3.13.2-bookworm
WORKDIR /app

COPY . .

RUN chmod +x ./core.sh

RUN apt update && apt install -y jq bind9-host

RUN ./core.sh --install-requirements

CMD ["bash"]