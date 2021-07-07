# Workshop Serverless 101

Serverless computing is a  modern approach to computing which changes the way we build, deploy manage and consume infrastructure. In the past when building software you would deploy the needed resources in terms of hardware or virtual machines then deploy your code ontop of that. Serverless changes this way of working and means rather than paying for the infrastructure which your application or service will run on a 24/7 basis you are charged per execution of your code.

You may also see serverles referred to as "Function as a Service", as all you as the developer really need to do is provide your code and the cloud provider will handle all the other complexity around providing an infrastructure to run your code. This isn't always necessarily as easy as it sounds, but we'll go onto explore more here in this lab and give you atleast an idea how you as a developer can start to leverage Serverless.

In this lab, we're going to create a simple serverless function which will return a status code of 200 when called and include a joke which the Python code dynamically pulls from an API everytime the code runs. For the purposes of this lab we're going to use probably the most popular serverless technology available today AWS Lambda, however there are many other examples of Serverless functions also available from other cloud providers including Azure and Google.

## Packaging up our code and creating a Lambda function

In this section we're going to get into building our code and deploying. One of the first idiosyncracies of we need to get our head round using Lambda is how we package up and upload our code to the service, especially if you have library dependancies in Python which you need to package up with your code, in this example function we have to do this for the requests module which isn't included in the Lambda python interpreter and has to be uploaded as a package at the same time we upload our code. We'll get onto how we do this later but first lets start with our code, you can either clone this repo and find it in the 'code' directory or create a file called main.py and copy the below in. 

```Python
import json
import requests

def main(event, context):

    joke = getJoke()

    return {
        'statusCode': 200,
        'body': json.dumps(joke)
    }


def getJoke():

    url = "https://icanhazdadjoke.com"
    headers = {
        "Accept":"application/json"
    }

    response = requests.request("GET", url=url, headers=headers)
    return response.json()["joke"]

```

As you can see our code is fairly simple. We have two functions, the first main() calls the function getJoke() and then returns the output of the function to the user with a status code of 200. The second function getJoke() calls out to an API from icanhazdadjoke.com and gets a random joke from its database.

As we're using the requests library to make an API call to this joke API we need to get our dependancies saved locally then package them in a zip file. To downlaod the our libraries in a new, project-local package directory we can use the pip command with the --target option.

```bash
pip install --target ./package requests
cd package
```

Now thats done and we have the newly created ./package as a current directory, create a ZIP archive of the dependencies. 

```bash 
zip -r9 ${OLDPWD}/function.zip .
```

And add your functions code to the ZIP archive also.

```
cd $OLDPWD
zip -g function.zip main.py
```

![](./images/create-zip.gif)

Now you have your function.zip archive, it's time to upload this to your Lambda function. But first lets create a Lambda function. To do this search for the "Lambda" service from your management console on AWS and go to the function section, from there you should see the "Create function" option, select this and use the create from scratch wizard to create your function (ensure the runtime is set to Python 3.8).

![](./images/lambda-create.gif)

Now that the function has been created, upload your newly created function.zip archive which hosts your code and packages, you can find this from the actions button under the "Function code" section,

![](./images/zip-upload.gif)

Now our code is uploaded to the function we have to edit some of the settings for when the code is run, scroll down the page to "Basic settings" and press edit, we need to change the handler to "main.main" this means when the function runs it will look in the main.py file and run the main() function. This is your entrypoint for the Lambda function. Remember this when you design your code as you can only invoke a single function in a lambda event.

![](./images/change-handler.gif)

## Building an API gateway

Now we have our function ready we need a way to invoke the function from an event. In this example we're going to do this through invoking an API that we're going to create from AWS's API gateway service

As you get more advanced, you can add extra layers of authentication and additional features to the API. But for this example we're going to keep it simple.

First we need to create our API gateway, to do this search for the "API Gateway" service from your management console on AWS and go to the function section, from there you should see the "Create API" option, select this and use the create from scratch wizard to create your function (ensure the runtime is set to Python 3.8).

![](./images/create-gateway.gif)

Once you've created your gateway, it's time to add some resources and methods. From the resources section, select actions and click on create resource. This will be the REST endpoint that you're API will serve. Once you've gave it a name then select create method and select "GET"

![](./images/create-method.gif)

## Invoking our API

Now all thats left to do is to test out our API and invoke our function. 

![](./images/invoke-api.gif)

Now all that's left to do is deploy your API. Using the "deploy API" option from the actions drop down. Create a new stage, call it whatever you want here. 

![](./images/deploy-api.gif)

Congratulations, you've just set up your first Lambda function and built your first API gateway! Great work!
