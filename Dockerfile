FROM python:3.9-slim
WORKDIR /project
ENV PYTHONPATH=/project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data
COPY search_engine ./search_engine

EXPOSE 5000  

CMD [ "python", "app/app.py"]