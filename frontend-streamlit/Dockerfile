
FROM python:3.9.12

ENV PYTHONUNBUFFERED=1

RUN mkdir /frontend-streamlit

WORKDIR /frontend-streamlit

COPY requirements.txt /frontend-streamlit/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /frontend-streamlit

ENV ON_DOCKER Yes

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]




