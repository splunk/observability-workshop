provider "aws" {
  profile = "default"
  region  = var.aws_region
}

provider "signalfx" {
  auth_token = var.signalfx_api_access_token
  api_url    = "https://api.${var.signalfx_realm}.signalfx.com"
}

resource "signalfx_aws_external_integration" "aws_myteam_extern" {
  name = var.signalfx_aws_integration_name
}

data "aws_iam_policy_document" "signalfx_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = [signalfx_aws_external_integration.aws_myteam_extern.signalfx_aws_account]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [signalfx_aws_external_integration.aws_myteam_extern.external_id]
    }
  }
}

resource "aws_iam_role" "aws_sfx_role" {
  name               = "signalfx-reads-from-cloudwatch2"
  description        = "Observability Cloud integration to read out data and send it to Observability Cloud's AWS aws account"
  assume_role_policy = data.aws_iam_policy_document.signalfx_assume_policy.json
}

resource "aws_iam_policy" "aws_read_permissions" {
  name        = "SignalFxReadPermissionsPolicy"
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
  role       = aws_iam_role.aws_sfx_role.name
  policy_arn = aws_iam_policy.aws_read_permissions.arn
}

resource "time_sleep" "iam_policy_available" {
  depends_on = [aws_iam_role_policy_attachment.sfx-read-attach]
  create_duration = "13s"
}

resource "signalfx_aws_integration" "aws_sfx" {
  enabled    = true
  depends_on = [time_sleep.iam_policy_available]

  integration_id     = signalfx_aws_external_integration.aws_myteam_extern.id
  external_id        = signalfx_aws_external_integration.aws_myteam_extern.external_id
  role_arn           = aws_iam_role.aws_sfx_role.arn
  regions            = [var.aws_region]
  poll_rate          = 60
  import_cloud_watch = true
  enable_aws_usage   = false
}
