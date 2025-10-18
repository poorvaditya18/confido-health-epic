# CONFIDO AUTH SERVICE:

description : responsible of generating auth, refresh tokens with data sources. Currently support SMART Oauth on FHIR.

# setup envs

EPIC_CLIENT_ID=
EPIC_PRIVATE_KEY_PATH=
EPIC_TOKEN_URL=
EPIC_SCOPES=
REDIS_PORT=
REDIS_HOST=
REDIS_PASSWORD=

NOTE:

- set the `EPIC_PRIVATE_KEY_PATH` of your local machine. file should look like `privatekey.pem`
- `EPIC_SCOPES` should be correctly provided : example system/Patient.read system/Appointment.read

# for setting up REDIS -

pull the latest docker image with correctly mention PORT number same as in envs.

# start server:

change directory to src : `cd src/`
start the server using `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

# API :

- for generating token : provide `x-source-type` in request headers

  request :
  `curl --location --request POST 'localhost:8000/confido-health/api/v1/auth' --header 'x-source-type: epic'`

  2xx response:
  `{ "source": "epic", "access_token": <ACCESS_TOKEN> }`