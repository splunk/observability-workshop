# Post Workshop Clean Up

Once you have finished with this workshop `exit` from the Multipass instance(s) you are in and get back to your system command prompt.

You can use `multipass list` to get the names of any current running instances:

=== "Shell Command"

    ```bash
    multipass list
    ```

=== "Example Output"

    ```
    Name                State             IPv4             Image
    vmpe-vo1            Running           192.168.64.13    Ubuntu 18.04 LTS
    vmpe-vo2            Running           192.168.64.14    Ubuntu 18.04 LTS
    ```

Ensure the `INSTANCE` environment variable is still set:

=== "Shell Command"

    ```bash
    echo $INSTANCE
    ```

If the environment varilable is not set, then you will have to replace `${INSTANCE}` below with the prefix of the instance name from the `multipass list` above.

Run the following commands to delete the Multipass instance(s):

=== "Shell Command"

    ```bash
    multipass delete --purge ${INSTANCE}-vo1
    multipass delete --purge ${INSTANCE}-vo2
    ```
