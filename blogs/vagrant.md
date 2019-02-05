---
title: Vagrant for dummies
author: Michael Yee
published: True
---


# Overview

In this blog, I will describe how to setup and teardown Vagrant locally on MacOS and upon AWS.

NOTE: This blog assume the reader has an understanding AWS cloud platform

## Background

What is VirtualBox?

VirtualBox is an open-source general-purpose full virtualizer for x86 hardware, targeted at server, desktop and embedded use. VirtualBox allows additional operating systems to be installed and run as virtual machines. ~ [VirtualBox](https://www.virtualbox.org/)

What is Vagrant?

Vagrant is an open-source software product for building and maintaining portable virtual software development environments,[4] e.g. for VirtualBox, Hyper-V, Docker containers, VMware, and AWS. It tries to simplify software configuration management of virtualizations in order to increase development productivity. Vagrant is written in the Ruby language, but its ecosystem supports development in a few languages. ~ [Vagrant](https://en.wikipedia.org/wiki/Vagrant_(software))

What are Vagrant boxes?

Boxes are the package format for Vagrant environments. A box can be used by anyone on any platform that Vagrant supports to bring up an identical working environment.

The vagrant box utility provides all the functionality for managing boxes. You can read the documentation on the [vagrant box](https://www.vagrantup.com/docs/cli/box.html) command for more information.

The easiest way to use a box is to add a box from the [publicly available catalog of Vagrant boxes](https://app.vagrantup.com). You can also add and share your own customized boxes on this website.

Boxes also support versioning so that members of your team using Vagrant can update the underlying box easily, and the people who create boxes can push fixes and communicate these fixes efficiently.

## Installation

What is Homebrew?

Homebrew is an open-source software package management system that simplifies the installation of software on macOS operating system. It is known as the missing package manager for macOS.

VirtualBox
---

The following is the single command required to install Virtual on macOS using Homebrew

    $ brew cask install virtualbox

The following will is the single command required to verify Vagrant is installated

    $ virtualbox --help

To install the [Oracle VM VirtualBox Extension Pack](https://www.virtualbox.org/wiki/Downloads), navigate to the VirutalBox download page and click the  -> "All supported paltforms" link.  Once downloaded, doubled click on it and it will perform all the necessary installation actions.

Vagrant
---

The following is the single command required to install Vagrant on macOS using Homebrew

    $ brew cask install vagrant

The following will is the single command required to verify Vagrant is installed

    $ vagrant --version

Plugins are a great way to augment or change the behavior and functionality of Vagrant. Plugins are written using Ruby and are packaged using [RubyGems](https://rubygems.org/). You can find many useful plugins on RubyGems like vagrant-aws which enables Vagrant to manage machines on AWS.

The following is the single command required to install vagrant-aws

    $ vagrant plugin install vagrant-aws

The following will is the single command required to verify the plugin is installated

    $ vagrant plugin list


## Let's start!

Setup Vagrant locally
---

Let us first create a folder to contain the new Vagrant environment

    $ mkdir vagrant-tutorial-locally
    $ cd vagrant-tutorial-locally

To initializes a new Vagrant environment, type _vagrant init <boxpath>_, where <boxpath> is the name of Vagrant box. For example, to use the base image of Ubuntu-16.04, type:

    $ vagrant init ubuntu/xenial64

Output:

```
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
```

The _vagrant init_ command creates a file called Vagrantfile that describes the type of machine required and how to configure and provision the machine.

The following is the contents of the newly created Vagrantfile:

```
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end

```

To start the Vagrant enviroment,

    $ vagrant up

The _vagrant up_ command creates, configures and starts a VirtualBox according to your Vagrantfile. On the first run, it automatically downloads the required Vagrant box from the box repository and performs provisioning.

The output is quite long as follows: 

```
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Box 'ubuntu/xenial64' could not be found. Attempting to find and install...
    default: Box Provider: virtualbox
    default: Box Version: >= 0
==> default: Loading metadata for box 'ubuntu/xenial64'
    default: URL: https://vagrantcloud.com/ubuntu/xenial64
==> default: Adding box 'ubuntu/xenial64' (v20190204.3.0) for provider: virtualbox
    default: Downloading: https://vagrantcloud.com/ubuntu/boxes/xenial64/versions/20190204.3.0/providers/virtualbox.box
    default: Download redirected to host: cloud-images.ubuntu.com
==> default: Successfully added box 'ubuntu/xenial64' (v20190204.3.0) for 'virtualbox'!
==> default: Importing base box 'ubuntu/xenial64'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'ubuntu/xenial64' version '20190204.3.0' is up to date...
==> default: Setting the name of the VM: vagrant-tutorial_default_1549396126981_9476
Vagrant is currently configured to create VirtualBox synced folders with
the `SharedFoldersEnableSymlinksCreate` option enabled. If the Vagrant
guest is not trusted, you may want to disable this option. For more
information on this option, please refer to the VirtualBox manual:

  https://www.virtualbox.org/manual/ch04.html#sharedfolders

This option can be disabled globally with an environment variable:

  VAGRANT_DISABLE_VBOXSYMLINKCREATE=1

or on a per folder basis within the Vagrantfile:

  config.vm.synced_folder '/host/path', '/guest/path', SharedFoldersEnableSymlinksCreate: false
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Remote connection disconnect. Retrying...
    default: Warning: Connection reset. Retrying...
    default: 
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default: 
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
Got different reports about installed GuestAdditions version:
Virtualbox on your host claims:   5.0.18
VBoxService inside the vm claims: 5.1.38
Going on, assuming VBoxService is correct...
[default] GuestAdditions versions on your host (6.0.4) and guest (5.1.38) do not match.
Got different reports about installed GuestAdditions version:
Virtualbox on your host claims:   5.0.18
VBoxService inside the vm claims: 5.1.38
Going on, assuming VBoxService is correct...
Reading package lists...
Building dependency tree...
Reading state information...
Package 'virtualbox-guest-dkms' is not installed, so not removed
Package 'virtualbox-guest-x11' is not installed, so not removed
The following packages will be REMOVED:
  virtualbox-guest-utils*
0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
After this operation, 2,338 kB disk space will be freed.
(Reading database ... 54197 files and directories currently installed.)
Removing virtualbox-guest-utils (5.1.38-dfsg-0ubuntu1.16.04.2) ...
Purging configuration files for virtualbox-guest-utils (5.1.38-dfsg-0ubuntu1.16.04.2) ...
Processing triggers for man-db (2.7.5-1) ...
Reading package lists...
Building dependency tree...
Reading state information...
linux-headers-4.4.0-142-generic is already the newest version (4.4.0-142.168).
linux-headers-4.4.0-142-generic set to manually installed.
The following additional packages will be installed:
  binutils cpp cpp-5 fakeroot gcc gcc-5 libasan2 libatomic1 libc-dev-bin
  libc6-dev libcc1-0 libcilkrts5 libfakeroot libgcc-5-dev libgomp1 libisl15
  libitm1 liblsan0 libmpc3 libmpx0 libquadmath0 libtsan0 libubsan0
  linux-libc-dev make manpages-dev
Suggested packages:
  binutils-doc cpp-doc gcc-5-locales gcc-multilib autoconf automake libtool
  flex bison gdb gcc-doc gcc-5-multilib gcc-5-doc libgcc1-dbg libgomp1-dbg
  libitm1-dbg libatomic1-dbg libasan2-dbg liblsan0-dbg libtsan0-dbg
  libubsan0-dbg libcilkrts5-dbg libmpx0-dbg libquadmath0-dbg glibc-doc
  make-doc
The following NEW packages will be installed:
  binutils cpp cpp-5 dkms fakeroot gcc gcc-5 libasan2 libatomic1 libc-dev-bin
  libc6-dev libcc1-0 libcilkrts5 libfakeroot libgcc-5-dev libgomp1 libisl15
  libitm1 liblsan0 libmpc3 libmpx0 libquadmath0 libtsan0 libubsan0
  linux-libc-dev make manpages-dev
0 upgraded, 27 newly installed, 0 to remove and 0 not upgraded.
Need to get 27.6 MB of archives.
After this operation, 101 MB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu xenial/main amd64 libmpc3 amd64 1.0.3-1 [39.7 kB]
Get:2 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 binutils amd64 2.26.1-1ubuntu1~16.04.7 [2,309 kB]
Get:3 http://archive.ubuntu.com/ubuntu xenial/main amd64 libisl15 amd64 0.16.1-1 [524 kB]
Get:4 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 cpp-5 amd64 5.4.0-6ubuntu1~16.04.11 [7,660 kB]
Get:5 http://archive.ubuntu.com/ubuntu xenial/main amd64 cpp amd64 4:5.3.1-1ubuntu1 [27.7 kB]
Get:6 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libcc1-0 amd64 5.4.0-6ubuntu1~16.04.11 [38.8 kB]
Get:7 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libgomp1 amd64 5.4.0-6ubuntu1~16.04.11 [55.0 kB]
Get:8 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libitm1 amd64 5.4.0-6ubuntu1~16.04.11 [27.4 kB]
Get:9 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libatomic1 amd64 5.4.0-6ubuntu1~16.04.11 [8,896 B]
Get:10 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libasan2 amd64 5.4.0-6ubuntu1~16.04.11 [264 kB]
Get:11 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 liblsan0 amd64 5.4.0-6ubuntu1~16.04.11 [105 kB]
Get:12 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libtsan0 amd64 5.4.0-6ubuntu1~16.04.11 [244 kB]
Get:13 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libubsan0 amd64 5.4.0-6ubuntu1~16.04.11 [95.4 kB]
Get:14 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libcilkrts5 amd64 5.4.0-6ubuntu1~16.04.11 [40.1 kB]
Get:15 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libmpx0 amd64 5.4.0-6ubuntu1~16.04.11 [9,748 B]
Get:16 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libquadmath0 amd64 5.4.0-6ubuntu1~16.04.11 [131 kB]
Get:17 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libgcc-5-dev amd64 5.4.0-6ubuntu1~16.04.11 [2,229 kB]
Get:18 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 gcc-5 amd64 5.4.0-6ubuntu1~16.04.11 [8,417 kB]
Get:19 http://archive.ubuntu.com/ubuntu xenial/main amd64 gcc amd64 4:5.3.1-1ubuntu1 [5,244 B]
Get:20 http://archive.ubuntu.com/ubuntu xenial/main amd64 make amd64 4.1-6 [151 kB]
Get:21 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 dkms all 2.2.0.3-2ubuntu11.5 [66.3 kB]
Get:22 http://archive.ubuntu.com/ubuntu xenial/main amd64 libfakeroot amd64 1.20.2-1ubuntu1 [25.5 kB]
Get:23 http://archive.ubuntu.com/ubuntu xenial/main amd64 fakeroot amd64 1.20.2-1ubuntu1 [61.8 kB]
Get:24 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libc-dev-bin amd64 2.23-0ubuntu10 [68.7 kB]
Get:25 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-libc-dev amd64 4.4.0-142.168 [867 kB]
Get:26 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libc6-dev amd64 2.23-0ubuntu10 [2,079 kB]
Get:27 http://archive.ubuntu.com/ubuntu xenial/main amd64 manpages-dev all 4.04-2 [2,048 kB]
dpkg-preconfigure: unable to re-open stdin: No such file or directory
Fetched 27.6 MB in 6s (3,946 kB/s)
Selecting previously unselected package libmpc3:amd64.
(Reading database ... 54184 files and directories currently installed.)
Preparing to unpack .../libmpc3_1.0.3-1_amd64.deb ...
Unpacking libmpc3:amd64 (1.0.3-1) ...
Selecting previously unselected package binutils.
Preparing to unpack .../binutils_2.26.1-1ubuntu1~16.04.7_amd64.deb ...
Unpacking binutils (2.26.1-1ubuntu1~16.04.7) ...
Selecting previously unselected package libisl15:amd64.
Preparing to unpack .../libisl15_0.16.1-1_amd64.deb ...
Unpacking libisl15:amd64 (0.16.1-1) ...
Selecting previously unselected package cpp-5.
Preparing to unpack .../cpp-5_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking cpp-5 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package cpp.
Preparing to unpack .../cpp_4%3a5.3.1-1ubuntu1_amd64.deb ...
Unpacking cpp (4:5.3.1-1ubuntu1) ...
Selecting previously unselected package libcc1-0:amd64.
Preparing to unpack .../libcc1-0_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libcc1-0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libgomp1:amd64.
Preparing to unpack .../libgomp1_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libgomp1:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libitm1:amd64.
Preparing to unpack .../libitm1_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libitm1:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libatomic1:amd64.
Preparing to unpack .../libatomic1_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libatomic1:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libasan2:amd64.
Preparing to unpack .../libasan2_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libasan2:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package liblsan0:amd64.
Preparing to unpack .../liblsan0_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking liblsan0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libtsan0:amd64.
Preparing to unpack .../libtsan0_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libtsan0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libubsan0:amd64.
Preparing to unpack .../libubsan0_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libubsan0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libcilkrts5:amd64.
Preparing to unpack .../libcilkrts5_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libcilkrts5:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libmpx0:amd64.
Preparing to unpack .../libmpx0_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libmpx0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libquadmath0:amd64.
Preparing to unpack .../libquadmath0_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libquadmath0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package libgcc-5-dev:amd64.
Preparing to unpack .../libgcc-5-dev_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking libgcc-5-dev:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package gcc-5.
Preparing to unpack .../gcc-5_5.4.0-6ubuntu1~16.04.11_amd64.deb ...
Unpacking gcc-5 (5.4.0-6ubuntu1~16.04.11) ...
Selecting previously unselected package gcc.
Preparing to unpack .../gcc_4%3a5.3.1-1ubuntu1_amd64.deb ...
Unpacking gcc (4:5.3.1-1ubuntu1) ...
Selecting previously unselected package make.
Preparing to unpack .../archives/make_4.1-6_amd64.deb ...
Unpacking make (4.1-6) ...
Selecting previously unselected package dkms.
Preparing to unpack .../dkms_2.2.0.3-2ubuntu11.5_all.deb ...
Unpacking dkms (2.2.0.3-2ubuntu11.5) ...
Selecting previously unselected package libfakeroot:amd64.
Preparing to unpack .../libfakeroot_1.20.2-1ubuntu1_amd64.deb ...
Unpacking libfakeroot:amd64 (1.20.2-1ubuntu1) ...
Selecting previously unselected package fakeroot.
Preparing to unpack .../fakeroot_1.20.2-1ubuntu1_amd64.deb ...
Unpacking fakeroot (1.20.2-1ubuntu1) ...
Selecting previously unselected package libc-dev-bin.
Preparing to unpack .../libc-dev-bin_2.23-0ubuntu10_amd64.deb ...
Unpacking libc-dev-bin (2.23-0ubuntu10) ...
Selecting previously unselected package linux-libc-dev:amd64.
Preparing to unpack .../linux-libc-dev_4.4.0-142.168_amd64.deb ...
Unpacking linux-libc-dev:amd64 (4.4.0-142.168) ...
Selecting previously unselected package libc6-dev:amd64.
Preparing to unpack .../libc6-dev_2.23-0ubuntu10_amd64.deb ...
Unpacking libc6-dev:amd64 (2.23-0ubuntu10) ...
Selecting previously unselected package manpages-dev.
Preparing to unpack .../manpages-dev_4.04-2_all.deb ...
Unpacking manpages-dev (4.04-2) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Processing triggers for man-db (2.7.5-1) ...
Setting up libmpc3:amd64 (1.0.3-1) ...
Setting up binutils (2.26.1-1ubuntu1~16.04.7) ...
Setting up libisl15:amd64 (0.16.1-1) ...
Setting up cpp-5 (5.4.0-6ubuntu1~16.04.11) ...
Setting up cpp (4:5.3.1-1ubuntu1) ...
Setting up libcc1-0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libgomp1:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libitm1:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libatomic1:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libasan2:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up liblsan0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libtsan0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libubsan0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libcilkrts5:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libmpx0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libquadmath0:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up libgcc-5-dev:amd64 (5.4.0-6ubuntu1~16.04.11) ...
Setting up gcc-5 (5.4.0-6ubuntu1~16.04.11) ...
Setting up gcc (4:5.3.1-1ubuntu1) ...
Setting up make (4.1-6) ...
Setting up dkms (2.2.0.3-2ubuntu11.5) ...
Setting up libfakeroot:amd64 (1.20.2-1ubuntu1) ...
Setting up fakeroot (1.20.2-1ubuntu1) ...
update-alternatives: using /usr/bin/fakeroot-sysv to provide /usr/bin/fakeroot (fakeroot) in auto mode
Setting up libc-dev-bin (2.23-0ubuntu10) ...
Setting up linux-libc-dev:amd64 (4.4.0-142.168) ...
Setting up libc6-dev:amd64 (2.23-0ubuntu10) ...
Setting up manpages-dev (4.04-2) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Copy iso file /Applications/VirtualBox.app/Contents/MacOS/VBoxGuestAdditions.iso into the box /tmp/VBoxGuestAdditions.iso
Mounting Virtualbox Guest Additions ISO to: /mnt
mount: /dev/loop0 is write-protected, mounting read-only
Installing Virtualbox Guest Additions 6.0.4 - guest version is 5.1.38
Verifying archive integrity... All good.
Uncompressing VirtualBox 6.0.4 Guest Additions for Linux........
VirtualBox Guest Additions installer
Copying additional installer modules ...
Installing additional modules ...
VirtualBox Guest Additions: Building the VirtualBox Guest Additions kernel 
modules.  This may take a while.
VirtualBox Guest Additions: To build modules for other installed kernels, run
VirtualBox Guest Additions:   /sbin/rcvboxadd quicksetup <version>
VirtualBox Guest Additions: Building the modules for kernel 4.4.0-142-generic.
update-initramfs: Generating /boot/initrd.img-4.4.0-142-generic
VirtualBox Guest Additions: Starting.
Unmounting Virtualbox Guest Additions ISO from: /mnt
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => /Users/michael/vagrant-tutorial-locally

```


To SSH into a running Vagrant machine and access the shell,

    $ vagrant ssh

You should see the following output:

```
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-142-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.

New release '18.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


vagrant@ubuntu-xenial:~$ 

```

To shuts down the running Vagrant machine,

    $ vagrant halt

To suspends the Vagrant machine,

    $ vagrant suspend 

NOTE: Saves the exact point-in-time state of the machine

To teardown the Vagrant machine,

    $ vagrant destroy

```
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```


Setup Vagrant on AWS
---

Let us first create a folder to contain the new Vagrant environment

    $ mkdir vagrant-tutorial-aws
    $ cd vagrant-tutorial-aws

To add a spin to this seciton, I will add a AWS provider box from GitHub created by Mitchell Hashimoto.

    $ vagrant box add aws_provider_box https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box


The output of adding the box is as follows:
```
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'aws_provider_box' (v0) for provider: 
    box: Downloading: https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box
    box: Download redirected to host: raw.githubusercontent.com
==> box: Successfully added box 'aws_provider_box' (v0) for 'aws'!
```

NOTE: I have named the box _aws_provider_box_, but any name may be used.


Run the following command to create a vagrant file,

    $ vagrant init 

Edit the Vagrantfile created and replace the contents with the following:

```
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Require the AWS provider plugin
 require ‘vagrant-aws’

# Creating and configuring the AWS instance
Vagrant.configure("2") do |config|
  # Use dummy AWS box
  config.vm.box = "dummy"

  config.vm.provider :aws do |aws, override|
    # Specify AMI ID, key pair, Instance, security group and user data
    aws.ami = "ami-012fd5eb46f56731f"
    aws.keypair_name = "vagrant"
    aws.instance_type = "t2.micro"
    aws.security_groups = ["default"]
    aws.user_data = "#!/bin/bash\necho 'got user data' > /tmp/user_data.log\necho"

    # Specify username and private key path
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "PATH TO YOUR PRIVATE KEY"
  end
end
```

NOTE: Please visit [vagrant-aws](https://github.com/mitchellh/vagrant-aws) for all configuration options.

Ensure your AWS credentials are set and to start the Vagrant enviroment,

    $ vagrant up --provider=aws

The output is as follows: 

```
Bringing machine 'default' up with 'aws' provider...
==> default: Warning! The AWS provider doesn't support any of the Vagrant
==> default: high-level network configurations (`config.vm.network`). They
==> default: will be silently ignored.
==> default: Launching an instance with the following settings...
==> default:  -- Type: t2.micro
==> default:  -- AMI: ami-012fd5eb46f56731f
==> default:  -- Region: us-east-1
==> default:  -- Keypair: vagrant
==> default:  -- Security Groups: ["default"]
==> default:  -- Block Device Mapping: []
==> default:  -- Terminate On Shutdown: false
==> default:  -- Monitoring: false
==> default:  -- EBS optimized: false
==> default:  -- Source Destination check: 
==> default:  -- Assigning a public IP address in a VPC: false
==> default:  -- VPC tenancy specification: default
==> default: Waiting for instance to become "ready"...
==> default: Waiting for SSH to become available...
==> default: Machine is booted and ready for use!
```

The above will start an Ubuntu 18.04 instance and assuming your SSH information was filled in properly within your Vagrantfile and the EC2 instance is InService, SSH and provisioning will work as well.

To clean up everything, 

    $ vagrant destroy

```
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Terminating the instance...
```


# Conclusion

Vagrant can be easily setup to launch locally or on AWS. 
