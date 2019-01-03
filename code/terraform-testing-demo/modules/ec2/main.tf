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
