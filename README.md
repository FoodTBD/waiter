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

2. Create the EB config and application (substitute your actual API key for XXX):

    eb init food-tbd -r us-east-1 -p "Docker running on 64bit Amazon Linux 2023"
    eb create food-tbd-waiter -i t4g.nano --sample \
        --envvars ALGOLIA_SEARCH_API_KEY="XXX"

4. Deploy this code

    eb deploy

5. In [AWS Certificate Manager](https://us-east-1.console.aws.amazon.com/acm/home?region=us-east-1), create a HTTPS certificate for `api.food-tbd.com`.  This requires creating a CNAME record for DNS verification on the DNS host.

6. Also create a CNAME record to point `api.food-tbd.com` to the generated EB environment domain e.g. `food-tbd-waiter.eba-5ynepjcj.us-east-1.elasticbeanstalk.com`.

7. Finally, fix up the EB environment configuration. In [EB environment > Configuration > Instance traffic and scaling](https://us-east-1.console.aws.amazon.com/elasticbeanstalk/home?region=us-east-1#/environment/configuration/instance-traffic-scaling):

    * Under Listeners, add a listener for port 443, HTTPS, using the cert created in the previous step.
    * Under Processes, change the health check path from default `/` to `/hello`.
