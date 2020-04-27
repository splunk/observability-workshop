# 1. Removing the Multipass instance

Once you have finished with this workshop `exit` from the Multipass instance you are in and get back to your system command prompt and enter the following to delete the Multipass instance, replace `[YOUR_INITIALS]` with the ones you used in [Module 3](../../module3/prep/):

```bash
multipass delete --purge [YOUR_INITIALS]-k3s
```

!!! note
    If you are using a workshop instance on EC2 please ignore this and just terminate your instance.
