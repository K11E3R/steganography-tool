FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV AUTHOR="K11e3r"
ENV VERSION="1.0.0"
ENV DESCRIPTION="Steganography Tool for hiding and extracting images."

EXPOSE 80

ENTRYPOINT ["python", "steganography.py"]
