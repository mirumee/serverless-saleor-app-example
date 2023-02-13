# serverless-saleor-app-example
Example implementation of Saleor app using AWS Lambda. It provides a serverless, cost-effective way to extend Saleor's API.

By using this approach, you could for example listen to Saleor webhooks about Orders and inject them into your existing ERP system.

# Architecture

This project uses AWS Lambda as compute platform and API Gateway as a proxy.
For storing API keys from Saleor, it uses AWS Parameter Store.

Application uses FastAPI and could be easily deployed to AWS Lambda, thanks to the awesome https://github.com/jordaneremieff/mangum project!

# Deployment

1. Create AWS Lambda using console or some IaaC tool. Select Python 3.9 as Runtime
2. If you want to benefit from saving the API keys in Parameter Store, you need to extend the IAM Execution Role of your lambda function. Here is example policy:

Given, that function uses a prefix of `demo.lambda.app` following IAM policy would allow the function to write and read all parameters with this prefix.
You could change the prefix in `config.py`

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:PutParameter",
                "ssm:GetParametersByPath",
                "ssm:GetParameters",
                "ssm:GetParameter"
            ],
            "Resource": "arn:aws:ssm:<Your Region>:<your AWS Account ID>:parameter/demo.lambda.app*"
        },
        {
            "Effect": "Allow",
            "Action": "ssm:DescribeParameters",
            "Resource": "*"
        }
    ]
}

```

3. Create API Gateway - use HTTP API type and enable Lambda integration and use `$default` route for Lambda

![Screenshot 2023-02-13 at 08 54 58](https://user-images.githubusercontent.com/1754812/218401756-53139d72-e510-4fdd-b2c3-515ad79da221.png)
![image](https://user-images.githubusercontent.com/1754812/218401928-f2706096-5134-4939-b5d1-5871c67c22ba.png)

4. Build and deploy lambda

```bash
$ ./build.sh
```
Upload the `artifact.zip` to Lambda

You are all set! The app is ready to be connected with Saleor.

5. Important!  Set up correct path for the lambda handler. It should be set to the `lambda_saleor_app.main.handler` - the object created by Mangum.

![image](https://user-images.githubusercontent.com/1754812/218418266-10b85173-7ad8-41fc-b387-42f3b91a8359.png)


# Connect with Saleor

The example app exposes all the endpoints needed to act as a proper Saleor App.
All you need to do is to enter Saleor Dashboard and install the application using Manifest URL.

Manifest URL is `https://<your API gateway URL>/manifest.json`

![image](https://user-images.githubusercontent.com/1754812/218416679-48dcee60-c646-4270-9b2a-41a4d1a921ba.png)


![image](https://user-images.githubusercontent.com/1754812/218416748-a837d370-b4e0-4aec-9a97-ac6875248b56.png)

![image](https://user-images.githubusercontent.com/1754812/218416975-edd53df2-791b-4421-8302-f7b054220a51.png)


Now once you click to your app name in the Dashboard, you'll see content rendered by the `/app` endpoint (the one defined as `appUrl` in manifest).


Happy coding!


**Crafted with ❤️ by [Mirumee Software](http://mirumee.com)**
