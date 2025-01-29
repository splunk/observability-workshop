using System.IO;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Console;
using Microsoft.Extensions.Logging.Abstractions;

namespace SplunkTelemetry
{
   public static class SplunkTelemetryConfigurator
   {
       public static void ConfigureLogger(ILoggingBuilder logging)
       {
           logging.AddSimpleConsole(options =>
           {
               options.IncludeScopes = true;
           });

            logging.Configure(options =>
            {
                options.ActivityTrackingOptions = ActivityTrackingOptions.SpanId
                                                   | ActivityTrackingOptions.TraceId
                                                   | ActivityTrackingOptions.ParentId
                                                   | ActivityTrackingOptions.Baggage
                                                   | ActivityTrackingOptions.Tags;
            }).AddConsole(options =>
            {
               options.FormatterName = "splunkLogsJson";
            });

            logging.AddConsoleFormatter<SplunkTelemetryConsoleFormatter, ConsoleFormatterOptions>();
       }
   }

   public class SplunkTelemetryConsoleFormatter : ConsoleFormatter
   {
       public SplunkTelemetryConsoleFormatter() : base("splunkLogsJson") { }

       public override void Write<TState>(in LogEntry<TState> logEntry, IExternalScopeProvider? scopeProvider, TextWriter textWriter)
       {
           var serviceName = Environment.GetEnvironmentVariable("OTEL_SERVICE_NAME") ?? "Unknown";
           var severity = logEntry.LogLevel switch
           {
               Microsoft.Extensions.Logging.LogLevel.Trace => "DEBUG",
               Microsoft.Extensions.Logging.LogLevel.Debug => "DEBUG",
               Microsoft.Extensions.Logging.LogLevel.Information => "INFO",
               Microsoft.Extensions.Logging.LogLevel.Warning => "WARN",
               Microsoft.Extensions.Logging.LogLevel.Error => "ERROR",
               Microsoft.Extensions.Logging.LogLevel.Critical => "FATAL",
               Microsoft.Extensions.Logging.LogLevel.None => "NONE",
               _ => "INFO"
           };
           var logObject = new Dictionary<string, object>
           {
               { "event_id", logEntry.EventId.Id },
               { "log_level", logEntry.LogLevel.ToString().ToLower() },
               { "category", logEntry.Category },
               { "message", logEntry.Formatter(logEntry.State, logEntry.Exception) },
               { "timestamp", DateTime.UtcNow.ToString("o") },
               { "service.name", serviceName },
               { "severity", severity }
           };
           // Add exception if present
           if (logEntry.Exception != null)
           {
               logObject["exception"] = logEntry.Exception.ToString();
           }
           // Include scopes if enabled
           if (scopeProvider != null)
           {
               scopeProvider.ForEachScope((scope, state) =>
               {
                   if (scope is IReadOnlyList<KeyValuePair<string, object>> scopeItems)
                   {
                       foreach (var kvp in scopeItems)
                       {
                           if (kvp.Key.Equals("SpanId", StringComparison.OrdinalIgnoreCase))
                               logObject["span_id"] = kvp.Value;
                           else if (kvp.Key.Equals("TraceId", StringComparison.OrdinalIgnoreCase))
                               logObject["trace_id"] = kvp.Value;
                           else if (kvp.Key.Equals("ParentId", StringComparison.OrdinalIgnoreCase))
                               logObject["parent_id"] = kvp.Value;
                           else
                               logObject[kvp.Key] = kvp.Value;
                       }
                   }
                   else if (scope is IEnumerable<KeyValuePair<string, string>> baggage)
                   {
                       foreach (var kvp in baggage)
                       {
                           logObject[$"baggage_{kvp.Key}"] = kvp.Value;
                       }
                   }
                   else if (scope is IEnumerable<KeyValuePair<string, object>> tags)
                   {
                       foreach (var kvp in tags)
                       {
                           logObject[$"tag_{kvp.Key}"] = kvp.Value;
                       }
                   }
               }, logObject);
           }

           var logJson = JsonSerializer.Serialize(logObject);
           textWriter.WriteLine(logJson);
       }
   }
}