FROM python:alpine3.16
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
EXPOSE 5000
#ENTRYPOINT ["python", "main.py"] 
ENTRYPOINT ["waitress-serve", "--port=5000", "main:app"] 
