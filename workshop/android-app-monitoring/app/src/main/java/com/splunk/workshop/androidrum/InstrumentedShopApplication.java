package com.splunk.workshop.androidrum;

import android.app.Application;
import android.util.Log;

import com.splunk.rum.integration.agent.api.AgentConfiguration;
import com.splunk.rum.integration.agent.api.EndpointConfiguration;
import com.splunk.rum.integration.agent.api.SplunkRum;
import com.splunk.rum.integration.agent.api.session.SessionConfiguration;
import com.splunk.rum.integration.agent.api.user.UserConfiguration;
import com.splunk.rum.integration.agent.api.user.UserTrackingMode;
import com.splunk.rum.integration.agent.common.attributes.MutableAttributes;
import com.splunk.rum.integration.agent.common.module.ModuleConfiguration;
import com.splunk.rum.integration.anr.AnrModuleConfiguration;
import com.splunk.rum.integration.applicationlifecycle.ApplicationLifecycleModuleConfiguration;
import com.splunk.rum.integration.crash.CrashModuleConfiguration;
import com.splunk.rum.integration.interactions.InteractionsModuleConfiguration;
import com.splunk.rum.integration.navigation.NavigationModuleConfiguration;
import com.splunk.rum.integration.networkmonitor.NetworkMonitorModuleConfiguration;
import com.splunk.rum.integration.okhttp3.manual.OkHttp3ManualModuleConfiguration;
import com.splunk.rum.integration.slowrendering.SlowRenderingModuleConfiguration;
import com.splunk.rum.integration.startup.StartupModuleConfiguration;

import java.util.Arrays;

import okhttp3.Call;
import okhttp3.OkHttpClient;

public class InstrumentedShopApplication extends Application {
    private static final String TAG = "ButtercupRum";
    private static SplunkRum rum = SplunkRum.noop();
    private static boolean rumConfigured = false;

    @Override
    public void onCreate() {
        super.onCreate();

        if (!hasRumToken()) {
            Log.w(TAG, "RUM token is not configured. The app will run with no-op instrumentation.");
            return;
        }

        MutableAttributes globalAttributes = new MutableAttributes();
        globalAttributes.set("app.release_channel", BuildConfig.DEBUG ? "debug" : "release");
        globalAttributes.set("business.unit", "retail");
        globalAttributes.set("workshop.name", "android-app-monitoring");

        AgentConfiguration agentConfiguration = new AgentConfiguration(
                new EndpointConfiguration(BuildConfig.SPLUNK_REALM, BuildConfig.SPLUNK_RUM_ACCESS_TOKEN),
                BuildConfig.SPLUNK_RUM_APP_NAME,
                BuildConfig.SPLUNK_RUM_ENVIRONMENT,
                BuildConfig.VERSION_NAME,
                BuildConfig.DEBUG,
                globalAttributes,
                spanData -> spanData,
                new UserConfiguration(UserTrackingMode.ANONYMOUS_TRACKING),
                new SessionConfiguration(1.0),
                null,
                false
        );

        ModuleConfiguration[] moduleConfigurations = new ModuleConfiguration[] {
                new AnrModuleConfiguration(),
                new CrashModuleConfiguration(),
                new InteractionsModuleConfiguration(),
                new NavigationModuleConfiguration(true, true),
                new NetworkMonitorModuleConfiguration(),
                new OkHttp3ManualModuleConfiguration(
                        Arrays.asList("Accept", "Content-Type"),
                        Arrays.asList("Content-Type", "Server-Timing")
                ),
                new SlowRenderingModuleConfiguration(true),
                new StartupModuleConfiguration(),
                new ApplicationLifecycleModuleConfiguration(true)
        };

        rum = SplunkRum.install(this, agentConfiguration, moduleConfigurations);
        rumConfigured = true;
        Log.i(TAG, "Splunk RUM initialized for " + BuildConfig.SPLUNK_RUM_APP_NAME);
    }

    public static SplunkRum rum() {
        return rum;
    }

    public static boolean isRumConfigured() {
        return rumConfigured;
    }

    public static Call.Factory instrumentedCallFactory(OkHttpClient client) {
        if (!rumConfigured) {
            return client;
        }
        return rum.createRumOkHttpCallFactory(client);
    }

    private boolean hasRumToken() {
        String token = BuildConfig.SPLUNK_RUM_ACCESS_TOKEN;
        return token != null
                && !token.trim().isEmpty()
                && !token.contains("replace")
                && !token.contains("YOUR_ACCESS_TOKEN");
    }
}
