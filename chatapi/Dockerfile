FROM python:3.9-slim-buster

# Create dir
RUN mkdir /code
WORKDIR /code

# Install deps
COPY ./requirements.txt /code
RUN pip install -r requirements.txt

COPY ./ ./

# Change user
RUN useradd containeruser
RUN chown -R containeruser ./
USER containeruser

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
