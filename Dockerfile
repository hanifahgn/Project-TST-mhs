FROM python:3.10.5
WORKDIR /myapp
COPY requirements.txt /myapp/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /myapp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]