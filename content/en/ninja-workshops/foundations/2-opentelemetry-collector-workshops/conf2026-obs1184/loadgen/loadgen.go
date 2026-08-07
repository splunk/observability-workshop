package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"
)

// Global flag to ensure the first trace always uses "George Lucas"
var firstAttempt = true

// previewOnly prints the original OTLP/HTTP JSON payload without sending it.
var previewOnly bool

// getRandomUserName selects "George Lucas" for the first trace, then randomizes
func getRandomUserName() string {
	userNames := []string{
		"George Lucas",
		"Darth Vader",
		"Luke Skywalker",
		"Frodo Baggins",
		"Peter Jackson",
		"Thorin Oakenshield",
	}

	if firstAttempt {
		firstAttempt = false // Ensure future calls are random
		return "George Lucas"
	}
	return userNames[rand.Intn(len(userNames)-1)+1] // Skip "George Lucas" after the first attempt
}

// Function to generate a random trace ID
func generateTraceID() string {
	return randomHex(16)
}

// Function to generate a random span ID
func generateSpanID() string {
	return randomHex(8)
}

// GenerateRandomPayment generates a random payment amount between 50 and 100
func generateRandomPayment() float64 {
	rand.Seed(time.Now().UnixNano())
	amount := 50.00 + rand.Float64()*(100.00-50.00) // Random float between 50.00 and 100.00
	return float64(int(amount*100)) / 100           // Round to two decimal places
}

// Helper function to generate a random hex string of a given length
func randomHex(length int) string {
	b := make([]byte, length)
	_, err := rand.Read(b)
	if err != nil {
		log.Fatalf("Failed to generate random bytes: %v", err)
	}
	return hex.EncodeToString(b)
}

// Function to get the current timestamp in nanoseconds
func getCurrentTime() int64 {
	return time.Now().UnixNano()
}

