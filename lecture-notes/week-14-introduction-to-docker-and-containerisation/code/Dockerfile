FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home appuser && mkdir -p /app/evidence && chown -R appuser /app
USER appuser
ENTRYPOINT ["python3", "workflow.py"]

# .dockerignore
venv/
.env
.git/
__pycache__/
*.log
evidence/
output/
