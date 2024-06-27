# App service - Frontend application

This repo contains the frontend that works together with the [ml-service](https://github.com/remla24-team-1/model-service/) backend. It is versioned by [lib-version](https://github.com/remla24-team-1/lib-version).

## To run the frontend locally for testing or for developing: 
* First clone the repository using `git clone git@github.com:remla24-team-1/app.git` and access it with `cd app`.
* Create an environment file called `.env` containing MODEL_SERVICE_URL=http://172.17.0.2:8081 within the app-service folder root. For example: `echo MODEL_SERVICE_URL=http://172.17.0.2:8081 > .env`
* Build the project using `docker build -t ghcr.io/remla24-team-1/app:latest .`, and run the built image using `docker run ghcr.io/remla24-team-1/app:latest`.

The service will be hosted at localhost. To access the backend service, the model-service image also has to be ran.

## Release new image

To release a new docker image, create a git tag with `git tag vX.X.X`, and push that tag using `git push origin tag vX.X.X`. The GitHub workflow will then automatically update the corresponding versions accessible at [packages/app](https://github.com/orgs/remla24-team-1/packages/container/package/app).
