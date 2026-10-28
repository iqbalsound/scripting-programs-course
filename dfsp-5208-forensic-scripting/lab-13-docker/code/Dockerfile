FROM python:3.12-slim
WORKDIR /app
COPY log_filter_cli.py sample_data.csv ./
RUN useradd --create-home appuser && mkdir -p /app/out && chown appuser /app/out
USER appuser
ENTRYPOINT ["python", "log_filter_cli.py"]
CMD ["--input", "sample_data.csv", "--output", "/app/out/output.csv", "--level", "ERROR"]
