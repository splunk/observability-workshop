import Foundation
import SplunkAgent

enum MobileJourneyInstrumentation {
    static func reportProductViewed(category: String) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "catalog"
        attributes[string: "product.category"] = category

        SplunkRum.shared.customTracking.trackCustomEvent("Product Viewed", attributes)
    }

    static func reportAddToCart(category: String, cartSize: Int) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "cart"
        attributes[string: "product.category"] = category
        attributes[int: "cart.size"] = cartSize

        SplunkRum.shared.customTracking.trackCustomEvent("Add To Cart", attributes)
    }

    static func reportCheckoutStarted(cartSize: Int) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "checkout"
        attributes[int: "cart.size"] = cartSize

        SplunkRum.shared.customTracking.trackCustomEvent("Checkout Started", attributes)
    }

    static func runCheckoutSubmission(
        method: String,
        operation: () throws -> Void
    ) rethrows {
        let span = SplunkRum.shared.customTracking.trackWorkflow("Order Submitted")
        span.setAttribute(key: "app.feature", value: "checkout")
        span.setAttribute(key: "checkout.method", value: method)

        defer {
            span.end()
        }

        do {
            try operation()
            span.setAttribute(key: "result", value: "success")
        } catch {
            span.setAttribute(key: "result", value: "failure")
            span.setAttribute(key: "error.type", value: String(describing: type(of: error)))
            throw error
        }
    }

    static func reportCheckoutFailed(step: String, errorType: String) {
        let attributes = MutableAttributes()
        attributes[string: "app.feature"] = "checkout"
        attributes[string: "checkout.step"] = step
        attributes[string: "error.type"] = errorType

        SplunkRum.shared.customTracking.trackCustomEvent("Checkout Failed", attributes)
    }
}
