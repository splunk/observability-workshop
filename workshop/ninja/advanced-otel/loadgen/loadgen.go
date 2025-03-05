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

	if err := sendJSON("http://localhost:4318/v1/traces", spanJSON); err != nil {
		log.Printf("Failed to send base trace: %v", err)
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

	if err := sendJSON("http://localhost:4318/v1/traces", securityJSON); err != nil {
		log.Printf("Failed to send security trace: %v", err)
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

	if err := sendJSON("http://localhost:4318/v1/traces", healthJSON); err != nil {
		log.Printf("Failed to send health trace: %v", err)
	} else {
		fmt.Printf("\nHealth trace sent with traceId: %s and spanId: %s\n", traceID, spanID)
	}
}

// Helper function to send JSON data via HTTP POST
func sendJSON(url string, data interface{}) error {
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
func writeLogs(jsonOutput bool) {
	logFile := "quotes.log"
	fmt.Printf("Writing logs to %s. Press Ctrl+C to stop.\n", logFile)

	for {
		logEntry := generateLogEntry(jsonOutput)
		file, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatalf("Failed to open log file: %v", err)
		}
		file.WriteString(logEntry + "\n")
		file.Close()
		time.Sleep(1 * time.Second)
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
  -h, --help  Display this help message

Example:
  loadgen -health -security   Send health and security traces
  loadgen -logs -json         Write random quotes in JSON format to quotes.log`)
}

func main() {
	// Define flags
	baseFlag := flag.Bool("base", true, "Send base traces")
	healthFlag := flag.Bool("health", false, "Send health traces")
	securityFlag := flag.Bool("security", false, "Send security traces")
	logsFlag := flag.Bool("logs", false, "Enable logging of random quotes to quotes.log")
	jsonFlag := flag.Bool("json", false, "Output logs in JSON format (only applicable with -logs)")
	helpFlag := flag.Bool("h", false, "Display help message")
	helpFlagLong := flag.Bool("help", false, "Display help message")

	flag.Parse()

	// Display help and exit if -h or --help is provided
	if *helpFlag || *helpFlagLong {
		printHelp()
		os.Exit(0)
	}

	// Start logging if -logs flag is provided
	if *logsFlag {
		go writeLogs(*jsonFlag) // Run logs in a separate goroutine
	}

	fmt.Println("Sending traces every 5 seconds. Use Ctrl-C to stop.")

	for {
		traceID := generateTraceID()
		spanID := generateSpanID()
		currentTime := getCurrentTime()
		endTime := currentTime + int64(time.Second)

		if *baseFlag {
			sendBaseTrace(traceID, spanID, currentTime, endTime)
		}

		if *healthFlag {
			time.Sleep(5 * time.Second)
			sendHealthTrace(traceID, generateSpanID(), getCurrentTime(), getCurrentTime()+int64(time.Second))
		}

		if *securityFlag {
			time.Sleep(5 * time.Second)
			sendSecurityTrace(traceID, generateSpanID(), getCurrentTime(), getCurrentTime()+int64(time.Second))
		}

		time.Sleep(5 * time.Second)
	}
}
