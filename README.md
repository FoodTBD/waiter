# backend

This project implements the FoodTBD Data API, which provides access to restaurant menu and dish data.

We use [OpenAPI Specification 3](https://learn.openapis.org/introduction) to spec the API. The file `api.yaml` contains the full API description.

## Developing

### Setting up virtual environment

    python3 -m venv env

    source env/bin/activate
    pip install -r requirements.txt


### Running locally

    source env/bin/activate
    python main.py

Go to http://localhost:5000/ui/ to see the interactive API documentation.


## Building and Running in Docker

    docker build -t foodtbd_backend .
    docker run -p 80:80 foodtbd_backend

Go to http://localhost/ui/ to see the interactive API documentation.
