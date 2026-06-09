import Foundation

struct Product: Identifiable, Hashable {
    let id: String
    let name: String
    let category: String
    let price: Double
    let summary: String
    let detail: String
    let symbolName: String
}

struct CartItem: Identifiable, Hashable {
    let product: Product
    var quantity: Int

    var id: String {
        product.id
    }

    var lineTotal: Double {
        product.price * Double(quantity)
    }
}

struct OrderConfirmation: Identifiable, Hashable {
    let id: String
    let orderNumber: String
    let total: Double
    let createdAt: Date
}

enum CheckoutError: LocalizedError {
    case emptyCart
    case simulatedPaymentFailure

    var errorDescription: String? {
        switch self {
        case .emptyCart:
            "The cart is empty."
        case .simulatedPaymentFailure:
            "The payment service returned a controlled workshop failure."
        }
    }
}

enum TelemetryKind: String, CaseIterable {
    case bootstrap = "Bootstrap"
    case screen = "Screen"
    case interaction = "Interaction"
    case workflow = "Workflow"
    case network = "Network"
    case privacy = "Privacy"
    case error = "Error"
}

struct TelemetryEvent: Identifiable, Hashable {
    let id = UUID()
    let timestamp: Date
    let kind: TelemetryKind
    let name: String
    let attributes: [String: String]
}

extension Double {
    var currencyText: String {
        formatted(.currency(code: "USD"))
    }
}

extension Product {
    static let workshopProducts: [Product] = [
        Product(
            id: "pack-trace",
            name: "Trace Explorer Pack",
            category: "observability",
            price: 49,
            summary: "A field kit for debugging slow mobile journeys.",
            detail: "A compact kit for teams practicing mobile troubleshooting across slow screens, retries, and checkout handoffs.",
            symbolName: "point.3.connected.trianglepath.dotted"
        ),
        Product(
            id: "pack-rum",
            name: "RUM Signal Pack",
            category: "mobile",
            price: 59,
            summary: "Session, screen, and interaction signals in one bundle.",
            detail: "A signal bundle for teams who need to understand app launches, screen transitions, interactions, and user journeys.",
            symbolName: "iphone.gen3.radiowaves.left.and.right"
        ),
        Product(
            id: "pack-replay",
            name: "Replay Privacy Kit",
            category: "privacy",
            price: 39,
            summary: "Practice masking sensitive checkout fields.",
            detail: "A privacy review kit focused on checkout fields, account details, payment controls, and replay-safe troubleshooting.",
            symbolName: "eye.slash"
        )
    ]
}
