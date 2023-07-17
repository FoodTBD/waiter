# To run app locally
$ python3 -m venv .venv

$ . .venv/bin/activate

$ flask --app waiter run

# To run docker compose
Make sure docker daemon is running (open -a Docker)
$ docker compose up

# To create docker image
https://docs.docker.com/language/python/run-containers/

$ docker build -t waiter-server:latest .

$ docker tag waiter-server:latest 826534809592.dkr.ecr.us-east-1.amazonaws.com/waiter-ecr:latest

$ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 826534809592.dkr.ecr.us-east-1.amazonaws.com

$ docker push 826534809592.dkr.ecr.us-east-1.amazonaws.com/waiter-ecr:latest

$ docker run --publish 8000:5000 waiter-server 
The 8000 port can be replaced with something else