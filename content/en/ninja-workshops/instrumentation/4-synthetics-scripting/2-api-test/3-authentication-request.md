---
title: Authentication Request
linkTitle: 1.3 Authentication Request
weight: 3
---

## A quick note on what we're doing

Before we click anything, here's the OAuth 2 flow we're modelling:

1. Spotify (like most modern APIs) requires a short-lived bearer token on every authenticated request.
2. To obtain that token, we make a single `POST` to the OAuth token endpoint, sending our `client_id:client_secret` (Base64-encoded) in an HTTP Basic auth header and `grant_type=client_credentials` in the body. This is the **Client Credentials grant** — the machine-to-machine variant of OAuth 2, designed for backend services that need to call an API on their own behalf rather than on behalf of a logged-in user.
3. Spotify responds with JSON containing an `access_token`. We extract it, store it as a Synthetic Monitoring **custom variable**, and use it as the `Authorization: Bearer …` header on every subsequent request.

This same pattern is how most modern APIs authenticate service-to-service traffic, so what you build here is a template for monitoring any OAuth-protected backend.

## Add the authentication request

Click {{< button >}}+ Add requests{{< /button >}} and enter the request step name **Authenticate with Spotify API**. Meaningful names matter here for the same reason they did in the RBT — when a step fails, the alert message will use this name verbatim.

![New API request with the step name field filled in](../../img/add-request.png)

Expand the **Request** section, change the request method to **POST** from the dropdown, and enter the URL:

``` text
https://accounts.spotify.com/api/token
```

In the **Payload body** section enter:

``` text
grant_type=client_credentials
```

The `grant_type=client_credentials` value tells Spotify which OAuth flow we want. The body is `application/x-www-form-urlencoded` — the legacy form-post encoding — which is the standard for OAuth token endpoints (it predates the widespread use of JSON in API bodies).

Next, add two request headers with the following key/value pairings:

- **CONTENT-TYPE: application/x-www-form-urlencoded** — tells Spotify how to parse the body we just supplied.
- **AUTHORIZATION: Basic {{env.encoded_auth}}** — the workshop's pre-configured global variable from the previous chapter, expanded inline by the test runner. The runner sends the literal Base64 string; the variable name is never on the wire.

## Extract the access token

Spotify's response for a successful token request looks something like this:

``` json
{
  "access_token": "BQDxx...long-opaque-string...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

We need the `access_token` value for the next step. Expand the **Validation** section of the request and add the following extraction:

- **Extract** from **Response body** **JSON** **$.access_token** **as** **access_token**.

The `$.access_token` is a [**JSONPath**](https://goessner.net/articles/JsonPath/) expression — the JSON equivalent of XPath. `$` is the root of the document and `.access_token` selects the top-level field. JSONPath also supports array indexing, wildcards, and filters; we'll use the array form in the next chapter.

The extracted value is now available to all subsequent steps as `{{custom.access_token}}` — the `custom.` namespace is for variables produced *during* this run, in contrast to the `env.` namespace which is for organisation-level static values.

![Validation panel with JSONPath extraction for $.access_token configured](../../img/add-payload-token.png)