// Function to send a base trace
func sendBaseTrace(traceID, spanID string, startTime, endTime int64) {
	randomUser := getRandomUserName() // Ensure first attempt is "George Lucas", then randomize
	spanJSON := map[string]interface{}{
		"resourceSpans": []interface{}{
			map[string]interface{}{
				"resource": map[string]interface{}{
					"attributes": []interface{}{
						map[string]interface{}{
							"key": "service.name",
							"value": map[string]interface{}{
								"stringValue": "cinema-service",
							},
						},
						map[string]interface{}{
							"key": "deployment.environment",
							"value": map[string]interface{}{
								"stringValue": "production",
							},
						},
					},
				},
				"scopeSpans": []interface{}{
					map[string]interface{}{
						"scope": map[string]interface{}{
							"name":    "cinema.library",
							"version": "1.0.0",
							"attributes": []interface{}{
								map[string]interface{}{
									"key": "fintest.scope.attribute",
									"value": map[string]interface{}{
										"stringValue": "Starwars, LOTR",
									},
								},
							},
						},
						"spans": []interface{}{
							map[string]interface{}{
								"traceId":           traceID,
								"spanId":            spanID,
								"name":              "/movie-validator",
								"startTimeUnixNano": fmt.Sprintf("%d", startTime),
								"endTimeUnixNano":   fmt.Sprintf("%d", endTime),
								"kind":              2,
								"status": map[string]interface{}{
									"code":    1,
									"message": "Success",
								},
								"attributes": []interface{}{
									map[string]interface{}{
										"key": "user.name",
										"value": map[string]interface{}{
											"stringValue": randomUser, // Uses "George Lucas" first, then random
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
										"key": "user.password",
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
									map[string]interface{}{
										"key": "payment.amount",
										"value": map[string]interface{}{
											"doubleValue": generateRandomPayment(),
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

	if err := sendJSON("http://127.0.0.1:4318/v1/traces", spanJSON); err != nil {
		log.Printf("Failed to send base trace: %v", err)
	} else if previewOnly {
		fmt.Println("Base trace preview shown above; nothing was sent.")
	} else {
		fmt.Printf("\nBase trace sent with traceId: %s and spanId: %s\n", traceID, spanID)
	}
}

// Function to send a security trace
func sendSecurityTrace(traceID, spanID string, startTime, endTime int64) {
	securityJSON := map[string]interface{}{
		"resourceSpans": []interface{}{
			map[string]interface{}{
				"resource": map[string]interface{}{
					"attributes": []interface{}{
						map[string]interface{}{
							"key": "service.name",
							"value": map[string]interface{}{
								"stringValue": "password-check",
							},
						},
						map[string]interface{}{
							"key": "deployment.environment",
							"value": map[string]interface{}{
								"stringValue": "security-applications",
							},
						},
					},
				},
				"scopeSpans": []interface{}{
					map[string]interface{}{
						"scope": map[string]interface{}{
							"name":    "movie.library",
							"version": "1.0.0",
						},
						"spans": []interface{}{
							map[string]interface{}{
								"traceId":           traceID,
								"spanId":            spanID,
								"parentSpanId":      generateSpanID(),
								"name":              "password-validation",
								"startTimeUnixNano": fmt.Sprintf("%d", startTime),
								"endTimeUnixNano":   fmt.Sprintf("%d", endTime),
								"kind":              2,
								"status": map[string]interface{}{
									"code":    1,
									"message": "Success",
								},
								"attributes": []interface{}{
									map[string]interface{}{
										"key": "user.name",
										"value": map[string]interface{}{
											"stringValue": "George Lucas",
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

	if err := sendJSON("http://127.0.0.1:4318/v1/traces", securityJSON); err != nil {
		log.Printf("Failed to send security trace: %v", err)
	} else if previewOnly {
		fmt.Println("Security trace preview shown above; nothing was sent.")
	} else {
		fmt.Printf("\nSecurity trace sent with traceId: %s and spanId: %s\n", traceID, spanID)
	}
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
								"stringValue": "production",
							},
						},
					},
				},
				"scopeSpans": []interface{}{
					map[string]interface{}{
						"scope": map[string]interface{}{
							"name":    "healthz",
							"version": "1.0.0",
						},
						"spans": []interface{}{
							map[string]interface{}{
								"traceId":           traceID,
								"spanId":            spanID,
								"name":              "/_healthz",
								"startTimeUnixNano": fmt.Sprintf("%d", startTime),
								"endTimeUnixNano":   fmt.Sprintf("%d", endTime),
								"kind":              2,
								"status": map[string]interface{}{
									"code":    1,
									"message": "Success",
								},
							},
						},
					},
				},
			},
		},
	}

	if err := sendJSON("http://127.0.0.1:4318/v1/traces", healthJSON); err != nil {
		log.Printf("Failed to send health trace: %v", err)
	} else if previewOnly {
		fmt.Println("Health trace preview shown above; nothing was sent.")
	} else {
		fmt.Printf("\nHealth trace sent with traceId: %s and spanId: %s\n", traceID, spanID)
	}
}

// sendCorrelatedLog sends one OTLP log record with the same trace and span IDs
// as a base trace. This makes the optional Splunk Platform and Log Observer
// Connect exercise demonstrably correlated instead of merely colocated.
func sendCorrelatedLog(traceID, spanID string, timestamp int64) {
	quote, movie := getRandomQuote()
	logJSON := map[string]interface{}{
		"resourceLogs": []interface{}{
			map[string]interface{}{
				"resource": map[string]interface{}{
					"attributes": []interface{}{
						map[string]interface{}{
							"key": "service.name",
							"value": map[string]interface{}{
								"stringValue": "cinema-service",
							},
						},
						map[string]interface{}{
							"key": "deployment.environment",
							"value": map[string]interface{}{
								"stringValue": "production",
							},
						},
					},
				},
				"scopeLogs": []interface{}{
					map[string]interface{}{
						"scope": map[string]interface{}{
							"name":    "cinema.library",
							"version": "1.0.0",
						},
						"logRecords": []interface{}{
							map[string]interface{}{
								"timeUnixNano":   fmt.Sprintf("%d", timestamp),
								"severityNumber": 9,
								"severityText":   "INFO",
								"body": map[string]interface{}{
									"stringValue": quote,
								},
								"attributes": []interface{}{
									map[string]interface{}{
										"key": "movie",
										"value": map[string]interface{}{
											"stringValue": movie,
										},
									},
									map[string]interface{}{
										"key": "workshop.signal",
										"value": map[string]interface{}{
											"stringValue": "correlated-log",
										},
									},
								},
								"traceId": traceID,
								"spanId":  spanID,
								"flags":   1,
							},
						},
					},
				},
			},
		},
	}

	if err := sendJSON("http://127.0.0.1:4318/v1/logs", logJSON); err != nil {
		log.Printf("Failed to send correlated log: %v", err)
	} else if previewOnly {
		fmt.Println("Correlated log preview shown above; nothing was sent.")
	} else {
		fmt.Printf("Correlated log sent with traceId: %s and spanId: %s\n", traceID, spanID)
	}
}

// Helper function to send JSON data via HTTP POST
func sendJSON(url string, data interface{}) error {
	if previewOnly {
		var formatted bytes.Buffer
		encoder := json.NewEncoder(&formatted)
		encoder.SetIndent("", "  ")
		encoder.SetEscapeHTML(false)
		if err := encoder.Encode(data); err != nil {
			return fmt.Errorf("failed to format JSON preview: %w", err)
		}
		fmt.Printf("\nOriginal OTLP payload for %s:\n%s", url, formatted.String())
		return nil
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("failed to marshal JSON data: %w", err)
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("HTTP POST request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("received non-2xx HTTP status code: %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read response body: %w", err)
	}
	fmt.Println("Response:", string(body))

	return nil
}

// Function to generate a random quote
func getRandomQuote() (string, string) {
	lotrQuotes := []string{
		"One does not simply walk into Mordor.",
		"Even the smallest person can change the course of the future.",
		"All we have to decide is what to do with the time that is given us.",
		"There is some good in this world, and it's worth fighting for.",
		"Not all those who wander are lost.",
		"There's some good in this world, Mr. Frodo … and it's worth fighting for.",
		"I wish the Ring had never come to me. I wish none of this had happened.",
	}

	starWarsQuotes := []string{
		"Do or do not, there is no try.",
		"The Force will be with you. Always.",
		"I find your lack of faith disturbing.",
		"In my experience, there is no such thing as luck.",
		"Help me, Obi-Wan Kenobi. You're my only hope.",
		"May the Force be with you.",
		"Your focus determines your reality.",
	}

	if rand.Intn(100) < 66 {
		return lotrQuotes[rand.Intn(len(lotrQuotes))], "LOTR"
	}
	return starWarsQuotes[rand.Intn(len(starWarsQuotes))], "SW"
}

// Function to generate a random log level
func getRandomLogLevel() string {
	logLevels := []string{"INFO", "WARN", "ERROR", "DEBUG"}
	return logLevels[rand.Intn(len(logLevels))]
}

// Function to generate a log entry
func generateLogEntry(jsonOutput bool) string {
	timestamp := time.Now().Format("2006-01-02 15:04:05")
	level := getRandomLogLevel()
	quote, movie := getRandomQuote()

	if jsonOutput {
		logEntry := map[string]string{
			"timestamp": timestamp,
			"level":     level,
			"message":   quote,
			"movie":     movie,
		}
		jsonData, _ := json.Marshal(logEntry)
		return string(jsonData)
	}
	return fmt.Sprintf("%s [%s] - %s %s", timestamp, level, quote, movie)
}

// Function to write logs to a file
func writeLogs(jsonOutput bool, count int) {
	logFile := "quotes.log"
	if count == 0 {
		fmt.Printf("Writing logs to %s. Press Ctrl+C to stop.\n", logFile)
	} else {
		fmt.Printf("Writing %d logs to %s.\n", count, logFile)
	}

	// If count is 0, run infinitely
	if count == 0 {
		for {
			logEntry := generateLogEntry(jsonOutput)
			file, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
			if err != nil {
				log.Fatalf("Failed to open log file: %v", err)
			}
			file.WriteString(logEntry + "\n")
			file.Close()
			time.Sleep(100 * time.Millisecond)
		}
	} else {
		// Otherwise, run for the specified count
		for i := 0; i < count; i++ {
			logEntry := generateLogEntry(jsonOutput)
			file, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
			if err != nil {
				log.Fatalf("Failed to open log file: %v", err)
			}
			file.WriteString(logEntry + "\n")
			file.Close()
			time.Sleep(100 * time.Millisecond)
		}
	}
}

// Display usage instructions
func printHelp() {
	fmt.Println(`Usage: loadgen [OPTIONS]
Options:
  -base       Send base traces (enabled by default)
  -health     Send health traces
  -security   Send security traces
  -logs       Enable logging of random quotes to quotes.log
  -json       Output logs in JSON format (only applicable with -logs)
  -correlated Send an OTLP log correlated to each base trace
  -preview    Print original OTLP JSON payloads without sending them
  -count      Number of traces or logs to send (default: infinite)
  -h, --help  Display this help message

Example:
  loadgen -health -security -count 10   Send 10 health and security traces
  loadgen -preview -health -count 1     Show one original app span and health span without sending
  loadgen -preview -count 1             Show one original app span without sending
  loadgen -logs -json -count 5          Write 5 random quotes in JSON format to quotes.log
  loadgen -correlated -count 5          Send 5 traces with correlated OTLP logs`)
}

func main() {
	// Define flags
	baseFlag := flag.Bool("base", true, "Send base traces")
	healthFlag := flag.Bool("health", false, "Send health traces")
	securityFlag := flag.Bool("security", false, "Send security traces")
	logsFlag := flag.Bool("logs", false, "Enable logging of random quotes to quotes.log")
	jsonFlag := flag.Bool("json", false, "Output logs in JSON format (only applicable with -logs)")
	correlatedFlag := flag.Bool("correlated", false, "Send an OTLP log correlated to each base trace")
	previewFlag := flag.Bool("preview", false, "Print original OTLP JSON payloads without sending them")
	countFlag := flag.Int("count", 0, "Number of traces or logs to send (default: infinite)")
	helpFlag := flag.Bool("h", false, "Display help message")
	helpFlagLong := flag.Bool("help", false, "Display help message")

	flag.Parse()

	// Display help and exit if -h or --help is provided
	if *helpFlag || *helpFlagLong {
		printHelp()
		os.Exit(0)
	}

	previewOnly = *previewFlag

	// File-only log generation does not need the trace loop. Run it directly so
	// a finite -count exits as soon as the requested lines have been written.
	if *logsFlag && !*correlatedFlag {
		writeLogs(*jsonFlag, *countFlag)
		return
	}
	if *logsFlag {
		go writeLogs(*jsonFlag, *countFlag)
	}

	if previewOnly {
		fmt.Println("Preview mode: original OTLP payloads are printed but not sent.")
	} else {
		fmt.Println("Sending traces. Use Ctrl-C to stop.")
	}

	for i := 0; *countFlag == 0 || i < *countFlag; i++ {
		traceID := generateTraceID()
		spanID := generateSpanID()
		currentTime := getCurrentTime()
		endTime := currentTime + int64(time.Second)

		if *baseFlag && (!*logsFlag || *correlatedFlag) {
			sendBaseTrace(traceID, spanID, currentTime, endTime)
		}

		if *correlatedFlag {
			sendCorrelatedLog(traceID, spanID, getCurrentTime())
		}

		if *healthFlag {
			if !previewOnly {
				time.Sleep(2 * time.Second)
			}
			sendHealthTrace(traceID, generateSpanID(), getCurrentTime(), getCurrentTime()+int64(time.Second))
		}

		if *securityFlag {
			if !previewOnly {
				time.Sleep(2 * time.Second)
			}
			sendSecurityTrace(traceID, generateSpanID(), getCurrentTime(), getCurrentTime()+int64(time.Second))
		}

		if !previewOnly {
			time.Sleep(2 * time.Second)
		}
	}
}
