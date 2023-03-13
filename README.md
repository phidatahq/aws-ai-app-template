## ML Application Server

This repo contains the code for running an ML Application in 2 environments:

1. dev: A development env running on docker
2. prd: A production env running on AWS ECS

## Setup Workspace

1. Create + activate a virtual env:

```sh
python3 -m venv ~/.venvs/mlenv
source ~/.venvs/mlenv/bin/activate
```

2. Install + init `phidata`:

```sh
pip install phidata
phi init -l
```

> from the `ml-app` dir:

3. Setup workspace:

```sh
phi ws setup
```

4. Copy `workspace/example_secrets` to `workspace/secrets`:

```sh
cp -r workspace/example_secrets workspace/secrets
```

Optional: Create `.env` file:

```sh
cp example.env .env
```

## Run ML App locally using docker

The [workspace/dev](workspace/dev) directory contains the resources for the dev environment. Install [docker desktop](https://www.docker.com/products/docker-desktop) and run dev resources using:

```sh
phi ws up
```

Open [localhost:9095](http://localhost:9095) to view the ML Apps.

If something fails, try running again with debug logs:

```sh
phi ws up -d
```

### Shut down workspace

Shut down resources using:

```sh
phi ws down
```
