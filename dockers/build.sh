docker build -t myridia/webspider:latest .
docker run --name webspider  -it --rm  -v "$(pwd)":"/root/src"   myridia/webspider /bin/bash
