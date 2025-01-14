# Average word vector

Using Serverless to create an AWS lambda to save transformed data into OpenSearch and query the transformed data


## Deployment instructions

> **Requirements**: Docker. In order to build images locally and push them to ECR, you need to have Docker installed on your local machine. Please refer to [official documentation](https://docs.docker.com/get-docker/).

In order to deploy the service, run the following command

```
sls deploy
```

## APi Usage


### Create a query

curl -X POST https://XXXXXXX.execute-api.us-east-1.amazonaws.com/query --data '{ "index": "average-word-vectors", "size": 3, "keywords": ["test"], "k": 3 }'


Parameters
- index: Index to query
- size: Number of results to return
- keywords: An array of a single or mutliple words
- k: number of nearest neighbouts considered in the analysis


##  TODO:

- APi Basic Authentication
- APi timeout
- Behaviour for records with no keywords (null vectors?)
- Unit tests


References:

- Container Image Support for AWS Lambda[Container Image Support for AWS Lambda](https://www.serverless.com/blog/container-support-for-lambda)
