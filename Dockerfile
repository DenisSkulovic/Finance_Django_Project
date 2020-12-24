# Pull base image
FROM python:3.8
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /Finance_Django_Project
# Install dependencies
COPY Pipfile Pipfile.lock /Finance_Django_Project/
RUN pip install pipenv && pipenv install --system
# Copy project
COPY . /Finance_Django_Project/
