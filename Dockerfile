FROM python:3.7-slim

COPY scripts scripts

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r scripts/requirements.txt && \
    mkdir src

EXPOSE 1111

ENTRYPOINT ["python"]

CMD ["src/app.py"]