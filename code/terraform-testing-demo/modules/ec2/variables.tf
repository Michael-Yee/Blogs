# ---------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# Define the AWS credentials as environment variables
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
