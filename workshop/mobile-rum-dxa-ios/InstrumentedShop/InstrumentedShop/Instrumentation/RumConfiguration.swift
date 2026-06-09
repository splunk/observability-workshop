import Foundation

struct RumConfiguration: Hashable {
    let realm: String
    let rumAccessToken: String
    let applicationName: String
    let deploymentEnvironment: String
    let appVersion: String
}
