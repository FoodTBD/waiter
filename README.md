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

# To deploy to AWS Elastic Beanstalk

1. Install AWS Elastic Beanstalk CLI via Homebrew
    brew install awsebcli

2. Create the EB config and application

    eb init food-tbd -r us-east-1 -p "Docker running on 64bit Amazon Linux 2023"
    eb create food-tbd-waiter -i t4g.nano --sample

3. Copy `dotenv.sample` to `.env` and fill in the secrets.

4. Deploy this code

    eb deploy

5. Fix up the configuration from EB defaults. In [EB environment > Configuration > Instance traffic and scaling](https://us-east-1.console.aws.amazon.com/elasticbeanstalk/home?region=us-east-1#/environment/configuration/instance-traffic-scaling):

    * Under Processes, change the health check path from default `/` to `/hello`.