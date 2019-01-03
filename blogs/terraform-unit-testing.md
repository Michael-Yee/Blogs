---
title: Infrastructure as Code (IaC): Testing strategies (is this a thing?)
author: Michael Yee
published: True
---


# Overview

In this blog, I will discuss a couple strategies to test Terraform code.

NOTE: This blog assumes the reader has an understanding of AWS cloud platform and Terraform.


## Introduction

In the short time that I have been working with Terraform, it seems to be THE TOOL for deploying and provision Infrastructure as Code (IaC) on any platform. As I visit blogs, GitHub repositories, official documentation, etc... to better understand best practices, there tends to be one topic that is either briefly mentioned or totally omitted: **IaC testing**.


## Structure

The [standard module structure](https://www.terraform.io/docs/modules/create.html#standard-module-structure) is a file and folder layout Terraform recommends when using modules. The files of interest for this blog will be found in modules and tests folders.

```
├── README.md
├── main.tf
├── outputs.tf
├── variables.tf
├── examples
├── ...
├── tests
│   ├─ ec2
│   │  ├─ terraform_EC2_example_test.go
│   
├── modules
	├─ ec2
    │  ├─ README.md
    │  ├─ main.tf
    │  ├─ outputs.tf
    │  ├─ variables.tf

```


## File contents

main.tf

```
# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY AN EC2 INSTANCE RUNNING RABBITMQ
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_instance" "production_rabbitmq" {
  ami           = "${data.aws_ami.rabbitmq_ami.id}"
  instance_type = "t2.micro"

  tags {
    Name = "${var.instance_name}"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# LOOK UP THE LATEST RABBITMQ AMI
# ---------------------------------------------------------------------------------------------------------------------

data "aws_ami" "rabbitmq_ami" {
  most_recent = true
  owners      = ["679593333241"] 

  filter {
    name   = "state"
    values = ["available"]
  }

  filter {
    name   = "name"
    values = ["bitnami-rabbitmq-3.7.9-0-linux-ubuntu-16.04-x86_64*"]
  }
}

```

outputs.tf
```
output "instance_id" {
  value = "${aws_instance.production_rabbitmq.id}"
}

```

variables.tf
```
# ---------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# Define these secrets as environment variables
# ---------------------------------------------------------------------------------------------------------------------


# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_DEFAULT_REGION


# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# You must provide a value for each of these parameters.
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# These parameters have reasonable defaults.
# ---------------------------------------------------------------------------------------------------------------------


variable "instance_name" {
  description = "The Name tag to set for the EC2 Instance."
  default     = "terraform-testing-example"
}
```

terraform_EC2_example_test.go
```
package test

import (
    "testing"

    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

// An example of how to test the Terraform module in modules/ec2 using Terratest.
func TestTerraformAwsExample(t *testing.T) {
    t.Parallel()

    // Define the name of the EC2 instance
    expectedName := "terraform-testing-example"

    // Define the AWS region to test within. To run the test in a random regions -> awsRegion := aws.GetRandomStableRegion(t, nil, nil) 
    awsRegion := "us-east-2"

    terraformOptions := &terraform.Options{
        // The path to where our Terraform code is located
        TerraformDir: "../../modules/ec2",

        // Variables to pass to our Terraform code using -var options
        Vars: map[string]interface{}{
            "instance_name": expectedName,
        },

        // Environment variables to set when running Terraform
        EnvVars: map[string]string{
            "AWS_DEFAULT_REGION": awsRegion,
        },
    }

    // At the end of the test, run `terraform destroy` to clean up any resources that were created
    defer terraform.Destroy(t, terraformOptions)

    // This will run `terraform init` and `terraform apply` and fail the test if there are any errors
    terraform.InitAndApply(t, terraformOptions)

    // Run `terraform output` to get the value of an output variable
    instanceID := terraform.Output(t, terraformOptions, "instance_id")

    aws.AddTagsToResource(t, awsRegion, instanceID, map[string]string{"testing": "testing-tag-value"})

    // Look up the tags for the given Instance ID
    instanceTags := aws.GetTagsForEc2Instance(t, awsRegion, instanceID)

    testingTag, containsTestingTag := instanceTags["testing"]
    assert.True(t, containsTestingTag)
    assert.Equal(t, "testing-tag-value", testingTag)

    // Verify that our expected name tag is one of the tags
    nameTag, containsNameTag := instanceTags["Name"]
    assert.True(t, containsNameTag)
    assert.Equal(t, expectedName, nameTag)
}

```


## Test Strategy ONE: terraform plan

If your infrastructure is as simple as spinning up an EC2 instance, maybe "eyeballing" it with *terraform plan* is all you need. This command is a convenient way to check whether the execution plan for a set of changes matches your expectations without making any changes to real resources or to the state. 

```
Advantages: 
    Quick development time 
    Shallow learning curve

Disadvantages:
    Hard to spot mistakes
    Scaling issues
```

---

Over the Xmas break, I went searching for a tool to that could test the Terraform code I was producing...  I have investigated a few tools as following:

[InSpec-Iggy](https://github.com/inspec/inspec-iggy) an InSpec plugin for generating compliance controls and profiles from Terraform tfstate files and AWS CloudFormation templates.

[Kitchen-Terraform](https://github.com/newcontext-oss/kitchen-terraform) provides a set of Test Kitchen plugins which enable a system to use Test Kitchen to converge a Terraform configuration and verify the resulting Terraform state with InSpec controls.

[Goss](https://github.com/aelsabbahy/goss) is a YAML based serverspec tool for validating a server’s configuration.

[Terraform Validate](https://github.com/elmundio87/terraform_validate) allows users to define Policy as Code for Terraform configurations.

[Terratest](https://github.com/gruntwork-io/terratest) is a Go library that makes it easier to write automated tests for Terraform code. It provides a variety of helper functions and patterns for common infrastructure testing tasks.

In the end, I have decided to put some time into learning Terratest due to various reasons... open source, decent documentation, current and well maintained, etc...


## Test Strategy TWO: Terratest


### Installation

Prerequisite: install [Go](https://golang.org/).

To add Terratest to your projects, 

```bash
go get github.com/gruntwork-io/terratest/modules/aws
go get github.com/gruntwork-io/terratest/modules/terraform

```

To run a test you need to provide a Terraform file and a Go test. Then you simply call 'go test' and Terratest takes care of 'init' and 'apply' the infrastructure. It performs some tests then 'destroy'.


go test
```
TestTerraformAwsExample 2019-01-03T16:42:20-05:00 retry.go:69: Running terraform [init -upgrade=false]
TestTerraformAwsExample 2019-01-03T16:42:20-05:00 command.go:53: Running command terraform with args [init -upgrade=false]
TestTerraformAwsExample 2019-01-03T16:42:20-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:20-05:00 command.go:121: Initializing provider plugins...
TestTerraformAwsExample 2019-01-03T16:42:20-05:00 command.go:121: - Checking for available provider plugins on https://releases.hashicorp.com...
TestTerraformAwsExample 2019-01-03T16:42:20-05:00 command.go:121: - Downloading plugin for provider "aws" (1.54.0)...
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: The following providers do not have any version constraints in configuration,
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: so the latest version was installed.
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: To prevent automatic upgrades to new major versions that may contain breaking
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: changes, it is recommended to add version = "..." constraints to the
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: corresponding provider blocks in configuration, with the constraint strings
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: suggested below.
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: * provider.aws: version = "~> 1.54"
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: Terraform has been successfully initialized!
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: You may now begin working with Terraform. Try running "terraform plan" to see
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: any changes that are required for your infrastructure. All Terraform commands
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: should now work.
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: If you ever set or change modules or backend configuration for Terraform,
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: rerun this command to reinitialize your working directory. If you forget, other
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:121: commands will detect it and remind you to do so if necessary.
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 retry.go:69: Running terraform [get -update]
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:53: Running command terraform with args [get -update]
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 retry.go:69: Running terraform [apply -input=false -lock=false -auto-approve -var instance_name="terraform-testing-example"]
TestTerraformAwsExample 2019-01-03T16:42:24-05:00 command.go:53: Running command terraform with args [apply -input=false -lock=false -auto-approve -var instance_name="terraform-testing-example"]
TestTerraformAwsExample 2019-01-03T16:42:26-05:00 command.go:121: data.aws_ami.rabbitmq_ami: Refreshing state...
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121: aws_instance.production_rabbitmq: Creating...
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   ami:                          "" => "ami-0414159cd18f9449f"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   arn:                          "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   associate_public_ip_address:  "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   availability_zone:            "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   cpu_core_count:               "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   cpu_threads_per_core:         "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   ebs_block_device.#:           "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   ephemeral_block_device.#:     "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   get_password_data:            "" => "false"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   host_id:                      "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   instance_state:               "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   instance_type:                "" => "t2.micro"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   ipv6_address_count:           "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   ipv6_addresses.#:             "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   key_name:                     "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   network_interface.#:          "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   network_interface_id:         "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   password_data:                "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   placement_group:              "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   primary_network_interface_id: "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   private_dns:                  "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   private_ip:                   "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   public_dns:                   "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   public_ip:                    "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   root_block_device.#:          "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   security_groups.#:            "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   source_dest_check:            "" => "true"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   subnet_id:                    "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   tags.%:                       "" => "1"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   tags.Name:                    "" => "terraform-testing-example"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   tenancy:                      "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   volume_tags.%:                "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:29-05:00 command.go:121:   vpc_security_group_ids.#:     "" => "<computed>"
TestTerraformAwsExample 2019-01-03T16:42:39-05:00 command.go:121: aws_instance.production_rabbitmq: Still creating... (10s elapsed)
TestTerraformAwsExample 2019-01-03T16:42:49-05:00 command.go:121: aws_instance.production_rabbitmq: Still creating... (20s elapsed)
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: aws_instance.production_rabbitmq: Creation complete after 24s (ID: i-08e98b4aec5824979)
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: Outputs:
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: instance_id = i-08e98b4aec5824979
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 retry.go:69: Running terraform [output -no-color instance_id]
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:53: Running command terraform with args [output -no-color instance_id]
TestTerraformAwsExample 2019-01-03T16:42:52-05:00 command.go:121: i-08e98b4aec5824979
TestTerraformAwsExample 2019-01-03T16:42:53-05:00 retry.go:69: Running terraform [destroy -auto-approve -input=false -lock=false -var instance_name="terraform-testing-example"]
TestTerraformAwsExample 2019-01-03T16:42:53-05:00 command.go:53: Running command terraform with args [destroy -auto-approve -input=false -lock=false -var instance_name="terraform-testing-example"]
TestTerraformAwsExample 2019-01-03T16:42:55-05:00 command.go:121: data.aws_ami.rabbitmq_ami: Refreshing state...
TestTerraformAwsExample 2019-01-03T16:42:55-05:00 command.go:121: aws_instance.production_rabbitmq: Refreshing state... (ID: i-08e98b4aec5824979)
TestTerraformAwsExample 2019-01-03T16:42:58-05:00 command.go:121: aws_instance.production_rabbitmq: Destroying... (ID: i-08e98b4aec5824979)
TestTerraformAwsExample 2019-01-03T16:43:08-05:00 command.go:121: aws_instance.production_rabbitmq: Still destroying... (ID: i-08e98b4aec5824979, 10s elapsed)
TestTerraformAwsExample 2019-01-03T16:43:18-05:00 command.go:121: aws_instance.production_rabbitmq: Still destroying... (ID: i-08e98b4aec5824979, 20s elapsed)
TestTerraformAwsExample 2019-01-03T16:43:28-05:00 command.go:121: aws_instance.production_rabbitmq: Still destroying... (ID: i-08e98b4aec5824979, 30s elapsed)
TestTerraformAwsExample 2019-01-03T16:43:38-05:00 command.go:121: aws_instance.production_rabbitmq: Still destroying... (ID: i-08e98b4aec5824979, 40s elapsed)
TestTerraformAwsExample 2019-01-03T16:43:48-05:00 command.go:121: aws_instance.production_rabbitmq: Still destroying... (ID: i-08e98b4aec5824979, 50s elapsed)
TestTerraformAwsExample 2019-01-03T16:43:49-05:00 command.go:121: aws_instance.production_rabbitmq: Destruction complete after 51s
TestTerraformAwsExample 2019-01-03T16:43:49-05:00 command.go:121: 
TestTerraformAwsExample 2019-01-03T16:43:49-05:00 command.go:121: Destroy complete! Resources: 1 destroyed.
PASS
ok      _/Users/michael/Blogs/code/terraform-testing-demo/tests/ec2   89.789s
```

NOTE:  Multiply test could be run in parallel using Terratest

```
Advantages:
    Environments can be spun up with ease
    Documents the infrastructure
    Allows for version tagging of your infrastructure

Disadvantages:
    Super slow
    AWS costs
    Who know Go around here?
```


# Conclusion

Terratest provides a whole range of Go modules to help with IaC testing. 

All the test could run in a CI pipeline with 'cd tests ; go test -v ./...' and a global pass/fail will be outputted. 
