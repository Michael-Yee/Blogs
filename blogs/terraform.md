---
title: Terraform Basics
author: Michael Yee
published: True
---


# Overview

In this blog, I will describe some fundamentals concepts of Terraform.

## Installation

Download the [Terraform zip archive](https://www.terraform.io/downloads.html) from HashiCorp and unzip it. Test the binary file name Terraform with the following command:

    terraform --version

## Background

Infrastructure as a code (IAC) is the process of managing and provisioning infrastructure through the code instead of physical hardware configuration or interactive configuration tools. With IAC, infrastructure can be provisioned in seconds and scale can be achieved with capacity planning. Terraform is one of the tools which can be used for building, changing, versioning our infrastructure safely and efficiently.

### Configuration

Terraform uses text files to describe infrastructure and to set variables. These text files are called Terraform configurations and end in .tf. 

The format of the configuration files are either in the Terraform format (.tf) or JSON (tf.json). The Terraform format is more human-readable, supports comments, and is the generally recommended format for most Terraform files. In this blog, we will use the Terraform format.

### Load Order and Semantics

When invoking any command that loads the Terraform configuration, Terraform loads all configuration files within the directory specified in alphabetical order.

The order of variables, resources, etc. defined within the configuration doesn't matter. Terraform configurations are declarative, so references to other resources and variables do not depend on the order they're defined.

### Configuration Syntax

The syntax of Terraform configurations is called HashiCorp Configuration Language (HCL).

The following is an example of Terraform's HCL syntax:

```
# An AMI
variable "ami" {
  description = "the AMI to use"
}

/* A multi
   line comment. */
resource "aws_instance" "web" {
  ami               = "${var.ami}"
  count             = 2
  source_dest_check = false

  connection {
    user = "root"
  }
}

  * Single line comments start with #

  * Multi-line comments are wrapped with /* and */

  * Values are assigned with the syntax of key = value (whitespace doesn't matter). The value can be any primitive (string, number, boolean), a list, or a map.

  * Strings are in double-quotes.

  * Strings can interpolate other values using syntax wrapped in ${}, such as ${var.foo}.

  * Multiline strings can use shell-style "here doc" syntax, with the string starting with a marker like <<EOF and then the string ending with EOF on a line of its own. The lines of the string and the end marker must not be indented.

  * Numbers are assumed to be base 10. If you prefix a number with 0x, it is treated as a hexadecimal number.

  * Boolean values: true, false.

  * Lists of primitive types can be made with square brackets ([]). Example: ["foo", "bar", "baz"].

  * Maps can be made with braces ({}) and colons (:): { "foo": "bar", "bar": "baz" }. Quotes may be omitted on keys, unless the key starts with a number, in which case quotes are required. Commas are required between key/value pairs for single line maps. A newline between key/value pairs is sufficient in multi-line maps.
```

In addition to the basics, the syntax supports hierarchies of sections, such as the "resource" and "variable" in the example above. These sections are similar to maps, but visually look better. For example, these are nearly equivalent:

    variable "ami" {
      description = "the AMI to use"
    }

is equal to:

    variable = [{
      "ami": {
        "description": "the AMI to use",
      }
    }]

### Resource

The most important thing you'll configure with Terraform are resources. Resources are a component of your infrastructure. It might be some low level component such as a physical server, virtual machine, or container. Or it can be a higher level component such as an email provider, DNS record, or database provider.

A resource configuration looks like the following:

    resource "aws_instance" "web" {
      ami           = "ami-408c7f28"
      instance_type = "t1.micro"
    }


The resource block creates a resource of the given TYPE (first parameter) and NAME (second parameter). The combination of the type and name must be unique.

Within the block (the { }) is configuration for the resource. The configuration is dependent on the type, and is documented for each resource type in the providers section.

### Data Source

Data sources allow data to be fetched or computed for use elsewhere in Terraform configuration. Use of data sources allows a Terraform configuration to build on information defined outside of Terraform, or defined by another separate Terraform configuration.

Providers are responsible in Terraform for defining and implementing data sources. Whereas a resource causes Terraform to create and manage a new infrastructure component, data sources present read-only views into pre-existing data, or they compute new values on the fly within Terraform itself.

For example, a data source may retrieve artifact information from Terraform Enterprise, configuration information from Consul, or look up a pre-existing AWS resource by filtering on its attributes and tags.

Every data source in Terraform is mapped to a provider based on longest-prefix matching. For example the aws_ami data source would map to the aws provider (if that exists).

A data source configuration looks like the following:

```
# Find the latest available AMI that is tagged with Component = web
data "aws_ami" "web" {
  filter {
    name   = "state"
    values = ["available"]
  }

  filter {
    name   = "tag:Component"
    values = ["web"]
  }

  most_recent = true
}
```

The data block creates a data instance of the given TYPE (first parameter) and NAME (second parameter). The combination of the type and name must be unique.

Within the block (the { }) is configuration for the data instance. The configuration is dependent on the type, and is documented for each data source in the providers section.

Each data instance will export one or more attributes, which can be interpolated into other resources using variables of the form data.TYPE.NAME.ATTR. For example:

    resource "aws_instance" "web" {
      ami           = "${data.aws_ami.web.id}"
      instance_type = "t1.micro"
    }

### Provider

Providers are responsible in Terraform for managing the lifecycle of a resource: create, read, update, delete.

Most providers require some sort of configuration to provide authentication information, endpoint URLs, etc. Where explicit configuration is required, a provider block is used within the configuration as illustrated in the following sections.

By default, resources are matched with provider configurations by matching the start of the resource name. For example, a resource of type vsphere_virtual_machine is associated with a provider called vsphere.

A provider configuration looks like the following:

    provider "aws" {
      access_key = "foo"
      secret_key = "bar"
      region     = "us-east-1"
    }


A provider block represents a configuration for the provider named in its header. For example, provider "aws" above is a configuration for the aws provider.

Within the block body (between { }) is configuration for the provider. The configuration is dependent on the type, and is documented for each provider.

The arguments alias and version, if present, are special arguments handled by Terraform Core for their respective features described above. All other arguments are defined by the provider itself.

### Input Variable

Input variables serve as parameters for a Terraform module.

Input variables can be defined as follows:

```
variable "key" {
  type    = "string"
  default = "value"
}

variable "long_key" {
  type = "string"
  default = <<EOF
This is a long key.
Running over several lines.
EOF
}

variable "images" {
  type    = "map"
  default = {
    "us-east-1" = "image-1234"
    "us-west-2" = "image-4567"
  }
}

variable "zones" {
  type    = "list"
  default = ["us-east-1a", "us-east-1b"]
}

variable "active" {
  default = false
}
```

The variable block configures a single input variable for a Terraform module. Each block declares a single variable.

### Environment Variables

Environment variables can be used to set the value of an input variable in the root module. The name of the environment variable must be TF_VAR_ followed by the variable name, and the value is the value of the variable.

For example, given the configuration below:

    variable "image" {}

The variable can be set via an environment variable:

    $ TF_VAR_image=foo terraform apply

Maps and lists can be specified using environment variables as well using HCL syntax in the value.

For a list variable like so:

    variable "somelist" {
      type = "list"
    }

The variable could be set like so:

    $ TF_VAR_somelist='["ami-abc123", "ami-bcd234"]' terraform plan

Similarly, for a map declared like:

    variable "somemap" {
      type = "map"
    }

The value can be set like this:

    $ TF_VAR_somemap='{foo = "bar", baz = "qux"}' terraform plan

### Variable Files

Values for the input variables of a root module can be gathered in variable definition files and passed together using the -var-file=FILE option.

For all files which match terraform.tfvars or *.auto.tfvars present in the current directory, Terraform automatically loads them to populate variables. If the file is located somewhere else, you can pass the path to the file using the -var-file flag. It is recommended to name such files with names ending in .tfvars.

Variables files use HCL or JSON syntax to define variable values. Strings, lists or maps may be set in the same manner as the default value in a variable block in Terraform configuration. For example:

```
foo = "bar"
xyz = "abc"

somelist = [
  "one",
  "two",
]

somemap = {
  foo = "bar"
  bax = "qux"
}
```

Note: Variable files are evaluated in the order in which they are specified on the command line. If a particular variable is defined in more than one variable file, the last value specified is effective.

The -var-file flag can be used multiple times per command invocation:

    $ terraform apply -var-file=foo.tfvars -var-file=bar.tfvars

Let's start!

---

## Terraform init

The terraform init command is used to initialize a working directory containing Terraform configuration files. This is the first command that should be run after creating a new Terraform configuration.

    Usage: terraform init [options] [DIR]

NOTE: It is safe to run this command multiple times.

In a folder, we will start by defining a aws_resource.tf file as follows:

    resource "aws_instance" "web" {
      ami           = "ami-0cf31d971a3ca20d6"
      instance_type = "t2.micro"
    }

NOTE: The ami (ami-0cf31d971a3ca20d6) used in this example was created in a previous blog.

In the same folder, we will defining our an aws_provider.tf file as follows:

```
variable access_key {
  type = "string"
  default = "access_key"
  description = "My secret access key"
}

variable secret_key {
  type = "string"
  default = "secret_key"
  description = "My secret access key"
}

provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "us-east-1"
}
```

After the above files are created, run the following command in the same folder:

    $ terrraform init

This command performs several different initialization steps in order to prepare a working directory for use.

Output:

```
Initializing provider plugins...
- Checking for available provider plugins on https://releases.hashicorp.com...
- Downloading plugin for provider "aws" (1.43.2)...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, it is recommended to add version = "..." constraints to the
corresponding provider blocks in configuration, with the constraint strings
suggested below.

* provider.aws: version = "~> 1.43"

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

```

## Terraform plan

The terraform plan command is used to create an execution plan. Terraform performs a refresh, unless explicitly disabled, and then determines what actions are necessary to achieve the desired state specified in the configuration files.

This command is a convenient way to check whether the execution plan for a set of changes matches your expectations without making any changes to real resources or to the state. For example, terraform plan might be run before committing a change to version control, to create confidence that it will behave as expected.

    Usage: terraform plan [options] [dir-or-plan]

NOTE: The optional -out argument can be used to save the generated plan to a file for later execution with terraform apply, which can be useful when running Terraform in automation.

After running terraform init, run the following command in the same folder:

    $ export TF_VAR_access_key="access_key" 
    $ export TF_VAR_secret_key="secret_key" 
    $ terraform plan

View the output to check whether the set of changes matches our expectation without making any real infrastructure changes.

Output:

```
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.


------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  + aws_instance.web
      id:                           <computed>
      ami:                          "ami-0cf31d971a3ca20d6"
      arn:                          <computed>
      associate_public_ip_address:  <computed>
      availability_zone:            <computed>
      cpu_core_count:               <computed>
      cpu_threads_per_core:         <computed>
      ebs_block_device.#:           <computed>
      ephemeral_block_device.#:     <computed>
      get_password_data:            "false"
      instance_state:               <computed>
      instance_type:                "t2.micro"
      ipv6_address_count:           <computed>
      ipv6_addresses.#:             <computed>
      key_name:                     <computed>
      network_interface.#:          <computed>
      network_interface_id:         <computed>
      password_data:                <computed>
      placement_group:              <computed>
      primary_network_interface_id: <computed>
      private_dns:                  <computed>
      private_ip:                   <computed>
      public_dns:                   <computed>
      public_ip:                    <computed>
      root_block_device.#:          <computed>
      security_groups.#:            <computed>
      source_dest_check:            "true"
      subnet_id:                    <computed>
      tenancy:                      <computed>
      volume_tags.%:                <computed>
      vpc_security_group_ids.#:     <computed>


Plan: 1 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.
```

## Terraform apply

The terraform apply command is used to apply the changes required to reach the desired state of the configuration, or the pre-determined set of actions generated by a terraform plan execution plan.

    Usage: terraform apply [options] [dir-or-plan]

After running terraform plan, run the following command in the same folder:

    $ terraform apply

By default, apply scans the current directory for the configuration and applies the changes appropriately. However, a path to another configuration or an execution plan can be provided.

Output:

```
n execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  + aws_instance.web
      id:                           <computed>
      ami:                          "ami-0cf31d971a3ca20d6"
      arn:                          <computed>
      associate_public_ip_address:  <computed>
      availability_zone:            <computed>
      cpu_core_count:               <computed>
      cpu_threads_per_core:         <computed>
      ebs_block_device.#:           <computed>
      ephemeral_block_device.#:     <computed>
      get_password_data:            "false"
      instance_state:               <computed>
      instance_type:                "t2.micro"
      ipv6_address_count:           <computed>
      ipv6_addresses.#:             <computed>
      key_name:                     <computed>
      network_interface.#:          <computed>
      network_interface_id:         <computed>
      password_data:                <computed>
      placement_group:              <computed>
      primary_network_interface_id: <computed>
      private_dns:                  <computed>
      private_ip:                   <computed>
      public_dns:                   <computed>
      public_ip:                    <computed>
      root_block_device.#:          <computed>
      security_groups.#:            <computed>
      source_dest_check:            "true"
      subnet_id:                    <computed>
      tenancy:                      <computed>
      volume_tags.%:                <computed>
      vpc_security_group_ids.#:     <computed>


Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```

At this point, type in yes to create your resource and sit back and wait for all the operations to be applied on AWS. 

Further output:

```
  Enter a value: yes

aws_instance.web: Creating...
  ami:                          "" => "ami-09c624b6cc0ab6e61"
  arn:                          "" => "<computed>"
  associate_public_ip_address:  "" => "<computed>"
  availability_zone:            "" => "<computed>"
  cpu_core_count:               "" => "<computed>"
  cpu_threads_per_core:         "" => "<computed>"
  ebs_block_device.#:           "" => "<computed>"
  ephemeral_block_device.#:     "" => "<computed>"
  get_password_data:            "" => "false"
  instance_state:               "" => "<computed>"
  instance_type:                "" => "t2.micro"
  ipv6_address_count:           "" => "<computed>"
  ipv6_addresses.#:             "" => "<computed>"
  key_name:                     "" => "<computed>"
  network_interface.#:          "" => "<computed>"
  network_interface_id:         "" => "<computed>"
  password_data:                "" => "<computed>"
  placement_group:              "" => "<computed>"
  primary_network_interface_id: "" => "<computed>"
  private_dns:                  "" => "<computed>"
  private_ip:                   "" => "<computed>"
  public_dns:                   "" => "<computed>"
  public_ip:                    "" => "<computed>"
  root_block_device.#:          "" => "<computed>"
  security_groups.#:            "" => "<computed>"
  source_dest_check:            "" => "true"
  subnet_id:                    "" => "<computed>"
  tenancy:                      "" => "<computed>"
  volume_tags.%:                "" => "<computed>"
  vpc_security_group_ids.#:     "" => "<computed>"
aws_instance.web: Still creating... (10s elapsed)
aws_instance.web: Still creating... (20s elapsed)
aws_instance.web: Still creating... (30s elapsed)
aws_instance.web: Creation complete after 34s (ID: i-0a2e7eb36434b5bd8)

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

```

NOTE: Ine the EC2 Dashbboard, you should see the instance now running.

In the folder where the .tf files were created, Terraform has generatred a terraform.tfstate file. This file records the configuration state of the applied plan. 

## Terraform destroy

The terraform destroy command is used to destroy the Terraform-managed infrastructure.

    Usage: terraform destroy [options] [dir]

When you are satified with this demo, run the following command in the same folder:

    $ terraform destroy

Output:

```
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  - aws_instance.web


Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: 

```

Infrastructure managed by Terraform will be destroyed. This will ask for confirmation before destroying.

Further output:

```
  Enter a value: yes

aws_instance.web: Destroying... (ID: i-0a2e7eb36434b5bd8)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 10s elapsed)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 20s elapsed)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 30s elapsed)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 40s elapsed)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 50s elapsed)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 1m0s elapsed)
aws_instance.web: Still destroying... (ID: i-0a2e7eb36434b5bd8, 1m10s elapsed)
aws_instance.web: Destruction complete after 1m12s

Destroy complete! Resources: 1 destroyed.
```

NOTE: Ine the EC2 Dashbboard, you should see the instance now terminated.

# Conclusion

Terraform uses an infrastructure as code approach to provide effective, reusable, and safe infrastructure provisioning automation. This approach enables operators to increase their productivity, move quicker, and reduce human error.
