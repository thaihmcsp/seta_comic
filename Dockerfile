FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
 
# Keep entrypoint out of /app so the bind mount can't override it
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh
 
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]