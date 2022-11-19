FROM python:alpine3.16
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
#RUN python --version
EXPOSE 5000
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "main.py"]  
#CMD ["main.py"]
