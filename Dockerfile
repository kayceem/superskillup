FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-traditional
# RUN apt-get update && apt-get install -y wkhtmltopdf

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


EXPOSE 8033


# CMD python manage.py runserver 0.0.0.0:8003
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]