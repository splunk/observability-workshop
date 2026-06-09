import Foundation
import SplunkAgent

enum PrivacySpanInterceptor {
    static let redact: (SpanData) -> SpanData? = { spanData in
        var attributes = spanData.attributes

        attributes["http.url"] = .string("redacted")
        attributes["url.full"] = .string("redacted")

        return spanData.settingAttributes(attributes)
    }
}
