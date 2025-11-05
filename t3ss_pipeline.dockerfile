# USE offical Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /usr/src/app

#Install dependancie: Biopython and hmmer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        build-essential \ 
        zlib1g-dev \
        libncurses5-dev \
        libbz2-dev \
        liblzma-dev \
        && rm -rf /var/lib/apt/lists/*

# Install Biopython
RUN pip install --no-cache-dir Biopython

#download and install hmmer 
RUN wget http://eddylab.org/software/hmmer/hmmer.tar.gz && \
    tar -xvzf hmmer.tar.gz && \
    cd hmmer-* && \
    ./configure && make && make install && \
    cd .. && rm -rf hmmer-*

#Copy your combined pipeline script into the container
COPY t3ss_hmmscan_pipeline.py .

# Make script executable
RUN chmod +x t3ss_hmmscan_pipeline.py

#set default command to print usage
CMD ["python", "t3ss_hmmscan_pipeline.py"]
