FROM continuumio/miniconda3:latest

# found this code snippet at the following repository: https://github.com/jacopoMauro/minizinc/blob/master/Dockerfile
RUN apt-get update &&\
	apt-get -y install \
		git \
		wget \
		libgl1 && \
	rm -rf /var/lib/apt/lists/* && \
	mkdir /tool && \
	cd /tool && \
	wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.7.6/MiniZincIDE-2.7.6-bundle-linux-x86_64.tgz && \
	tar -zxvf MiniZincIDE-2.7.6-bundle-linux-x86_64.tgz && \
	mv /tool/MiniZincIDE-2.7.6-bundle-linux-x86_64 /tool/MiniZincIDE && \
	rm -rf MiniZincIDE-2.7.6-bundle-linux-x86_64.tgz

ENV PATH "$PATH:/tool/MiniZincIDE/bin"
ENV LD_LIBRARY_PATH "$LD_LIBRARY_PATH:/tool/MiniZincIDE/lib"

WORKDIR /app

COPY . .

RUN conda env create -f ift-4001-tp2.yml

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ift-4001-tp2"]

CMD ["python3", "/app"]
