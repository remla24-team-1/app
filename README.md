# App service - Frontend application

This repo contains the frontend that works together with the [ml-service](https://github.com/remla24-team-1/model-service/) backend. It is versioned by [lib-version](https://github.com/remla24-team-1/lib-version).

## To run the frontend locally for testing or for developing: 
* First clone the repository using `git clone git@github.com:remla24-team-1/app.git` and access it with `cd app`.
* Create an environment file called `.env` containing MODEL_SERVICE_URL=http://172.17.0.2:8081 within the app-service folder root. For example: `echo MODEL_SERVICE_URL=http://172.17.0.2:8081 > .env`
* Build the project using `docker build`, and run the built image using `docker run`.

The service will be hosted at localhost. To access the backend service, the model-service image also has to be ran.
