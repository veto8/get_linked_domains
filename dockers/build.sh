docker build -t myridia/linkchecker:latest .
docker run --name linkchecker  -it --rm  -v "$(pwd)":"/root/src"   myridia/linkchecker /bin/bash
