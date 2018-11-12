variable access_key {
  type = "string"
  default = "<access_key>"
  description = "My secret access key"
}

variable secret_key {
  type = "string"
  default = "<secret_key>"
  description = "My secret secret key"
}

provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "us-east-1"
}
