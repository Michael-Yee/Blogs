resource "aws_instance" "web" {
  ami           = "ami-09c624b6cc0ab6e61"
  instance_type = "t2.micro"
}
