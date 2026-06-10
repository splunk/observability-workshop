import Foundation
import SplunkAgent

enum RUMBootstrap {
    static func install() {
        let globalAttributes = MutableAttributes()
        globalAttributes[string: "app.team"] = "mobile-experience"
        globalAttributes[string: "workshop.name"] = "mobile-rum-dxa-ios"

        let endpointConfiguration = EndpointConfiguration(
            realm: "YOUR_REALM",
            rumAccessToken: "YOUR_RUM_ACCESS_TOKEN"
        )

        let agentConfiguration = AgentConfiguration(
            endpoint: endpointConfiguration,
            appName: "YOUR_APP_NAME",
            deploymentEnvironment: "YOUR_DEPLOYMENT_ENVIRONMENT"
        )
        .globalAttributes(globalAttributes)
        .spanInterceptor(PrivacySpanInterceptor.redact)

        do {
            let agent = try SplunkRum.install(with: agentConfiguration)

            agent.user.preferences.trackingMode = .anonymousTracking
            agent.navigation.preferences.enableAutomatedTracking = true
            agent.sessionReplay.start()
        } catch {
            print("Unable to start the Splunk RUM iOS agent: \(error)")
        }
    }
}
