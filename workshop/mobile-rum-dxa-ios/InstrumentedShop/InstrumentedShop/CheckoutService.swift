import Foundation

struct CheckoutService {
    func submit(
        items: [CartItem],
        paymentMethod: String,
        shouldFail: Bool
    ) async throws -> OrderConfirmation {
        guard !items.isEmpty else {
            throw CheckoutError.emptyCart
        }

        try await Task.sleep(for: .milliseconds(850))

        if shouldFail {
            throw CheckoutError.simulatedPaymentFailure
        }

        let total = items.reduce(0) { $0 + $1.lineTotal }
        let suffix = UUID().uuidString.prefix(6).uppercased()

        return OrderConfirmation(
            id: String(suffix),
            orderNumber: "SPL-\(suffix)",
            total: total,
            createdAt: Date()
        )
    }
}
