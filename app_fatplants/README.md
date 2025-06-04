# Fatplants API


## Steps needed in order to use and deploy api:
    - clone the repo to desire location. Repo link "https://github.com/akhil6297/fastapi-fatplants.git"
    - create config file and enter your confidential credentials (REMEMBER to add this to gitignore file)
    - create auth_docker directory and add the SSL certificates as `fullchain.pem` and `privkey.pem` (REMEMBER to add this to gitignore file)
    - create auth directory and make credential.py file for accessing creds from config file.
  

# serve API (Outside Docker) for local testing:
`uvicorn main:app --reload`


# To serve API in Docker:
`docker build -t fastapi_fatplants.v1 .`
`docker run -d -v /home/fatplants_volume:/app/fatplants_volume -p 5000:5000 --network=host fastapi_fatplants.v1`

# For dev:
`docker build -f Dockerfile.dev -t fastapi_fatplants .`
`docker run -d -v /home/fatplants_volume:/app/fatplants_volume -p 5004:5004 --network=host fastapi_fatplants`

# Renew of SSL certificates
    - Usually certificates are automatically renewed every two months in their respective path
    - CronJob to automatically copy those SSL files to corresponding folder has been set up (every one hour now)
    - You can check that using "sudo crontab -l", as cronjob is run by Root(sudo) user
    - Cronjob uses shell script "ssl_certs_copy.sh" in /home directory.
    - EDIT the file "ssl_certs_copy.sh" and "sudo cronjob" to change the variables as per the user and their paths.

# Server permission issue:
lsof -i :5000
kill PID


