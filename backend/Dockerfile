FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY backend/requirements.txt .
COPY backend/entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /src/backend

WORKDIR /src/backend

RUN chmod +x /src/entrypoint.sh

EXPOSE 8000

CMD ["/src/entrypoint.sh"]