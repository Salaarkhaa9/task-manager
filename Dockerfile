FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Initialize DB and start app
CMD python -c "from app import init_db; init_db()" && python app.py
