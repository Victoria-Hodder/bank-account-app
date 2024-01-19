# Welcome to my sample banking app

I built this as part of my Frauenloop course on backend development back in 2019. It is simple but still something of great pride to me.

## Getting it running

First of all, set up a virtual environment using your tool of choice.

You can simply create and activate a virtual environment so:

```
# create virutal environment (if bank is the name you want to give to your virtual environment):

~/your_workspace$ python3 -m venv bank

# activate virutal env
~/your_workspace$ source bank/bin/activate

# The environment name in brackets to the left of your workspace indicates the environment is active
(bank) ~/your_workspace$
```

Easy peasy. Now you can install all the necessary libraries to get the project running...

`pip install -r requirements.txt`

Now you have the Python environment ready, you can set up flask in the following way:

```
(bank) ~/your_workspace$ export FLASK_APP=run
(bank) ~/your_workspace$ export FLASK_ENV=development

# Run flask
(bank) ~/your_workspace$ flask run
```

Once your app is running successfully, you should be able to access it on your browser at: http://127.0.0.1:5000


### Fun Fact:
If you don't want to set the environment variables manually every time, it's worth looking into [python-dotenv](https://pypi.org/project/python-dotenv/) (just be sure not to commit anything private to the repo ;))


## Testing the endpoints

Though you can use the browser, I used postman to test the different http requests. This way it is much easier to swap between different methods.

For example if you are using POST method to create a new user, you would enter the url: http://127.0.0.1:5000/users

Then enter a json body (for example)...

```
{
    "name": "Maya",
    "address": "North Street, Glasgow"
    "pin": "9876",
}
```

...which would add a new user by the name of "Maya" in your database. An id will be automatically created for you.

You can download and learn more about postman here https://www.postman.com/

## Testing the app

I use unittest to test the app. You can run them with the following command within the project directory:

`python3 -m unittest bankapp/tests/*.py`

If you wish to run a single test file you can simply replace `*.py` with the name of the file. For example:

`python3 -m unittest bankapp/tests/test_user.py`

## Running on Docker

There is also the possibility to run this project on Docker if you prefer to do that.

To run, simply, run:

```
(bank) ~/your_workspace$ docker build --tag <tag-name-of-your-choice> .
(bank) ~/your_workspace$ docker run -p 5000:5000 <tag-name-of-your-choice>

# To stop your Docker container running ctrl+c usually suffices but you can 
# double check if any instances are still active by running...
(bank) ~/your_workspace$ docker ps

# You can clean up your space after stopping with:
(bank) ~/your_workspace$ docker container prune

```

### Fun fact:
If you are having `permission denied` issues connecting to Docker on your machine (like I do), start all your docker commands with `sudo`. Usually helps.

## Running tests on Docker

Once the container is running, find out its name using `docker ps`. 

The name can be found under NAMES - usually the last column.

Then run:

`docker exec -i <container-name> python3 -m unittest bankapp/tests/*.py`


## Room for improvement with Docker

I would like to explore the possibility of:
- defining a custom container name from the beginning.
- creating a separate Dockerfile for the Tests directory and run the project using docker-compose.

Watch this space.