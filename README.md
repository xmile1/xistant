# Xistant - A laid-back ai assistant

A laid-back implementation of an ai assistant based on Langchain and my immediate needs.

Objective
This project intends to create an ai assistant backend with a single point of entry, and multiple clients for different platforms.

Using the langchain ecosystem, the project intents to have a system that will be able to leverage and combine different ai services and applications.

It architechture utilizes a plugin system that allows for easy integration of new services and applications.


## Installation
1. clone the repository

### Backend
1. cd to the backend folder
2. add the neccessary environment variables to the .env.sample file and rename it to .env
3. setup a virtual environment
4. install the requirements using poetry
5. run the backend using uvicorn
```bash
  uvicorn api.main:app --reload  --host 0.0.0.0 --port 8000
```

## Clients
1. cd to the clients folder
2. cd into the client you want to use e.g mobile
3. Set the environment variables in the .env.sample file and rename it to .env
3. run yarn install
4. run yarn dev

### Contribution
Xistant is right now a per need basis.
If you have a need for a feature, please open an issue and we can discuss it or you can open a PR.
