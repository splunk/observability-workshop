import SwiftUI

struct ProductDetailView: View {
    @EnvironmentObject private var store: WorkshopStore
    let product: Product

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                Image(systemName: product.symbolName)
                    .font(.system(size: 72))
                    .frame(maxWidth: .infinity, minHeight: 180)
                    .foregroundStyle(.white)
                    .background(.pink.gradient)
                    .clipShape(RoundedRectangle(cornerRadius: 8))

                VStack(alignment: .leading, spacing: 8) {
                    Text(product.category.uppercased())
                        .font(.caption.weight(.bold))
                        .foregroundStyle(.secondary)
                    Text(product.name)
                        .font(.largeTitle.weight(.bold))
                    Text(product.price.currencyText)
                        .font(.title2.weight(.semibold))
                    Text(product.detail)
                        .foregroundStyle(.secondary)
                }

                Button {
                    store.addToCart(product)
                } label: {
                    Label("Add to cart", systemImage: "cart.badge.plus")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)

                NavigationLink {
                    CartView()
                } label: {
                    Label("Review cart", systemImage: "cart")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
                .controlSize(.large)
            }
            .padding()
        }
        .navigationTitle("Product Detail")
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            store.screenViewed("Product Detail", feature: "catalog")
            store.productViewed(product)
        }
    }
}
