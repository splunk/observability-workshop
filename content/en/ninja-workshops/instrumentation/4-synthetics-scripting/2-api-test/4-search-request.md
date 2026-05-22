---
title: Search Request
linkTitle: 1.4 Search Request
weight: 4
hidden: false
---

## Add Search Request

Click on {{< button >}}+ Add Request{{< /button >}} to add the next step. Name the step **Search for Tracks named "Up around the bend"**.

Expand the **Request** section and change the request method to **GET** and enter the following URL:

``` text
https://api.spotify.com/v1/search?q=Up%20around%20the%20bend&type=track&offset=0&limit=5
```

Next, add two request headers with the following key/value pairings:

- **CONTENT-TYPE: application/json**
- **AUTHORIZATION: Bearer {{custom.access_token}}**

![Add search request](../../img/add-search-request.png)

Expand the **Validation** section and add the following extraction:

- **Extract** from **Response body** **JSON** **$.tracks.items[0].id** **as** **track.id**.

![Add search payload](../../img/add-search-payload.png)

Click on {{< button style="blue" >}}< Return to test{{< /button >}} to return to the test configuration page. And then click {{< button style="blue" >}}Save{{< /button >}} to save the API test.
