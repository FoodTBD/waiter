import logging

import connexion

logging.basicConfig(level=logging.INFO)


app = connexion.FlaskApp(__name__)
app.add_api("api.yaml")


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
else:
    # Export symbol for uWSGI 
    application = app
