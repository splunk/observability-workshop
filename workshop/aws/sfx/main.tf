provider "aws" {
  profile = var.aws_profile
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
      "Effect": "Allow",
      "Action": [
        "airflow:GetEnvironment",
        "airflow:ListEnvironments",
        "apigateway:GET",
        "autoscaling:DescribeAutoScalingGroups",
        "cloudformation:ListResources",
        "cloudformation:GetResource",
        "cloudfront:GetDistributionConfig",
        "cloudfront:ListDistributions",
        "cloudfront:ListTagsForResource",
        "cloudwatch:GetMetricData",
        "cloudwatch:ListMetrics",
        "directconnect:DescribeConnections",
        "dynamodb:DescribeTable",
        "dynamodb:ListTables",
        "dynamodb:ListTagsOfResource",
        "ec2:DescribeInstances",
        "ec2:DescribeInstanceStatus",
        "ec2:DescribeNatGateways",
        "ec2:DescribeRegions",
        "ec2:DescribeReservedInstances",
        "ec2:DescribeReservedInstancesModifications",
        "ec2:DescribeTags",
        "ec2:DescribeVolumes",
        "ecs:DescribeClusters",
        "ecs:DescribeServices",
        "ecs:DescribeTasks",
        "ecs:ListClusters",
        "ecs:ListServices",
        "ecs:ListTagsForResource",
        "ecs:ListTaskDefinitions",
        "ecs:ListTasks",
        "eks:DescribeCluster",
        "eks:ListClusters",
        "elasticache:DescribeCacheClusters",
        "elasticloadbalancing:DescribeLoadBalancerAttributes",
        "elasticloadbalancing:DescribeLoadBalancers",
        "elasticloadbalancing:DescribeTags",
        "elasticloadbalancing:DescribeTargetGroups",
        "elasticmapreduce:DescribeCluster",
        "elasticmapreduce:ListClusters",
        "es:DescribeElasticsearchDomain",
        "es:ListDomainNames",
        "kafka:DescribeCluster",
        "kafka:DescribeClusterV2",
        "kafka:ListClusters",
        "kafka:ListClustersV2",
        "kinesis:DescribeStream",
        "kinesis:ListShards",
        "kinesis:ListStreams",
        "kinesis:ListTagsForStream",
        "kinesisanalytics:DescribeApplication",
        "kinesisanalytics:ListApplications",
        "kinesisanalytics:ListTagsForResource",
        "lambda:GetAlias",
        "lambda:ListFunctions",
        "lambda:ListTags",
        "logs:DeleteSubscriptionFilter",
        "logs:DescribeLogGroups",
        "logs:DescribeSubscriptionFilters",
        "logs:PutSubscriptionFilter",
        "organizations:DescribeOrganization",
        "rds:DescribeDBInstances",
        "rds:DescribeDBClusters",
        "rds:ListTagsForResource",
        "redshift:DescribeClusters",
        "redshift:DescribeLoggingStatus",
        "s3:GetBucketLocation",
        "s3:GetBucketLogging",
        "s3:GetBucketNotification",
        "s3:GetBucketTagging",
        "s3:ListAllMyBuckets",
        "s3:ListBucket",
        "s3:PutBucketNotification",
        "sqs:GetQueueAttributes",
        "sqs:ListQueues",
        "sqs:ListQueueTags",
        "states:ListActivities",
        "states:ListStateMachines",
        "tag:GetResources",
        "workspaces:DescribeWorkspaces"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cassandra:Select"
      ],
      "Resource": [
        "arn:aws:cassandra:*:*:/keyspace/system/table/local",
        "arn:aws:cassandra:*:*:/keyspace/system/table/peers",
        "arn:aws:cassandra:*:*:/keyspace/system_schema/*",
        "arn:aws:cassandra:*:*:/keyspace/system_schema_mcs/table/tags",
        "arn:aws:cassandra:*:*:/keyspace/system_schema_mcs/table/tables",
        "arn:aws:cassandra:*:*:/keyspace/system_schema_mcs/table/columns"
      ]
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
