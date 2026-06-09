import SwiftUI

struct CartView: View {
    @EnvironmentObject private var store: WorkshopStore

    var body: some View {
        List {
            if store.cartItems.isEmpty {
                ContentUnavailableView(
                    "Cart is empty",
                    systemImage: "cart",
                    description: Text("Add an item from the catalog to continue to checkout.")
                )
            } else {
                Section("Items") {
                    ForEach(store.cartItems) { item in
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(item.product.name)
                                    .font(.headline)
                                Text("Quantity \(item.quantity)")
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            Text(item.lineTotal.currencyText)
                                .fontWeight(.semibold)
                        }
                    }
                    .onDelete { offsets in
                        offsets
                            .map { store.cartItems[$0] }
                            .forEach(store.removeFromCart)
                    }
                }

                Section {
                    HStack {
                        Text("Total")
                        Spacer()
                        Text(store.cartTotal.currencyText)
                            .fontWeight(.bold)
                    }

                    NavigationLink {
                        CheckoutView()
                    } label: {
                        Label("Begin checkout", systemImage: "creditcard")
                    }
                }
            }
        }
        .navigationTitle("Cart")
        .onAppear {
            store.screenViewed("Cart", feature: "cart")
        }
    }
}
