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

# If I were to use requirements.txt instead:
# COPY requirements.txt /Finance_Django_Project/
# RUN pip install --no-cache-dir -r requirements.txt

# Copy project (an equivalent is COPY . . )
COPY . /Finance_Django_Project/
