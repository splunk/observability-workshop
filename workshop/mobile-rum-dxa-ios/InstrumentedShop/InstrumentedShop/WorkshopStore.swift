import Foundation

@MainActor
final class WorkshopStore: ObservableObject {
    @Published private(set) var products: [Product] = Product.workshopProducts
    @Published private(set) var cartItems: [CartItem] = []
    @Published private(set) var events: [TelemetryEvent] = []
    @Published private(set) var isSubmittingCheckout = false

    private let instrumentation = TrainingRumInstrumentation()
    private let checkoutService = CheckoutService()
    private var didBootstrap = false

    init() {
        instrumentation.onEvent = { [weak self] event in
            self?.events.insert(event, at: 0)
        }
    }

    var cartCount: Int {
        cartItems.reduce(0) { $0 + $1.quantity }
    }

    var cartTotal: Double {
        cartItems.reduce(0) { $0 + $1.lineTotal }
    }

    func bootstrapIfNeeded() {
        guard !didBootstrap else {
            return
        }

        didBootstrap = true
        instrumentation.start(
            configuration: RumConfiguration(
                realm: "us1",
                rumAccessToken: "training-mode",
                applicationName: "ios-dxa-workshop",
                deploymentEnvironment: "workshop",
                appVersion: Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0"
            )
        )
        instrumentation.enableAutomaticNavigationTracking()
        instrumentation.enableAnonymousTracking()
        instrumentation.startSessionReplay()
    }

    func screenViewed(_ name: String, feature: String) {
        instrumentation.screenViewed(name, attributes: [
            "app.feature": feature,
            "instrumentation.type": "automatic"
        ])
    }

    func productViewed(_ product: Product) {
        instrumentation.customEvent("Product Viewed", attributes: [
            "app.feature": "catalog",
            "instrumentation.type": "custom",
            "product.category": product.category
        ])
    }

    func addToCart(_ product: Product) {
        if let index = cartItems.firstIndex(where: { $0.product.id == product.id }) {
            cartItems[index].quantity += 1
        } else {
            cartItems.append(CartItem(product: product, quantity: 1))
        }

        instrumentation.customEvent("Add To Cart", attributes: [
            "app.feature": "cart",
            "instrumentation.type": "custom",
            "product.category": product.category,
            "cart.size": "\(cartCount)"
        ])
    }

    func removeFromCart(_ item: CartItem) {
        cartItems.removeAll { $0.id == item.id }
        instrumentation.customEvent("Remove From Cart", attributes: [
            "app.feature": "cart",
            "instrumentation.type": "custom",
            "cart.size": "\(cartCount)"
        ])
    }

    func checkoutStarted() {
        instrumentation.customEvent("Checkout Started", attributes: [
            "app.feature": "checkout",
            "instrumentation.type": "custom",
            "cart.size": "\(cartCount)"
        ])
        instrumentation.markSensitiveView("checkout.email")
        instrumentation.markSensitiveView("checkout.payment")
    }

    func submitCheckout(paymentMethod: String, shouldFail: Bool) async throws -> OrderConfirmation {
        guard !cartItems.isEmpty else {
            instrumentation.customEvent("Checkout Failed", attributes: [
                "app.feature": "checkout",
                "instrumentation.type": "custom",
                "checkout.step": "preflight",
                "error.type": "empty_cart"
            ])
            throw CheckoutError.emptyCart
        }

        isSubmittingCheckout = true
        let workflow = instrumentation.startWorkflow("Order Submitted", attributes: [
            "app.feature": "checkout",
            "instrumentation.type": "custom",
            "checkout.method": paymentMethod,
            "cart.size": "\(cartCount)"
        ])
        instrumentation.networkRequest("POST /checkout", attributes: [
            "http.method": "POST",
            "server.address": "api.workshop.example"
        ])

        do {
            let confirmation = try await checkoutService.submit(
                items: cartItems,
                paymentMethod: paymentMethod,
                shouldFail: shouldFail
            )
            instrumentation.finishWorkflow(workflow, result: "success", attributes: [
                "order.total": cartTotal.currencyText
            ])
            cartItems.removeAll()
            isSubmittingCheckout = false
            return confirmation
        } catch {
            instrumentation.finishWorkflow(workflow, result: "failure", attributes: [
                "error.type": String(describing: type(of: error))
            ])
            instrumentation.customEvent("Checkout Failed", attributes: [
                "app.feature": "checkout",
                "instrumentation.type": "custom",
                "checkout.step": "submit",
                "error.type": String(describing: type(of: error))
            ])
            isSubmittingCheckout = false
            throw error
        }
    }

    func clearTelemetry() {
        events.removeAll()
        instrumentation.customEvent("Telemetry Cleared", attributes: [
            "app.feature": "training",
            "instrumentation.type": "custom"
        ])
    }
}
