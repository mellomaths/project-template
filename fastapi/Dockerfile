FROM python:3.12 as base

# RUN apt-get update && apt-get upgrade -y

FROM base as runner

WORKDIR /app

COPY ./ ./

ENV POETRY_VERSION 1.8.2

ENV PORT 4000
EXPOSE 4000

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install "uvicorn[standard]"

CMD gunicorn --workers=2 --threads=4 --timeout 360 --worker-class uvicorn.workers.UvicornWorker -b :$PORT src.main:app
