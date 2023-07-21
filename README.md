# serverless-saleor-app-example
Example implementation of Saleor app using AWS Lambda. It provides a serverless, cost-effective way to extend Saleor's API.
By using this approach, you could for example listen to Saleor webhooks about Orders and inject them into your existing ERP system.

# Architecture

This project uses AWS Lambda as compute platform and API Gateway as a proxy.
For storing API keys from Saleor, it uses AWS Secret manager.
Application uses FastAPI and could be easily deployed to AWS Lambda, thanks to the awesome `magnum <https://github.com/jordaneremieff/mangum>`_ project!

# Deployment

1. Build and deploy lambda with `./build.sh`.
2. Upload the `artifact.zip` to s3 bucket.
1. Use provided sample terraform code.

You are all set! The app is ready to be connected with Saleor.

# Connect with Saleor

The example app exposes all the endpoints needed to act as a proper Saleor App.
All you need to do is to enter Saleor Dashboard and install the application using Manifest URL.
Manifest URL is `https://<your API gateway URL>/manifest.json`
Now once you click on your app name in the Dashboard, you'll see content rendered by the `/app` endpoint (the one defined as `appUrl` in the manifest).


# Development

Using moto you can set up a local parameter store mock. The easiest way to work on your app is to use moto with unit/integration tests.

Happy coding!


**Crafted with ❤️ by [Mirumee Software](http://mirumee.com)**
