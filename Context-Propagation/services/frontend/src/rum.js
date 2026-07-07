import { SplunkRum } from '@splunk/otel-web';
import SplunkSessionRecorder from '@splunk/otel-web-session-recorder';

const realm = import.meta.env.VITE_SPLUNK_RUM_REALM;
const token = import.meta.env.VITE_SPLUNK_RUM_TOKEN;

export function initSplunkRum() {
  if (!realm || !token || token === 'YOUR_RUM_ACCESS_TOKEN') {
    console.warn(
      '[Splunk RUM] Skipping initialization — set SPLUNK_REALM and SPLUNK_RUM_ACCESS_TOKEN in .env',
    );
    return;
  }

  SplunkRum.init({
    realm,
    rumAccessToken: token,
    applicationName: import.meta.env.VITE_SPLUNK_APP_NAME || 'cosmic-observatory-shop',
    deploymentEnvironment: import.meta.env.VITE_SPLUNK_ENV || 'workshop',
    version: '1.0.0',
    instrumentations: {
      fetch: true,
      xhr: true,
      document: true,
      interactions: true,
    },
    globalAttributes: {
      'app.theme': 'astronomy',
      'workshop.name': 'context-propagation',
    },
  });

  SplunkSessionRecorder.init({
    realm,
    rumAccessToken: token,
    recorder: 'splunk',
  });

  console.info('[Splunk RUM] Initialized with session replay for Cosmic Observatory Shop');
}
