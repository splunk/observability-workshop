provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      o11y-workshop = "lambda-tracing"
    }
  }
}


# Get IAM Role
data "aws_caller_identity" "current" {}
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

# Create S3 Bucket, Ownership, ACL
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "${var.prefix}-lambda-code"
}

resource "aws_s3_bucket_ownership_controls" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "lambda_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.lambda_bucket]

  bucket = aws_s3_bucket.lambda_bucket.id
  acl    = "private"
}


# Package Producer and Consumer Apps, Upload to S3 Bucket
data "archive_file" "producer_app" {
  type = "zip"

  source_file  = "${path.module}/handler/producer.mjs"
  output_path = "${path.module}/lambda_producer.zip"
}

resource "aws_s3_object" "producer_app" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda_producer.zip"
  source = data.archive_file.producer_app.output_path

  etag = filemd5(data.archive_file.producer_app.output_path)
}

data "archive_file" "consumer_app" {
  type = "zip"

  source_file  = "${path.module}/handler/consumer.mjs"
  output_path = "${path.module}/lambda_consumer.zip"
}

resource "aws_s3_object" "consumer_app" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda_consumer.zip"
  source = data.archive_file.consumer_app.output_path

  etag = filemd5(data.archive_file.consumer_app.output_path)
}


# Create Lambda Functions
resource "aws_lambda_function" "lambda_producer" {
  function_name = "${var.prefix}-producer"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.producer_app.key

  runtime = "nodejs20.x"
  handler = "producer.producer"

  source_code_hash = data.archive_file.producer_app.output_base64sha256

  role = aws_iam_role.lambda_kinesis.arn

  environment {
    variables = {
      SPLUNK_ACCESS_TOKEN = var.o11y_access_token
      SPLUNK_REALM = var.o11y_realm
      OTEL_SERVICE_NAME = "${var.prefix}-producer-lambda"
      OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
      AWS_LAMBDA_EXEC_WRAPPER = "/opt/nodejs-otel-handler"
      KINESIS_STREAM = aws_kinesis_stream.lambda_stream.name
    }
  }

  layers = var.otel_lambda_layer

  timeout = 60
}

resource "aws_lambda_function" "lambda_consumer" {
  function_name = "${var.prefix}-consumer"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.consumer_app.key

  runtime = "nodejs20.x"
  handler = "consumer.consumer"

  source_code_hash = data.archive_file.consumer_app.output_base64sha256

  role = aws_iam_role.lambda_kinesis.arn

  environment {
    variables = {
      SPLUNK_ACCESS_TOKEN = var.o11y_access_token
      SPLUNK_REALM = var.o11y_realm
      OTEL_SERVICE_NAME = "${var.prefix}-consumer-lambda"
      OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
      AWS_LAMBDA_EXEC_WRAPPER = "/opt/nodejs-otel-handler"
    }
  }

  layers = var.otel_lambda_layer

  timeout = 60
}

# Add API Gateway API, Stage, Integration, Route and Permission Resources
resource "aws_apigatewayv2_api" "lambda" {
  name = "${var.prefix}-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name = "${var.prefix}-gw-stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.lambda_producer.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "POST /producer"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_producer.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

# CloudWatch Log Groups for Lambda and API Gateway
resource "aws_cloudwatch_log_group" "lambda_producer" {
  name = "/aws/lambda/${aws_lambda_function.lambda_producer.function_name}"

  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "lambda_consumer" {
  name = "/aws/lambda/${aws_lambda_function.lambda_consumer.function_name}"

  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

# Kinesis Data Stream
resource "aws_kinesis_stream" "lambda_stream" {
    name = "${var.prefix}-lambda_stream"
    shard_count = 1
    retention_period = 24
    shard_level_metrics = [
        "IncomingBytes",
        "OutgoingBytes"
    ]
}

# Source Mapping Lambda Consumer to Kinesis Stream
resource "aws_lambda_event_source_mapping" "kinesis_lambda_event_mapping" {
    batch_size = 100
    event_source_arn = aws_kinesis_stream.lambda_stream.arn
    enabled = true
    function_name = aws_lambda_function.lambda_consumer.arn
    starting_position = "LATEST"
}