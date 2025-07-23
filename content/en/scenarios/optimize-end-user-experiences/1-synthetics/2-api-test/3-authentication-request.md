---
title: Authentication Request
linkTitle: 2.3 Authentication Request
weight: 3
---

Click on {{< button >}}+ Add requests{{< /button >}} and enter the request step name e.g. **Authenticate with Spotify API**.

![placeholder](../../_img/add-request.png)

Expand the Request section, from the drop-down change the request method to **POST** and enter the following URL:

``` text
https://accounts.spotify.com/api/token
```

In the **Payload body** section enter the following:

``` text
grant_type=client_credentials
```

Next, add two {{< button >}}+ Request headers{{< /button >}} with the following key/value pairings:

- **CONTENT-TYPE: application/x-www-form-urlencoded**
- **AUTHORIZATION: Basic {{env.encoded_auth}}**

Expand the **Validation** section and add the following extraction:

- **Extract** from **Response body** **JSON** **$.access_token** as **access_token**

This will parse the JSON payload that is received from the Spotify API, extract the access token and store it as a custom variable.

![Add request payload token](../../_img/api-payload-token.png)
