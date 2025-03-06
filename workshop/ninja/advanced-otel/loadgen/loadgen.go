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

// Generate a random trace ID
func generateTraceID() string {
	return randomHex(16)
}

// Generate a random span ID
func generateSpanID() string {
	return randomHex(8)
}

// Generate a random payment amount between 50 and 100
func generateRandomPayment() float64 {
	rand.Seed(time.Now().UnixNano())
	amount := 50.00 + rand.Float64()*(100.00-50.00) // Random float between 50.00 and 100.00
	return float64(int(amount*100)) / 100           // Round to two decimal places
}

// Generate a random hex string
func randomHex(length int) string {
	b := make([]byte, length)
	_, err := rand.Read(b)
	if err != nil {
		log.Fatalf("Failed to generate random bytes: %v", err)
	}
	return hex.EncodeToString(b)
}

// Get current timestamp in nanoseconds
func getCurrentTime() int64 {
	return time.Now().UnixNano()
}

// Send a base trace
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
		fmt.Printf("\nBase trace sent with traceId: %s, spanId: %s, user: %s\n", traceID, spanID, randomUser)
	}
}

// Send JSON data via HTTP POST
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

func main() {
	// Define flags
	baseFlag := flag.Bool("base", true, "Send base traces")
	countFlag := flag.Int("count", 0, "Number of traces to send (default: infinite)")
	helpFlag := flag.Bool("h", false, "Display help message")
	helpFlagLong := flag.Bool("help", false, "Display help message")

	flag.Parse()

	// Display help and exit if -h or --help is provided
	if *helpFlag || *helpFlagLong {
		fmt.Println("Usage: loadgen [OPTIONS]\n" +
			"Options:\n" +
			"  -base       Send base traces (enabled by default)\n" +
			"  -count      Number of traces to send (default: infinite)\n" +
			"  -h, --help  Display this help message")
		os.Exit(0)
	}

	fmt.Println("Sending traces. Use Ctrl-C to stop.")

	for i := 0; *countFlag == 0 || i < *countFlag; i++ {
		traceID := generateTraceID()
		spanID := generateSpanID()
		currentTime := getCurrentTime()
		endTime := currentTime + int64(time.Second)

		if *baseFlag {
			sendBaseTrace(traceID, spanID, currentTime, endTime)
		}

		time.Sleep(2 * time.Second)
	}
}
