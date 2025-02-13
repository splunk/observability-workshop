---
title: Creating Basic Alerts
linkTitle: 3. Creating Services in ITSI
weight: 1
---

# Creating Services in ITSI with Dependencies Based on Entity Type

This workshop outlines how to create a service in Splunk IT Service Intelligence (ITSI) using an existing entity and establishing dependencies based on the entity's type. We'll differentiate between entities representing business workflows from Splunk Observability Cloud and those representing AppDynamics Business Transactions.

**Scenario:**

We have two existing services: "Online-Boutique-US" (representing an application running in Kubernetes and being monitored by Splunk Observability Cloud) and "AD.ECommerce" (representing an application monitored by AppDynamics). We want to create a new service and add it as a dependent of one of those services. It is not necessary to create a service for both during your first run through this workshop so pick one that you are more interested in to start with.

![show-entry](../images/service_tree_start.png?classes=inline)

## Starting with an Observability Cloud Based Service

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

## Setting PaymentService2's Service Health as a Dependency for Online-Boutique-US

1. **Locate Online-Boutique-US:** Find the "Online-Boutique-US" service in the service list.

2. **Edit Online-Boutique-US:** Click "Edit".

3. **Service Dependencies:** Look for the "Service Dependencies" section. 

4. **Add Dependency:**  There should be an option to add a dependent service.  Search for "PaymentService2".

5. **Select KPI:** Check the box next to ServiceHealthScore for PaymentService2.

6. **Save Changes:** Save the changes to the "Online-Boutique-US" service.

## Verification

* Verify "PaymentService2" is created and linked to the correct entity.
* Verify "Online-Boutique-US" now has "PaymentService2" (specifically its Service Health Score) as a dependency.  Changes in the health of "PaymentService2" should now impact the health of "Online-Boutique-US."
