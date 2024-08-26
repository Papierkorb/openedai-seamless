FROM python:3-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bake the model into the image to speed up start up and reduce network load.
COPY download.py .
RUN python download.py

COPY main.py .
EXPOSE 3000
CMD [ "python", "main.py" ]
