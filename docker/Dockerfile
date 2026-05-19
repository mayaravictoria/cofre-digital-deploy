FROM python:3.11-slim
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
USER appuser
EXPOSE ${PORT:-5000}
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
