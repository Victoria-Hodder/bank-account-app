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


## Testing the endpoints

Though you can use the browser, I used postman to test the different http requests. This way it is much easier to swap between different methods.

For example if you are using POST method to create a new user, you would enter the url: http://127.0.0.1:5000/users

Then enter a json body (for example)...

```
{
    "name": "Maya",
    "address": "North Street, Glasgow"
    "pin": "9876",
    "balance": 2500
}
```

...which would add a new user by the name of "Maya" in your database. An id will be automatically created for you.

You can download and learn more about postman here https://www.postman.com/

## Testing the app

... Documentation to follow ...
