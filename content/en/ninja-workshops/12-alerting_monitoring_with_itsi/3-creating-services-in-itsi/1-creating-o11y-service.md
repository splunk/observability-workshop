---
title: Creating an O11y Based Service
linkTitle: 3.1 Creating an O11y Based Service
weight: 2
---

# Starting with an Observability Cloud Based Service

1. **Access Services:** In ITSI click "Configuration", click on "Services".

2. **Create New Service: PaymentService2:** Click "Create New Service".

3. **Service Details (PaymentService2):**
    * **Title:** "PaymentService2"
    * **Description (Optional):**  e.g., "Payment Service for Hipster Shop - version 2"

4. **Select Template:** Choose "Link service to a service template" and search for "Splunk APM Business Workflow KPIs" from the template dropdown. Click **Create** to save the new service.

6. **Entity Assignment:**
    * The page will load and display the new Service and you will be on the Entities page. This demo defaults to selecting the *paymentservice:grpc.hipstershop.PaymentService/Charge* entity. In a real world situation you would need to match the workflow to the entity name manually.
    * **Direct Entity Selection (If Available):** Search for the entity using `sf_workflow="paymentservice:grpc.hipstershop.PaymentService/Charge"` and select it.

7. **Save Service (PaymentService2):** Click "Save" to create "PaymentService2".

8. **Settings:** Click the "Settings" tab, enable *Backfill* and keep that standard 7 days. Enable the Service, and click "Save"

## Setting PaymentService2's Service Health as a Dependency for Online-Boutique-US

1. **Locate Online-Boutique-US:** Find the "Online-Boutique-US" service in the service list.

2. **Edit Online-Boutique-US:** Click "Edit".

3. **Service Dependencies:** Look for the "Service Dependencies" section. 

4. **Add Dependency:**  There should be an option to add a dependent service.  Search for "PaymentService2".

5. **Select KPI:** Check the box next to ServiceHealthScore for PaymentService2.

6. **Save Changes:** Save the changes to the "Online-Boutique-US" service.

## Verification

* Click on "Service Analyzer" and select the "Default Analyzer"
* Filter the service to just "Buttercup Business Health"
* Verify that *PaymentService2* is now present below *Online-Boutique-US* and should be in a grey status.

![show-entry](../images/service_tree_o11y.png?classes=inline)