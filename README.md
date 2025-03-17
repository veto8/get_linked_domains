# get_linked_domains
Python App to extract all linked Domain Names from a specific Website

## Install
```
git clone https://github.com/myridia/get_linked_domains.git
cd get_linked_domains
python3 -m venv env
. env/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

## Test run
### Run Docker to simulate a nested website on local host 127.0.0.1
```
cd website/dockers/
docker-compose up -d
```

### Run ./main.py to access the docker website what runs on your local host 127.0.0.1
```
cd ../../
./main.py
```
