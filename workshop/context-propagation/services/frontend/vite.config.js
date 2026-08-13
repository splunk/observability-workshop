import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    define: {
      'import.meta.env.VITE_SPLUNK_RUM_REALM': JSON.stringify(env.REALM ?? ''),
      'import.meta.env.VITE_SPLUNK_RUM_TOKEN': JSON.stringify(env.RUM_TOKEN ?? ''),
      'import.meta.env.VITE_SPLUNK_APP_NAME': JSON.stringify(env.RUM_APP_NAME ?? 'cosmic-observatory-shop'),
      'import.meta.env.VITE_SPLUNK_ENV': JSON.stringify(env.DEPLOYMENT_ENV ?? 'workshop'),
      'import.meta.env.VITE_API_BASE': JSON.stringify(env.VITE_API_BASE ?? ''),
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: env.VITE_DEV_PROXY || 'http://localhost:8080',
          changeOrigin: true,
        },
      },
    },
  };
});
