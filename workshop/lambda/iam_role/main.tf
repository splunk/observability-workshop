provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      o11y-workshop = "lambda-tracing"
    }
  }
}


# Create IAM Role
resource "aws_iam_role" "lambda_kinesis" {
  name = "lambda_kinesis"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
resource "aws_iam_role_policy_attachment" "lambda_kinesis_execution" {
  role       = aws_iam_role.lambda_kinesis.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisFullAccess"
}

resource "aws_iam_policy" "lambda_cloudwatch_logs" {
  name = "LambdaCloudWatchLogsCustomPolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_cloudwatch_logs_attachment" {
  role       = aws_iam_role.lambda_kinesis.name
  policy_arn = aws_iam_policy.lambda_cloudwatch_logs.arn
}

# Create IAM User and Credentials
resource "aws_iam_user" "workshop" {
  name = var.workshop_user_name
}

resource "aws_iam_access_key" "workshop" {
  user = aws_iam_user.workshop.name
}

data "aws_iam_policy_document" "workshop_user" {
  statement {
    sid = "ManageWorkshopResources"

    actions = [
      "apigateway:*",
      "kinesis:*",
      "lambda:*",
      "logs:*",
      "s3:*",
      "sts:GetCallerIdentity",
    ]

    resources = ["*"]
  }

  statement {
    sid = "UseLambdaExecutionRole"

    actions = [
      "iam:GetRole",
      "iam:PassRole",
    ]

    resources = [aws_iam_role.lambda_kinesis.arn]
  }
}

resource "aws_iam_user_policy" "workshop" {
  name   = "${var.workshop_user_name}-workshop-permissions"
  user   = aws_iam_user.workshop.name
  policy = data.aws_iam_policy_document.workshop_user.json
}
