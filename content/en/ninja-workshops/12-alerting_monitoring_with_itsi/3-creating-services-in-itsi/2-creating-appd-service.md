---
title: Creating an AppD Based Service
linkTitle: 3.2 Creating an AppD Based Service
weight: 3
---

# Starting with an AppDynamics Based Service

1. **Access Services:** In ITSI click "Configuration", click on "Services".

2. **Create Service: AD-Ecommerce2:** Click "Create Service -> Create Service".

3. **Service Details (AD-Ecommerce2):**
    * **Title:** "AD-Ecommerce2"
    * **Description (Optional):**  e.g., "Ecommerce Service - version 2"

4. **Select Template:** Choose "Link service to a service template" and search for "AppDynamics App Performance Monitoring" from the template dropdown. Click **Create** to save the new service.

5. **Entity Assignment:**
    * The page will load and display the new Service and you will be on the Entities page. This demo defaults to selecting the *AD-Ecommerce:18112:demo1.saas.appdynamics.com* entity. In a real world situation you would need to match the entity_name to the entity name manually.
    * **Direct Entity Selection (If Available):** Search for the entity using `entity_name="AD-Ecommerce:18112:demo1.saas.appdynamics.com"` and select it.

7. **Settings:** Click the "Settings" tab, enable *Backfill* and keep that standard 7 days. Enable the Service, and click "Save"

## Setting AD-Ecommerce2's Service Health as a Dependency for AD.Ecommerce

1. **Navigate back to Services page:** Click "Configuration -> Services"

2. **Locate AD.Ecommerce:** Find the "AD.Ecommerce" service in the service list.

3. **Edit AD.Ecommerce:** Click "Edit".

4. **Service Dependencies:** Look for the "Service Dependencies" section. 

5. **Add Dependency:**  There should be an option to add a dependent service.  Search for "AD-Ecommerce2".

6. **Select KPI:** Check the box next to ServiceHealthScore for AD-Ecommerce2.

7. **Save Changes:** Save the changes to the "AD.Ecommerce" service.

## Verification

* Click on "Service Analyzer" and select the "Default Analyzer"
* Filter the service to just "Buttercup Business Health"
* Verify that *AD-Ecommerce2* is now present below *AD.Ecommerce* and should be in a grey status.

![show-entry](../images/service_tree_appd.png?classes=inline)