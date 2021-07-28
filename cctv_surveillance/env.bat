# base or home directory of the container
set DOCKER_HOME=/usr/app

# dynamic code shared from host to container (for local testing)
set DOCKER_SANDBOX=/usr/app/sandbox

# location where code is cloned inside the container (for deployment)
set DOCKER_CHECKOUT=/usr/app/Video-Analytics


# !!! Modify following variable to suit your computing environment !!!
set MOVIE_FILES=c:\\Temp
# assign it to either DOCKER_SANDBOX or DOCKER_CHECKOUT above
set DOCKER_CODE=/usr/app/sandbox
