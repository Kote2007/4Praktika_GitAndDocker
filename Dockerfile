FROM python:3.11.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN groupadd --gid 10006 appgroup \
    && useradd --uid 10006 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser

COPY attendance.py attendance.csv.example ./

RUN chown -R appuser:appgroup /app

USER appuser

CMD ["python", "attendance.py"]