# AWS CloudFormation thread manager
![Build Status](https://travis-ci.org/vadymbat/aws-cf-concurrency-manager.svg?branch=master)

The CloudFormation doesn't manage or check resource creation limits during the deployment. The macro helps to deal with AWS API throttling during creating a lot of resources e.g. DynamoDB tables via CloudFormation. It creates different resource queues using `DependsOn` statement.

## How to deploy the macro
1. clone the repo

`git clone https://github.com/vadymbat/aws-cf-concurrency-manager.git`

2. prepare CloudFormation template

`aws cloudformation package --s3-bucket <your-s3-bucket> --template-file macro_template.yaml --output-template-file cf_parrallelizer.yaml`

3. deploy the CloudFormation macro

`aws cloudformation deploy --template-file cf_parrallelizer.yaml --stack-name cf-parrallelizer`

## How to use in your CloudFormation template
1. add "Transform" statement `Transform: CfConcurrencyMacro`
2. put `ParallelTaskQuantity: <int>` to the root level of your template to set in how many threads your infrastructure will be deployed 
3. (optional) fill `CommonDependancies: ["<ResourceLogicalId>"]` list of the resources which are dependencies of all resources in the stack

Check the [example template](demo.json) for more details.
