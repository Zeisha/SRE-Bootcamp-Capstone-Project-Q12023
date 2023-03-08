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
docker build -t zeisha/academy-sre-bootcamp-poonam-yadav:latest  .
docker run --rm -it -p 8000:8000 --env-file=.env  zeisha/academy-sre-bootcamp-poonam-yadav:latest 
```

## Endpoints

- [post] /login
- [get] /_health
- [get] /cidr-to-mask?value=?
- [get] /mask-to-cidr?value=?

