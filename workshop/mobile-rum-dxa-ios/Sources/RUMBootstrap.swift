import Foundation
import SplunkAgent

final class WorkshopNavigationProcessor: NavigationEventProcessor {
    func onViewController(
        typeName: String,
        controllerIdentity: String
    ) -> NavigationEvent? {
        let mappedName = [
            "ProductDetailViewController": "Product Detail",
            "CartViewController": "Cart",
            "CheckoutViewController": "Checkout"
        ][typeName] ?? typeName.replacingOccurrences(of: "ViewController", with: "")

        return NavigationEvent(
            name: mappedName,
            attributes: [
                "app.feature": "checkout",
                "app.team": "mobile"
            ]
        )
    }
}

enum RUMBootstrap {
    static func install() {
        let endpointConfiguration = EndpointConfiguration(
            realm: "YOUR_REALM",
            rumAccessToken: "YOUR_RUM_ACCESS_TOKEN"
        )

        let agentConfiguration = AgentConfiguration(
            endpoint: endpointConfiguration,
            appName: "YOUR_APP_NAME",
            deploymentEnvironment: "YOUR_DEPLOYMENT_ENVIRONMENT"
        ).spanInterceptor(PrivacySpanInterceptor.redact)

        let navigationConfig = NavigationConfiguration(
            isEnabled: true,
            enableAutomatedTracking: true,
            navigationEventProcessor: WorkshopNavigationProcessor()
        )

        do {
            let agent = try SplunkRum.install(
                with: agentConfiguration,
                moduleConfigurations: [navigationConfig]
            )

            SplunkRum.shared.user.preferences.trackingMode = .anonymousTracking
            agent.navigation.preferences.enableAutomatedTracking = true
            agent.sessionReplay.start()
        } catch {
            print("Unable to start the Splunk RUM iOS agent: \(error)")
        }
    }
}
