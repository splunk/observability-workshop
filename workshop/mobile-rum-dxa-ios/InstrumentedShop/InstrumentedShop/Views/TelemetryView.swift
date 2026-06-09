import SwiftUI

struct TelemetryView: View {
    @EnvironmentObject private var store: WorkshopStore

    var body: some View {
        NavigationStack {
            List {
                if store.events.isEmpty {
                    ContentUnavailableView(
                        "No telemetry yet",
                        systemImage: "waveform.path.ecg",
                        description: Text("Events appear here as you use the app.")
                    )
                } else {
                    ForEach(store.events) { event in
                        TelemetryEventRow(event: event)
                    }
                }
            }
            .navigationTitle("Telemetry")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        store.clearTelemetry()
                    } label: {
                        Label("Clear", systemImage: "trash")
                    }
                    .disabled(store.events.isEmpty)
                }
            }
        }
    }
}

private struct TelemetryEventRow: View {
    let event: TelemetryEvent

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Label(event.kind.rawValue, systemImage: iconName)
                    .font(.caption.weight(.bold))
                    .foregroundStyle(color)
                Spacer()
                Text(event.timestamp.formatted(date: .omitted, time: .standard))
                    .font(.caption.monospacedDigit())
                    .foregroundStyle(.secondary)
            }

            Text(event.name)
                .font(.headline)

            if !event.attributes.isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(event.attributes.sorted(by: { $0.key < $1.key }), id: \.key) { key, value in
                        HStack(alignment: .firstTextBaseline) {
                            Text(key)
                                .font(.caption.monospaced())
                                .foregroundStyle(.secondary)
                            Spacer(minLength: 12)
                            Text(value)
                                .font(.caption.monospaced())
                                .multilineTextAlignment(.trailing)
                        }
                    }
                }
                .padding(10)
                .background(.quaternary.opacity(0.6))
                .clipShape(RoundedRectangle(cornerRadius: 8))
            }
        }
        .padding(.vertical, 6)
    }

    private var iconName: String {
        switch event.kind {
        case .bootstrap:
            "power"
        case .screen:
            "iphone"
        case .interaction:
            "hand.tap"
        case .workflow:
            "arrow.triangle.branch"
        case .network:
            "network"
        case .privacy:
            "lock.shield"
        case .error:
            "exclamationmark.triangle"
        }
    }

    private var color: Color {
        switch event.kind {
        case .bootstrap:
            .blue
        case .screen:
            .purple
        case .interaction:
            .pink
        case .workflow:
            .orange
        case .network:
            .teal
        case .privacy:
            .green
        case .error:
            .red
        }
    }
}
