import Foundation

@MainActor
final class TrainingRumInstrumentation {
    struct Workflow: Hashable {
        let id = UUID()
        let name: String
        let startedAt: Date
    }

    var onEvent: ((TelemetryEvent) -> Void)?

    func start(configuration: RumConfiguration) {
        record(.bootstrap, "RUM Bootstrap", attributes: [
            "realm": configuration.realm,
            "application.name": configuration.applicationName,
            "deployment.environment": configuration.deploymentEnvironment,
            "app.version": configuration.appVersion,
            "rum.token": configuration.rumAccessToken == "training-mode" ? "training-mode" : "configured"
        ])
    }

    func enableAnonymousTracking() {
        record(.bootstrap, "Anonymous Tracking Enabled", attributes: [
            "user.tracking_mode": "anonymousTracking"
        ])
    }

    func startSessionReplay() {
        record(.privacy, "Session Replay Started", attributes: [
            "replay.mode": "training",
            "masking.default": "sensitive fields hidden"
        ])
    }

    func screenViewed(_ name: String, attributes: [String: String]) {
        var combined = attributes
        combined["screen.name"] = name
        record(.screen, name, attributes: combined)
    }

    func customEvent(_ name: String, attributes: [String: String]) {
        record(.interaction, name, attributes: attributes)
    }

    func startWorkflow(_ name: String, attributes: [String: String]) -> Workflow {
        record(.workflow, "\(name) Started", attributes: attributes)
        return Workflow(name: name, startedAt: Date())
    }

    func finishWorkflow(
        _ workflow: Workflow,
        result: String,
        attributes: [String: String]
    ) {
        var combined = attributes
        combined["result"] = result
        combined["duration.ms"] = "\(Int(Date().timeIntervalSince(workflow.startedAt) * 1000))"
        record(.workflow, "\(workflow.name) Finished", attributes: combined)
    }

    func networkRequest(_ name: String, attributes: [String: String]) {
        record(.network, name, attributes: attributes)
    }

    func markSensitiveView(_ name: String) {
        record(.privacy, "Sensitive View Marked", attributes: [
            "view.name": name,
            "session_replay.sensitive": "true"
        ])
    }

    private func record(
        _ kind: TelemetryKind,
        _ name: String,
        attributes: [String: String]
    ) {
        onEvent?(
            TelemetryEvent(
                timestamp: Date(),
                kind: kind,
                name: name,
                attributes: attributes
            )
        )
    }
}
