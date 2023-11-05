FROM continuumio/miniconda3:22.11.1

WORKDIR /app

COPY . .

RUN conda env create -f ift_4001_tp2.yml

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ift-4001-tp2"]

CMD ["python3", "/app"]
