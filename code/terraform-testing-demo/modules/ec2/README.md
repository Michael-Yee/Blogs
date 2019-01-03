# Terraform EC2 Example

This folder contains a simple Terraform module that deploys resources in [AWS](https://aws.amazon.com/) to demonstrate
how you can write automated tests for your Terraform code. This module deploys an [EC2
Instance](https://aws.amazon.com/ec2/) and gives that Instance a `Name` tag with the value specified in the
`instance_name` variable.


**WARNING**: This module and the automated tests for it deploy real resources into your AWS account which can cost you
money. The resources are all part of the [AWS Free Tier](https://aws.amazon.com/free/), so if you haven't used that up,
it should be free, but you are completely responsible for all AWS charges.


## Running this module manually

1. Sign up for [AWS](https://aws.amazon.com/).
2. Configure your AWS credentials using one of the [supported methods for AWS CLI
   tools](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), such as setting the
   `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. If you're using the `~/.aws/config` file for profiles then export `AWS_SDK_LOAD_CONFIG` as "True".
3. Set the AWS region you want to use as the environment variable `AWS_DEFAULT_REGION`.
4. Install [Terraform](https://www.terraform.io/) and make sure it's on your `PATH`.
5. Run `terraform init`.
6. Run `terraform apply`.
7. When you're done, run `terraform destroy`.


## Running Terratest against this module

1. Sign up for [AWS](https://aws.amazon.com/).
2. Configure your AWS credentials using one of the [supported methods for AWS CLI
   tools](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), such as setting the
   `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. If you're using the `~/.aws/config` file for profiles then export `AWS_SDK_LOAD_CONFIG` as "True".
3. Install [Terraform](https://www.terraform.io/) and make sure it's on your `PATH`.
4. Install [Golang](https://golang.org/) and make sure this code is checked out into your `GOPATH`.
5. `cd tests/ec2`
6. `go get github.com/gruntwork-io/terratest/modules/aws`
7. `go get github.com/gruntwork-io/terratest/modules/terraform`
8. `go test`
