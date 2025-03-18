FROM debian:latest
LABEL version="0.1"
MAINTAINER veto<veto@myridia.com>
RUN apt-get update && apt-get install -y \
  curl \
  wget \	      
  apt-utils \
  openssh-server \ 
  build-essential \
  checkinstall \
  libncursesw5-dev \
  libssl-dev  \
  libsqlite3-dev  \
  tk-dev  \
  libgdbm-dev  \
  libc6-dev  \
  libbz2-dev  \
  libffi-dev \
  libpython3-all-dev \
  git \
  libglib2.0-0 \
  libnss3 \
  libatk1.0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libxcomposite1  
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libxkbcommon0 \
  libpango  \
  libpango-1.0-0 \
  libcairo2 \
  libasound2 

#./chrome --headless--disable-gpu --no-sandbox https://myridia.com
  
WORKDIR /opt

RUN wget https://www.python.org/ftp/python/3.13.2/Python-3.13.2.tgz 
RUN tar xvf Python-3.13.2.tgz
WORKDIR /opt/Python-3.13.2 
RUN ./configure --enable-optimizations --enable-shared 
RUN make -j4 
RUN make altinstall
RUN ldconfig /usr/local/lib

WORKDIR /opt/



RUN git clone https://github.com/myridia/get_linked_domains.git
WORKDIR /opt/get_linked_domains
RUN /usr/local/bin/python3.13 -m venv env
#RUN . env/bin/activate
ENV PATH="env/bin:$PATH"
RUN pip install pip --upgrade
RUN pip install -r requirements.txt


#VOLUME /root/src



CMD ["/bin/bash"]
