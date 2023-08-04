FROM python:3.10
RUN mkdir /code
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN python3 -m pip install -U pip
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ /code