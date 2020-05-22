# Post Workshop Clean Up

Once you have finished with this workshop `exit` from the Multipass instance(s) you are in and get back to your system command prompt.

You can use `multipass list` to get the names of any current running instances:

=== "Input"

    ```bash
    multipass list
    ```

=== "Example Output"

    ```
    Name                State             IPv4             Image
    IXMY-vo1            Running           192.168.64.13    Ubuntu 18.04 LTS
    HWJL-vo2            Running           192.168.64.14    Ubuntu 18.04 LTS
    ```

Enter the following to delete the Multipass instance(s), replace `{==INSTANCE==}` with the ones from above:

=== "Input"

    ```bash
    multipass delete --purge {==INSTANCE==}-vo1
    multipass delete --purge {==INSTANCE==}-vo2
    ```
