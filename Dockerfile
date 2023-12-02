FROM continuumio/miniconda3

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install minizinc -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && conda env create -f ift_4001_tp2.yml

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ift-4001-tp2"]

CMD ["python3", "/app"]
