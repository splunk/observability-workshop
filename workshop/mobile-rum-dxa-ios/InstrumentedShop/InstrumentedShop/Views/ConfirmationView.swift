import SwiftUI

struct ConfirmationView: View {
    @EnvironmentObject private var store: WorkshopStore
    let confirmation: OrderConfirmation

    var body: some View {
        VStack(spacing: 18) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 76))
                .foregroundStyle(.green)

            Text("Order submitted")
                .font(.largeTitle.weight(.bold))

            VStack(spacing: 8) {
                Text(confirmation.orderNumber)
                    .font(.title2.monospacedDigit().weight(.semibold))
                Text(confirmation.total.currencyText)
                    .font(.title3)
                    .foregroundStyle(.secondary)
                Text(confirmation.createdAt.formatted(date: .abbreviated, time: .shortened))
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .padding()
        .navigationTitle("Confirmation")
        .onAppear {
            store.screenViewed("Order Confirmation", feature: "checkout")
        }
    }
}
