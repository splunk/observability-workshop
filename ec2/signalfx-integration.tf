provider "signalfx" {
  auth_token = var.signalFxApiAccessToken
  api_url    = "https://api.${var.signalFxRealm}.signalfx.com"
}

resource "signalfx_aws_external_integration" "aws_myteam_extern" {
  name  = var.signalFxAWSIntegrationName
  count = var.signalFxAWSIntegrationEnabled
}

data "aws_iam_policy_document" "signalfx_assume_policy" {
  count = var.signalFxAWSIntegrationEnabled
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = [signalfx_aws_external_integration.aws_myteam_extern[0].signalfx_aws_account]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [signalfx_aws_external_integration.aws_myteam_extern[0].external_id]
    }
  }
}

resource "aws_iam_role" "aws_sfx_role" {
  name               = "signalfx-reads-from-cloudwatch2"
  count              = var.signalFxAWSIntegrationEnabled
  description        = "SignalFx integration to read out data and send it to SignalFx's AWS aws account"
  assume_role_policy = data.aws_iam_policy_document.signalfx_assume_policy[0].json
}

resource "aws_iam_policy" "aws_read_permissions" {
  name        = "SignalFxReadPermissionsPolicy"
  count       = var.signalFxAWSIntegrationEnabled
  description = "SignalFx IAM Policy"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "dynamodb:ListTables",
                "dynamodb:DescribeTable",
                "dynamodb:ListTagsOfResource",
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeVolumes",
                "ec2:DescribeReservedInstances",
                "ec2:DescribeReservedInstancesModifications",
                "ec2:DescribeTags",
                "organizations:DescribeOrganization",
                "cloudwatch:ListMetrics",
                "cloudwatch:GetMetricData",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:DescribeAlarms",
                "sqs:ListQueues",
                "sqs:GetQueueAttributes",
                "sqs:ListQueueTags",
                "elasticmapreduce:ListClusters",
                "elasticmapreduce:DescribeCluster",
                "kinesis:ListShards",
                "kinesis:ListStreams",
                "kinesis:DescribeStream",
                "kinesis:ListTagsForStream",
                "rds:DescribeDBInstances",
                "rds:ListTagsForResource",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeTags",
                "elasticache:describeCacheClusters",
                "redshift:DescribeClusters",
                "lambda:GetAlias",
                "lambda:ListFunctions",
                "lambda:ListTags",
                "autoscaling:DescribeAutoScalingGroups",
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:GetBucketTagging",
                "ecs:ListServices",
                "ecs:ListTasks",
                "ecs:DescribeTasks",
                "ecs:DescribeServices",
                "ecs:ListClusters",
                "ecs:DescribeClusters",
                "ecs:ListTaskDefinitions",
                "ecs:ListTagsForResource",
                "apigateway:GET",
                "cloudfront:ListDistributions",
                "cloudfront:ListTagsForResource",
                "tag:GetResources",
                "es:ListDomainNames",
                "es:DescribeElasticsearchDomain"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "sfx-read-attach" {
  count       = var.signalFxAWSIntegrationEnabled
  role        = aws_iam_role.aws_sfx_role[0].name
  policy_arn  = aws_iam_policy.aws_read_permissions[0].arn
}

resource "signalfx_aws_integration" "aws_sfx" {
  count       = var.signalFxAWSIntegrationEnabled
  enabled     = true

  integration_id     = signalfx_aws_external_integration.aws_myteam_extern[0].id
  external_id        = signalfx_aws_external_integration.aws_myteam_extern[0].external_id
  role_arn           = aws_iam_role.aws_sfx_role[0].arn
  regions            = [var.aws_region]
  poll_rate          = 60
  import_cloud_watch = true
  enable_aws_usage   = false
}
