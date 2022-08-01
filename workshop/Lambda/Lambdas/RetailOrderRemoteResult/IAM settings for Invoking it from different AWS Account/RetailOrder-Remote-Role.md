This Lambda can be called  from the original accoutn, then it will follow the same procedure as any other lambda,  using a (Srandard) local Role when called.

However for Extra credit this can be called from an different AWS account  here are the IAM settings required to do so.

Create a role in account 2 to allow execution from other account :

### Lambda-Remote-Role

## Add to role the AWSLambdaExecute Policy

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::*"
        }
    ]
}

## Also add to the role the AWSLambdaRole Policy

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}

### Setup Trust relationship with Lambda Role in above Role

## (Replace Account-id and Role-name with the relevant info)

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RemotePH1",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "events.amazonaws.com",
                    "lambda.amazonaws.com"
                ],
                "AWS": "arn:aws:iam::[Account-id]:role/[Role-name]"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

### Optional - Create a policy for remote invocation

Remote-Lambda-Policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole",
                "lambda:InvokeFunctionUrl",
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": [
                "arn:aws:iam::527477237977:role/*",
                "arn:aws:lambda:*:527477237977:function:*"
            ]
        }
    ]
}