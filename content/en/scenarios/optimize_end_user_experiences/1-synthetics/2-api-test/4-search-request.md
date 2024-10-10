---
title: Search Request
linkTitle: 2.4 Search Request
weight: 4
hidden: false
---

Click on {{< button >}}+ Add Request{{< /button >}} to add the next step. Name the step **Search for Tracks named "Up around the bend"**.

Expand the **Request** section and change the request method to **GET** and enter the following URL:

``` text
https://api.spotify.com/v1/search?q=Up%20around%20the%20bend&type=track&offset=0&limit=5
```

Next, add two request headers with the following key/value pairings:

- **CONTENT-TYPE: application/json**
- **AUTHORIZATION: Bearer {{custom.access_token}}**
  - This uses the custom variable we created in the previous step!

![Add search request](../../images/add-search-request.png)

Expand the **Validation** section and add the following extraction:

- **Extract** from **Response body** **JSON** **$.tracks.items[0].id** as **track.id**

![Add search payload](../../images/add-search-payload.png)

To validate the test before saving, change the location as needed and click {{< button >}}Try now{{< /button >}}. See the docs for more information on the [try now feature](https://docs.splunk.com/observability/en/synthetics/test-config/try-now.html).

![try now](../../images/try-now.png)

When the validation is successful, click on {{< button style="blue" >}}< Return to test{{< /button >}} to return to the test configuration page. And then click {{< button style="blue" >}}Save{{< /button >}} to save the API test.

{{% notice title="Extra credit" style="green" icon="running" %}}
Have more time to work on this test? Take a look at the Response Body in one of your run results. What additional steps would make this test more thorough? Edit the test, and use the {{< button >}}Try now{{< /button >}} feature to validate any changes you make before you save the test.
{{% /notice %}}