FROM python:3.10-slim

# set up work dir
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install necessary dependents if needed
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# install requirements
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# expose streamlit port 
EXPOSE 8501

# activate

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]