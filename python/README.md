# Setup

## Install dependencies

``` bash
pip3 install -r requirements.txt
```

## Setup dotenv (environment variables)

Copy the .env.example file to .env

``` bash
cp .env.example .env
```
Replace the values of the variables in the .env file

## Run project locally

``` bash
export $(grep -v '^#' .env| xargs )
python3 api.py
```
## Running in Docker

```sh
# To build and run locally
docker build -t capstone  .
docker run --rm -it -p 8000:8000 --env-file=.env capstone
# To build and push to docker
docker buildx build --platform linux/amd64,linux/arm64 --push -t zeisha/academy-sre-bootcamp-poonam-yadav:latest .

#To run image available in docker (make sure you dont have an older version locally)
docker image rm zeisha/academy-sre-bootcamp-poonam-yadav 
docker run --rm -it -p 8000:8000 --env-file=.env zeisha/academy-sre-bootcamp-poonam-yadav
```

## Endpoints

- [post] /login
- [get] /_health
- [get] /cidr-to-mask?value=?
- [get] /mask-to-cidr?value=?

# Curl commands to see output of API

```sh
#login
curl -d "username=admin&password=secret" http://localhost:8000/login

output: {"data":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI"}

#cidr-to-mask
curl -H 'Accept: application/json' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI" "http://localhost:8000/cidr-to-mask?value=1"

output: {"function":"cidrToMask","input":"1","output":"128.0.0.0"}

#mask-to-cidr
curl -H 'Accept: application/json' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI" "http://localhost:8000/mask-to-cidr?value='0.0.0.0'"

output: {"function":"maskToCidr","input":"'0.0.0.0'","output":"Invalid mask provided"}

```