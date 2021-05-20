# Enable APM in the RetailOrderLine Function

## 1. Edit UID_RetailOderLine Lambda in your AWS Environment

To add APM to our lambda function, you need to got to the browser tab with your lambda functions selected in the first exercise, or follow the original [Validate Lambda Functions](../initial_run_env/#1-validate-availability-of-lambda-functions) instructions. Once filtered with your **UID** you should have something like this:

INSERT SCREENSHOT

Now select the Lambda Function **UID**_RetailOrderLine to open the browser based editor environment for Lambda functions.

INSERT SCREENSHOT

Enable the Full Screen Editor and then close the 'Execution Result' tab to give you a clean working area

INSERT SCREENSHOT

To enable APM, we need to import the Splunk SignalFx Lambda wrapper. We already included this for you, but you can find the details on how to set this up yourself [here](https://github.com/signalfx/lambda-python){: target=_blank}

Secondly we also import the opentracing library, we will use this later to customize the span information we send to Splunk's APM.

Add the follow lines at the top of the file and add an empty line.

=== "RetailOrderLine Updates"

    ```text
    import signalfx_lambda
    import opentracing
    from opentracing.ext import tags
    from opentracing.propagation import Format

    ```

Add the following line above the line stating ***def lambda_handler(event,context):*** This will enable the wrapper.

=== "RetailOrderLine Updates"

    ```text
    @signalfx_lambda.is_traced(with_span=False)
    ```

 Verify that the file now looks like this:

 INSERT SCREENSHOT
