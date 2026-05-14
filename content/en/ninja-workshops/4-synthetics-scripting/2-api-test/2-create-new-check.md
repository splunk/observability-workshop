---
title: Create new API test
linkTitle: 1.2 Create new API test
weight: 2
---

## Create a new API test

From the **Synthetics** landing page, click {{< button style="blue" >}}Add new test{{< /button >}} and select **API test** from the dropdown.

Name the test using **your initials** followed by **Spotify API** — for example **RWC - Spotify API**. The same naming convention applies as in Part 1: prefix with your initials so the test is easy to find in a shared organisation, and include the system under test in the name so alert messages are self-describing.

![Add new API test dialog with the test name field filled in](../../img/new-api-check.png)

Once you click {{< button style="blue" >}}Submit{{< /button >}} you'll land on the **API Test content** page. This is where you'll add the two requests that make up our synthetic business transaction:

1. **Authenticate with Spotify API** — a `POST` to the OAuth token endpoint that exchanges our client credentials for an access token, which we'll extract and stash as a custom variable.
2. **Search for tracks** — a `GET` to the search endpoint, sending the token from step 1 as a Bearer credential, and extracting an item from the JSON response.

We'll build them one at a time in the next two chapters.
