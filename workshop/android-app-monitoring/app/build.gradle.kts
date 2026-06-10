plugins {
    id("com.android.application")
}

android {
    namespace = "com.splunk.workshop.androidrum"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.splunk.workshop.androidrum"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0-workshop"

        val splunkRealm = providers.gradleProperty("splunkRealm").orElse("us1").get()
        val splunkRumAccessToken = providers.gradleProperty("splunkRumAccessToken").orElse("").get()
        val splunkRumAppName = providers.gradleProperty("splunkRumAppName").orElse("buttercup-android").get()
        val splunkRumEnvironment = providers.gradleProperty("splunkRumEnvironment").orElse("workshop").get()

        buildConfigField("String", "SPLUNK_REALM", "\"$splunkRealm\"")
        buildConfigField("String", "SPLUNK_RUM_ACCESS_TOKEN", "\"$splunkRumAccessToken\"")
        buildConfigField("String", "SPLUNK_RUM_APP_NAME", "\"$splunkRumAppName\"")
        buildConfigField("String", "SPLUNK_RUM_ENVIRONMENT", "\"$splunkRumEnvironment\"")
    }

    buildFeatures {
        buildConfig = true
    }

    compileOptions {
        isCoreLibraryDesugaringEnabled = true
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation("com.splunk:splunk-otel-android:2.3.1")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.3")
}
