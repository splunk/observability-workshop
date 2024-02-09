---
title: 1.5 Advanced Settings
weight: 5
---

Click on **Advanced**, these settings are optional and can be used to further configure the test.

{{% notice note %}}
In the case of this workshop, we will **not** be using any of these settings as this is for informational purposes only.
{{% /notice %}}

![Advanced Settings](../_img/advanced-settings.png)

- **Security**:
  - **TLS/SSL validation**: When activated, this feature is used to enforce the validation of expired, invalid hostname, or untrusted issuer on SSL/TLS certificates.
  - **Authentication**: Add credentials to authenticate with sites that require additional security protocols, for example from within a corporate network. By using [concealed global variables](https://docs.splunk.com/Observability/synthetics/test-config/global-variables.html) in the Authentication field, you create an additional layer of security for your credentials and simplify the ability to share credentials across checks.
- **Custom Content**:
  - **Custom headers**: Specify custom headers to send with each request. For example, you can add a header in your request to filter out requests from analytics on the back end by sending a specific header in the requests. You can also use custom headers to set cookies.
  - **Cookies**: Set cookies in the browser before the test starts. For example, to prevent a popup modal from randomly appearing and interfering with your test, you can set cookies. Any cookies that are set will apply to the domain of the starting URL of the check. Splunk Synthetics Monitoring uses the public suffix list to determine the domain.
  - **Host overrides**: Add host override rules to reroute requests from one host to another. For example, you can create a host override to test an existing production site against page resources loaded from a development site or a specific CDN edge node.

Next, we will edit the test steps to provide more meaningful names for each step.
