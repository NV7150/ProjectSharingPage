FROM nimlang/nim:1.4.2-ubuntu

RUN mkdir /code
COPY ./ /code
WORKDIR /code

RUN nimble build

# Change user
RUN useradd containeruser
RUN chown -R containeruser /code
USER containeruser

CMD ["./recommendengine"]
