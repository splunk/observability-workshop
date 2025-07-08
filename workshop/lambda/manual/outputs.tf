# Output value definitions


output "lambda_bucket_name" {
  description = "S3 Bucket"
  value = aws_s3_bucket.lambda_bucket.id
}

output "base_url" {
  description = "Endpoint"
  value = "${aws_apigatewayv2_stage.lambda.invoke_url}/producer"
}

output "producer_function_name" {
  description = "Lambda Producer"
  value = aws_lambda_function.lambda_producer.function_name
}

output "producer_log_group_name" {
  description = "Log Group Name for the Lambda Producer"
  value = aws_cloudwatch_log_group.lambda_producer.name
}

output "producer_log_group_arn" {
  description = "Log Group ARN for the Lambda Producer"
  value = aws_cloudwatch_log_group.lambda_producer.arn
}

output "consumer_function_name" {
  description = "Lambda Consumer"
  value = aws_lambda_function.lambda_consumer.function_name
}

output "consumer_log_group_name" {
  description = "Log Group Name for the Lambda Consumer"
  value = aws_cloudwatch_log_group.lambda_consumer.name
}

output "consumer_log_group_arn" {
  description = "Log Group ARN for the Lambda Consumer"
  value = aws_cloudwatch_log_group.lambda_consumer.arn
}

output "environment" {
  description = "Deployment Environment"
  value = "${var.prefix}-lambda-shop"
}
