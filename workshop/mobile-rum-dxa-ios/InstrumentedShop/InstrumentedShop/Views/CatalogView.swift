import SwiftUI

struct CatalogView: View {
    @EnvironmentObject private var store: WorkshopStore

    var body: some View {
        List {
            Section {
                ForEach(store.products) { product in
                    NavigationLink(value: product) {
                        ProductRow(product: product)
                    }
                }
            } header: {
                Text("Catalog")
            } footer: {
                Text("Browse the current workshop catalog.")
            }
        }
        .navigationTitle("Instrumented Shop")
        .navigationDestination(for: Product.self) { product in
            ProductDetailView(product: product)
        }
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                NavigationLink {
                    CartView()
                } label: {
                    Label("Cart", systemImage: "cart")
                        .symbolVariant(store.cartCount > 0 ? .fill : .none)
                }
                .accessibilityLabel("Cart, \(store.cartCount) items")
            }
        }
        .onAppear {
            store.screenViewed("Catalog", feature: "catalog")
        }
    }
}

private struct ProductRow: View {
    let product: Product

    var body: some View {
        HStack(spacing: 14) {
            Image(systemName: product.symbolName)
                .font(.title2)
                .frame(width: 40, height: 40)
                .foregroundStyle(.white)
                .background(.pink.gradient)
                .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading, spacing: 4) {
                Text(product.name)
                    .font(.headline)
                Text(product.summary)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
                Text(product.price.currencyText)
                    .font(.subheadline.weight(.semibold))
            }
        }
        .padding(.vertical, 6)
    }
}
