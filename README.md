# QuizGPT CMS Backend Setup

## Set up Auth0

### Instructions:

Register an application with Auth0 at https://auth0.com/. The CMS frontend and backend will use the same application. In the application settings panel, note down the *domain*.
\
\
Obtain the Auth0 JWT certification by fetching it from the URL that corresponds to your Auth0 domain and the route /pem:
\
\
``curl https://dev-yv4demusjbg8zfv3.us.auth0.com/pem``

## Set environmental variables

### Set:

``DATABASE_URL=postgresql://postgres:postgres@localhost:5432/quiz-app`` \
``AUTH0_DOMAIN=`` \
<span style="color: gray">\# Can be named arbitrarily but must be the same value as that of the CMS backend</span> \
``AUTH0_AUDIENCE=`` \
``AUTH0_CERT=``

The variable `AUTH0_DOMAIN` must fit on one line and line breaks must be replaced by newline characters, e.g.:
\
\
``AUTH0_CERT=-----BEGIN CERTIFICATE-----\nMMIIDHTC...``

## Set up the Python venv

### Run:

``python3 -m venv env``\
``source env/bin/activate``

## Install dependencies

### Run:

``pip install -r requirements.txt``

## Start the server

``flask --app app run``
