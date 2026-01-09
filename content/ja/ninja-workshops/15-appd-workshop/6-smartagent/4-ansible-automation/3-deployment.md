---
title: Deployment
weight: 3
time: 5 minutes
---

## Step 4: Execute the Playbook

To deploy the Smart Agent, run the following command from your project directory:

```bash
ansible-playbook -i inventory-cloud.yaml smartagent.yaml
```

Replace `inventory-cloud.yaml` with the appropriate inventory file for your setup if you named it differently.

### Verification

After the playbook completes successfully, you can verify the deployment by logging into one of the target hosts and checking the service status:

```bash
systemctl status smartagent
```

You should see the service is active (running).
