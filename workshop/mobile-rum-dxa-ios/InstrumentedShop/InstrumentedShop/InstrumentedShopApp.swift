import SwiftUI

@main
struct InstrumentedShopApp: App {
    @StateObject private var store = WorkshopStore()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(store)
                .task {
                    store.bootstrapIfNeeded()
                }
        }
    }
}

struct RootView: View {
    @EnvironmentObject private var store: WorkshopStore

    var body: some View {
        TabView {
            NavigationStack {
                CatalogView()
            }
            .tabItem {
                Label("Shop", systemImage: "bag")
            }

            TelemetryView()
                .tabItem {
                    Label("Telemetry", systemImage: "waveform.path.ecg")
                }
                .badge(store.events.count)
        }
    }
}
