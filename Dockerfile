FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /codelib_app
COPY requirements.txt requirements.txt
#EXPOSE 8000
RUN pip3 install -r requirements.txt
