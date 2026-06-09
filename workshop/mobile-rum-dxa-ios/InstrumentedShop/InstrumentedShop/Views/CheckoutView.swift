import SwiftUI

struct CheckoutView: View {
    @EnvironmentObject private var store: WorkshopStore
    @State private var email = "student@example.com"
    @State private var city = "Chicago"
    @State private var paymentMethod = "card"
    @State private var simulateFailure = false
    @State private var errorMessage: String?
    @State private var confirmation: OrderConfirmation?

    var body: some View {
        Form {
            Section("Contact") {
                TextField("Email", text: $email)
                    .textContentType(.emailAddress)
                    .textInputAutocapitalization(.never)
                    .keyboardType(.emailAddress)
                    .privacySensitive()
                TextField("City", text: $city)
                    .textContentType(.addressCity)
            }

            Section("Payment") {
                Picker("Method", selection: $paymentMethod) {
                    Text("Card").tag("card")
                    Text("Apple Pay").tag("apple_pay")
                    Text("Invoice").tag("invoice")
                }
                Toggle("Simulate checkout failure", isOn: $simulateFailure)
            }
            .privacySensitive()

            Section {
                Button {
                    submit()
                } label: {
                    if store.isSubmittingCheckout {
                        ProgressView()
                            .frame(maxWidth: .infinity)
                    } else {
                        Label("Submit order", systemImage: "checkmark.circle")
                            .frame(maxWidth: .infinity)
                    }
                }
                .disabled(store.isSubmittingCheckout)
            }

            if let errorMessage {
                Section("Checkout error") {
                    Text(errorMessage)
                        .foregroundStyle(.red)
                }
            }
        }
        .navigationTitle("Checkout")
        .navigationDestination(item: $confirmation) { confirmation in
            ConfirmationView(confirmation: confirmation)
        }
        .onAppear {
            store.screenViewed("Checkout", feature: "checkout")
            store.checkoutStarted()
        }
    }

    private func submit() {
        errorMessage = nil

        Task {
            do {
                confirmation = try await store.submitCheckout(
                    paymentMethod: paymentMethod,
                    shouldFail: simulateFailure
                )
            } catch {
                errorMessage = error.localizedDescription
            }
        }
    }
}
