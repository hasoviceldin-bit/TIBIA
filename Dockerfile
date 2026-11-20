FROM python:3.12-slim
WORKDIR /app
COPY site.tar.xz /tmp/site.tar.xz
RUN python -c "import tarfile; tarfile.open('/tmp/site.tar.xz','r:xz').extractall('/app')" \
 && pip install --no-cache-dir -r requirements.txt \
 && rm /tmp/site.tar.xz
ENV PYTHONUNBUFFERED=1
EXPOSE 10000
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-10000}"]
