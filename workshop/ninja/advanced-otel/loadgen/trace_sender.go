package main

import (
	"bytes"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// Function to generate a random trace ID
func generateTraceID() string {
	return randomHex(16)
}

// Function to generate a random span ID
func generateSpanID() string {
	return randomHex(8)
}

// Helper function to generate a random hex string of a given length
func randomHex(length int) string {
	b := make([]byte, length)
	_, err := rand.Read(b)
	if err != nil {
		panic(err)
	}
	return hex.EncodeToString(b)
}

// Function to get the current timestamp in nanoseconds
func getCurrentTime() int64 {
	return time.Now().UnixNano()
}

// Function to send a trace
func sendTrace(traceID, spanID string, startTime, endTime int64) {
	spanJSON := map[string]interface{}{
		"resourceSpans": []interface{}{
			map[string]interface{}{
				"resource": map[string]interface{}{
					"attributes": []interface{}{
						map[string]interface{}{
							"key": "service.name",
							"value": map[string]interface{}{
								"stringValue": "Validation-service",
							},
						},
						map[string]interface{}{
							"key": "deployment.environment",
							"value": map[string]interface{}{
								"stringValue": "Advanced-Otel",
							},
						},
					},
				},
				"scopeSpans": []interface{}{
					map[string]interface{}{
						"scope": map[string]interface{}{
							"name":    "fintest.library",
							"version": "1.0.0",
							"attributes": []interface{}{
								map[string]interface{}{
									"key": "fintest.scope.attribute",
									"value": map[string]interface{}{
										"stringValue": "Euro, Dollar, Yen",
									},
								},
							},
						},
						"spans": []interface{}{
							map[string]interface{}{
								"traceId":           traceID,
								"spanId":            spanID,
								"name":              "/Login Validator",
								"startTimeUnixNano": fmt.Sprintf("%d", startTime),
								"endTimeUnixNano":   fmt.Sprintf("%d", endTime),
								"kind":             2,
								"attributes": []interface{}{
									map[string]interface{}{
										"key": "user.name",
										"value": map[string]interface{}{
											"stringValue": "George Lucas",
										},
									},
									map[string]interface{}{
										"key": "user.phone_number",
										"value": map[string]interface{}{
											"stringValue": "+1555-867-5309",
										},
									},
									map[string]interface{}{
										"key": "user.email",
										"value": map[string]interface{}{
											"stringValue": "george@deathstar.email",
										},
									},
									map[string]interface{}{
										"key": "user.account_password",
										"value": map[string]interface{}{
											"stringValue": "LOTR>StarWars1-2-3",
										},
									},
									map[string]interface{}{
										"key": "user.visa",
										"value": map[string]interface{}{
											"stringValue": "4111 1111 1111 1111",
										},
									},
									map[string]interface{}{
										"key": "user.amex",
										"value": map[string]interface{}{
											"stringValue": "3782 822463 10005",
										},
									},
									map[string]interface{}{
										"key": "user.mastercard",
										"value": map[string]interface{}{
											"stringValue": "5555 5555 5555 4444",
										},
									},
								},
							},
						},
					},
				},
			},
		},
	}

	sendJSON("http://localhost:4318/v1/traces", spanJSON)
	fmt.Printf("\nBase trace sent with traceId: %s and spanId: %s\n", traceID, spanID)
}

// Function to send a health trace
func sendHealthTrace(traceID, spanID string, startTime, endTime int64) {
	healthJSON := map[string]interface{}{
		"resourceSpans": []interface{}{
			map[string]interface{}{
				"resource": map[string]interface{}{
					"attributes": []interface{}{
						map[string]interface{}{
							"key": "service.name",
							"value": map[string]interface{}{
								"stringValue": "frontend-service",
							},
						},
						map[string]interface{}{
							"key": "deployment.environment",
							"value": map[string]interface{}{
								"stringValue": "Advanced-Otel",
							},
						},
					},
				},
				"scopeSpans": []interface{}{
					map[string]interface{}{
						"scope": map[string]interface{}{
							"name":    "healthz",
							"version": "1.0.0",
							"attributes": []interface{}{
								map[string]interface{}{
									"key": "healthz.scope.attribute",
									"value": map[string]interface{}{
										"stringValue": "Health check",
									},
								},
							},
						},
						"spans": []interface{}{
							map[string]interface{}{
								"traceId":           traceID,
								"spanId":            spanID,
								"name":              "/_healthz",
								"startTimeUnixNano": fmt.Sprintf("%d", startTime),
								"endTimeUnixNano":   fmt.Sprintf("%d", endTime),
								"kind":             2,
								"attributes": []interface{}{
									map[string]interface{}{
										"key": "health.status",
										"value": map[string]interface{}{
											"stringValue": "pass",
										},
									},
								},
							},
						},
					},
				},
			},
		},
	}

	sendJSON("http://localhost:4318/v1/traces", healthJSON)
	fmt.Printf("\nHealth trace sent with traceId: %s and spanId: %s\n", traceID, spanID)
}

// Helper function to send JSON data via HTTP POST
func sendJSON(url string, data interface{}) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	fmt.Println("Response:", string(body))
}

// Display usage instructions
func printHelp() {
	fmt.Println(`Usage: trace_sender [OPTIONS]
Options:
  -h, --help    Display this help message
  -health       Send health traces in addition to base traces

Example:
  trace_sender -health    Send both base and health traces every 20 seconds
  trace_sender            Send only base traces every 20 seconds`)
}

func main() {
	// Define flags
	helpFlag := flag.Bool("h", false, "Display help message")
	helpFlagLong := flag.Bool("help", false, "Display help message")
	healthFlag := flag.Bool("health", false, "Send health traces in addition to base traces")

	flag.Parse()

	// Display help and exit if -h or --help is provided
	if *helpFlag || *helpFlagLong {
		printHelp()
		os.Exit(0)
	}

	fmt.Println("Sending traces every 20 seconds. Use Ctrl-C to stop.")

	for {
		// Generate trace and span IDs for base span
		traceID := generateTraceID()
		spanID := generateSpanID()
		currentTime := getCurrentTime()
		endTime := currentTime + int64(time.Second)

		// Send base trace
		sendTrace(traceID, spanID, currentTime, endTime)

		if *healthFlag {
			time.Sleep(10 * time.Second) // Wait 10 seconds before sending health span

			// Generate trace and span IDs for health span
			healthTraceID := generateTraceID()
			healthSpanID := generateSpanID()
			healthStartTime := getCurrentTime()
			healthEndTime := healthStartTime + int64(time.Second)

			// Send health trace
			sendHealthTrace(healthTraceID, healthSpanID, healthStartTime, healthEndTime)
		}

		time.Sleep(10 * time.Second) // Wait remaining 10 seconds before repeating
	}
}
