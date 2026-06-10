class RumConfig {
  const RumConfig({
    required this.realm,
    required this.accessToken,
    required this.applicationName,
    required this.hybridApplicationName,
    required this.environment,
    required this.appVersion,
    required this.apiBaseUrl,
    required this.rumAgentVersion,
  });

  factory RumConfig.fromEnvironment() {
    return const RumConfig(
      realm: String.fromEnvironment('SPLUNK_RUM_REALM', defaultValue: 'us1'),
      accessToken: String.fromEnvironment(
        'SPLUNK_RUM_ACCESS_TOKEN',
        defaultValue: 'replace-with-your-rum-token',
      ),
      applicationName: String.fromEnvironment(
        'SPLUNK_RUM_APPLICATION_NAME',
        defaultValue: 'mobile-checkout',
      ),
      hybridApplicationName: String.fromEnvironment(
        'SPLUNK_RUM_HYBRID_APPLICATION_NAME',
        defaultValue: 'mobile-checkout-webview',
      ),
      environment: String.fromEnvironment(
        'SPLUNK_RUM_ENVIRONMENT',
        defaultValue: 'workshop',
      ),
      appVersion: String.fromEnvironment(
        'SPLUNK_RUM_APP_VERSION',
        defaultValue: '1.0.0',
      ),
      apiBaseUrl: String.fromEnvironment(
        'SHOP_API_BASE_URL',
        defaultValue: 'https://httpbin.org',
      ),
      rumAgentVersion: String.fromEnvironment(
        'SPLUNK_RUM_AGENT_VERSION',
        defaultValue: 'v3',
      ),
    );
  }

  final String realm;
  final String accessToken;
  final String applicationName;
  final String hybridApplicationName;
  final String environment;
  final String appVersion;
  final String apiBaseUrl;
  final String rumAgentVersion;

  bool get liveRumEnabled {
    return accessToken.isNotEmpty &&
        !accessToken.startsWith('replace-with') &&
        accessToken != 'YOUR_RUM_ACCESS_TOKEN';
  }
}
