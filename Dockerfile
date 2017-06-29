FROM python:3

WORKDIR /usr/src/custom-pipeline

COPY table_plots.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt