# Fatplants API


## Steps needed in order to use and deploy api:
    - clone the repo to desire location. Repo link "https://github.com/akhil6297/fastapi-fatplants.git"
    - create config file and enter your confidential credentials (REMEMBER to add this to gitignore file)
    - create auth_docker directory and add the SSL certificates as `fullchain.pem` and `privkey.pem` (REMEMBER to add this to gitignore file)
    - create auth directory and make credential.py file for accessing creds from config file.
  

# serve API (Outside Docker) for local testing:
`uvicorn main:app --reload`


# To serve API in Docker:

`mkdir auth_docker && cd auth_docker && sudo cp /etc/letsencrypt/live/<domain>/fullchain.pem . && sudo cp /etc/letsencrypt/live/<domain>/privkey.pem .`
`chmod 666 fullchain.pem && chmod 666 privkey.pem`
`docker build -t fastapi_fatplants.v1 .`
`docker run -d -p 5000:5000 --name fatplants_backend --network=host fastapi_fatplants.v1`
<!-- If you want to mount ssl certificates folder automatically mount the folder onto docker -->
`docker run -d -v ssl_volume:/app/auth_docker -v fatplants_volume:/app/fatplants_volume -p 5000:5000 --name fatplants_backend --network=host fastapi_fatplants.v1`

# For dev:

`sudo docker build -f Dockerfile.dev -t fastapi_fatplants .`
<!-- In case you want to develop rapidly and check USE volumes in below command (-v) thats mounted on to docker container, Else remove "-v container_volume:/app" from below command -->
`sudo docker run -v fatplants_volume:/app/fatplants_volume -p 5004:5004 --network=host fastapi_fatplants`

# Renew domain name
`Renew the domain name in No-IP site every month, as it requires confirmation every month for free tier account`

# Renew of SSL certificates
    - Usually certificates are automatically renewed every two months in their respective path
    - CronJob to automatically copy those SSL files to corresponding folder has been set up (every one hour now)
    - You can check that using "sudo crontab -l", as cronjob is run by Root(sudo) user
    - Cronjob uses shell script "ssl_certs_copy.sh" in /home directory.
    - EDIT the file "ssl_certs_copy.sh" and "sudo cronjob" to change the variables as per the user and their paths.



