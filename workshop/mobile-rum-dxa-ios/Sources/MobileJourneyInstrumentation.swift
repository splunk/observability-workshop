import Foundation
import SplunkAgent

enum MobileJourneyInstrumentation {
    static func reportProductViewed(category: String) {
        let attributes: NSDictionary = [
            "app.feature": "catalog",
            "product.category": category
        ]

        SplunkRum.shared.customTracking.trackCustomEvent(
            name: "Product Viewed",
            attributes: attributes
        )
    }

    static func reportAddToCart(category: String, cartSize: Int) {
        let attributes: NSDictionary = [
            "app.feature": "cart",
            "product.category": category,
            "cart.size": cartSize
        ]

        SplunkRum.shared.customTracking.trackCustomEvent(
            name: "Add To Cart",
            attributes: attributes
        )
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
        let attributes: NSDictionary = [
            "app.feature": "checkout",
            "checkout.step": step,
            "error.type": errorType
        ]

        SplunkRum.shared.customTracking.trackCustomEvent(
            name: "Checkout Failed",
            attributes: attributes
        )
    }
}
