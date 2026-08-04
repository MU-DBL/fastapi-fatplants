# Fatplants API Developer Guide

## Developing

### Following the steps if you are running Windows:

1. Download Git Bash ([https://gitforwindows.org/](https://gitforwindows.org/)) to use Git commands.

2. Clone the repo using `git clone https://github.com/MU-DBL/fastapi-fatplants.git`.

3. Download Docker at [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

4. Go to `'fastapi-fatplants\app_fatplants'`, create a folder called `'fatplants_volume'` (make sure it’s included in the `.gitignore` file).

5. Paste your config file `'config-dev.yaml'` that contains your confidential credentials in `'fatplants_volume'`.

6. Use the command `docker build -f Dockerfile.dev -t fastapi_fatplants .` to dockerize the project files.

7. Open Docker Desktop, go to the `'Images'` tab, and click the run button on the row of `'fastapi_fatplants'`.

8. Expand `'Optional settings'`, enter `5004` to the first `'Host port'` and `8080` to the second `'Host port'` if it exists.

9. Click `'Run'`.

10. Once the container is running, go to `http://localhost:5004/`, you should see a welcome message in your web browser.

---

### Following the steps if you are running macOS:

1. Open Terminal to use command-line tools.

2. Clone the repo using `git clone https://github.com/MU-DBL/fastapi-fatplants.git`.

3. Navigate to the project directory: `cd fastapi-fatplants/app_fatplants`.

4. Create a folder called `'fatplants_volume'` inside `'app_fatplants'` (make sure it’s included in the `.gitignore` file).

5. Use the command `docker build -f Dockerfile.dev -t fastapi_fatplants .` to dockerize the project files.

6. Open Docker Desktop, go to the `'Images'` tab, and click the run button on the row of `'fastapi_fatplants'`.

7. Expand `'Optional settings'`, enter `5004` to the first `'Host port'` and `8080` to the second `'Host port'` if it exists.

8. Click `'Run'`.

9. Once the container is running, go to `http://localhost:5004/`, you should see a welcome message in your web browser.

---

## Deploying

(to be done)


