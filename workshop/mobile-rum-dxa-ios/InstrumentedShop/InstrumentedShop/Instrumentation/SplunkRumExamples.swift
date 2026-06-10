import Foundation

#if canImport(SplunkAgent)
import SplunkAgent

enum SplunkRumAutoInstrumentationExample {
    static func install() {
        let globalAttributes = MutableAttributes()
        globalAttributes[string: "app.team"] = "mobile-experience"
        globalAttributes[string: "workshop.name"] = "mobile-rum-dxa-ios"

        let agentConfiguration = AgentConfiguration(
            endpoint: EndpointConfiguration(
                realm: "YOUR_REALM",
                rumAccessToken: "YOUR_RUM_ACCESS_TOKEN"
            ),
            appName: "InstrumentedShop",
            deploymentEnvironment: "workshop"
        )
        .appVersion(Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0")
        .globalAttributes(globalAttributes)
        .sessionConfiguration(SessionConfiguration(samplingRate: 1))
        .spanInterceptor { spanData in
            var attributes = spanData.attributes
            attributes["http.url"] = .string("redacted")
            attributes["url.full"] = .string("redacted")

            return spanData.settingAttributes(attributes)
        }

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

enum SplunkRumCustomInstrumentationExample {
    static func screenViewed(_ name: String) {
        SplunkRum.shared.navigation.track(screen: name)
    }

    static func productViewed(_ product: Product) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "catalog"
        attributes[string: "product.category"] = product.category

        SplunkRum.shared.customTracking.trackCustomEvent("Product Viewed", attributes)
    }

    static func addToCart(product: Product, cartSize: Int) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "cart"
        attributes[string: "product.category"] = product.category
        attributes[int: "cart.size"] = cartSize

        SplunkRum.shared.customTracking.trackCustomEvent("Add To Cart", attributes)
    }

    static func checkoutStarted(cartSize: Int) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "checkout"
        attributes[int: "cart.size"] = cartSize

        SplunkRum.shared.customTracking.trackCustomEvent("Checkout Started", attributes)
    }

    static func checkoutFailed(step: String, errorType: String) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "checkout"
        attributes[string: "checkout.step"] = step
        attributes[string: "error.type"] = errorType

        SplunkRum.shared.customTracking.trackCustomEvent("Checkout Failed", attributes)
    }

    static func trackCheckoutSubmission<T>(
        method: String,
        cartSize: Int,
        operation: () async throws -> T
    ) async rethrows -> T {
        let span = SplunkRum.shared.customTracking.trackWorkflow("Order Submitted")
        span.setAttribute(key: "app.feature", value: "checkout")
        span.setAttribute(key: "checkout.method", value: method)
        span.setAttribute(key: "cart.size", value: "\(cartSize)")

        defer {
            span.end()
        }

        do {
            let value = try await operation()
            span.setAttribute(key: "result", value: "success")
            return value
        } catch {
            let errorType = String(describing: type(of: error))
            span.setAttribute(key: "result", value: "failure")
            span.setAttribute(key: "error.type", value: errorType)
            checkoutFailed(step: "submit", errorType: errorType)
            throw error
        }
    }
}
#endif
