# Post Workshop Clean Up

=== "Multipass"

    Once you have finished with this Workshop `exit` from the Multipass instance to get back to your system command prompt.
    
    Enter the following to delete and purge the Multipass instance:

    ```bash
    multipass delete --purge $INSTANCE
    ```

=== "AWS/EC2"

    Once you have finished with this Workshop `exit` from the AWS/EC2 instance to get back to your system command prompt.
    
    We will use Terraform to destroy the instance with the parameters you used in [Smart Agent](../../smartagent/prep/) module:

    ```bash
    cd ~/workshop/ec2
    terraform destroy -var="aws_instance_count=1" -var="instance_type=1"
    ```

    Enter `Instance Count`, `Provide the desired region` and `Select instance type required`.
    
    When prompted type `yes` to confirm you want to destroy, this will take a while to complete.

    ```text
    aws_instance.app-dev-instance[0]: Destroying... [id=i-088560a5f6e2bbdbb]
    aws_instance.app-dev-instance[0]: Still destroying... [id=i-088560a5f6e2bbdbb, 10s elapsed]
    aws_instance.app-dev-instance[0]: Still destroying... [id=i-088560a5f6e2bbdbb, 20s elapsed]
    aws_instance.app-dev-instance[0]: Still destroying... [id=i-088560a5f6e2bbdbb, 30s elapsed]
    aws_instance.app-dev-instance[0]: Still destroying... [id=i-088560a5f6e2bbdbb, 40s elapsed]
    aws_instance.app-dev-instance[0]: Still destroying... [id=i-088560a5f6e2bbdbb, 50s elapsed]
    aws_instance.app-dev-instance[0]: Destruction complete after 56s
    aws_security_group.instance: Destroying... [id=sg-0d6841fbeef022a9f]
    aws_security_group.instance: Destruction complete after 2s
    ```
