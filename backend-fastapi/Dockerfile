#linux image that have python
FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /backend-fastapi

WORKDIR /backend-fastapi

COPY requirements.txt /backend-fastapi/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


COPY . /backend-fastapi/

ENV ON_DOCKER Yes

EXPOSE 5000

# CMD ["python", "main.py"]