---
title: Docker or Vagrant for a software development environment?
author: Michael Yee
published: True
---

# Overview

In this blog, I will perform a general evaluation between Docker and Vagrant to understand which tool would be the best suited for a software development environment.

## Background

What is Docker?

[Docker](https://www.docker.com/) is a tool designed to ease the creation, deployment and execution of an application by using container images. A DockerFile is a text document that contains all the commands a user could call on the command line to assemble a container image. A container image is a lightweight, standalone, executable package of software that includes everything needed to execute an application: code, runtime, system tools, system libraries and settings.  

What is Vagrant?

[Vagrant](https://www.vagrantup.com/) is a tool designed to ease the creation, deployment and execution of an application by using virtual machines. Vagrant provides a simple and easy client or extension to manage these virtual machines and an interpreter for the text-based definitions of what each environment looks like, called Vagrantfiles. Once you are connected to the virtual machine, it will behave like any other operating system that you have worked with before.

What is the goal of using either tool?

Using either tool, once a developer configures the tool, there is no longer a need to worry about how to get the application executed on any system every again.

## Let's start!

You might be asking yourself why do I need a software development environment? I press F5 in visual studio and the application executes.

Pros:

    - Minimal effort to execute the application


Cons:

    - Good luck trying to get a Windows application to run on a Linux (or visa versa)
    - Spending hours manually and installing all the dependencies and services on each team members dev machine (if you can remember what you installed (not to speak of versions) and any trick required to get things to work)

So, what is the alternative to using the host OS directly? Go virtual! 

You can execute your application in a virtual machine.  A virtual machine is a fully functioning operating system that exist on top of your host OS. The most popular tool for running a development environment within a virtual machine is with Vagrant.  

Pros:

    - cross-platform portability
    - the virtual machine can execute multiple application
    - dev machine will be isolated from all the dependencies and services required from the project
    - mapping of the code from the host directory to the directory on the virtual machine
    - to set up the virtual machine onto another dev machine is as simple as copying the Vagrantfile(s)

Cons: 

    - the time to create a virtual machine depends on the time to download and install dependencies and services
    - virtual machine cost a certain amount of resources to operate
    - vagrantfile(s) may become too complex to maintain

An equally popular tool uses a design that bundles dependencies and services into a container image. The image does nothing by itself, the image needs to be executed and at this point become a container instance. 

It is best practice to have multiple container images if you are executing more than one application or service. Docker Compose gives you a tool set to link container images together to produce a development environment.
NOTE: Kubernetes was not considered in managing a local development environment as it adds another layer of complexity which is not needed for local development or may have not been identified as a requirement.

Pros: 

    - cross-platform portability
    - development with containers will closely mimic production
    - a container can execute on top of the host OS negating layers of resources
    - dev machine will be isolated from all the dependencies and services required from the project
    - to set up the virtual environment onto other dev machines is as simple as copying the docker-compose and DockerFiles

Cons:

    - using containers adds more layers and increases the complexity of the environment
    - development and maintenance of multiply container images takes time as the project grows
    - a tool is required to manage multiple interacting container images

# The bottom line

In this blog, we have evaluated three development environments: 

Host operating system is not an option.

Virtual machine will replicate most of the qualities of the production environment, but is slow to stand up and does not scale well as your project grows.

Container development will best match your production environment, lends itself throughout the software delivery pipeline and will scale onto cloud as your outgrow your local environment. Although, the complexity of container management is a task not to be taken lightly.
