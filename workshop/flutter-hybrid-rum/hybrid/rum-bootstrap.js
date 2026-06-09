(function bootstrapSplunkRum(config) {
  if (!window.SplunkRum) {
    console.warn('SplunkRum is not available. Load the browser RUM agent first.');
    return;
  }

  window.SplunkRum.init({
    realm: config.realm,
    rumAccessToken: config.rumAccessToken,
    applicationName: config.applicationName,
    deploymentEnvironment: config.environment,
    version: config.appVersion,
    globalAttributes: {
      'app.platform': 'hybrid-webview',
      'app.shell': config.shell,
      'app.webview': 'true',
      'app.version': config.appVersion
    }
  });
})(window.__RUM_CONFIG__ || {});
