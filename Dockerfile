FROM python:3.7-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY * ./

RUN pip install pipenv
RUN pipenv install --system

EXPOSE 5000
CMD [ "python", "speedport_exporter.py"]
