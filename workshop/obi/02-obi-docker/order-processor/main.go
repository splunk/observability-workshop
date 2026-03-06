package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	paymentURL := os.Getenv("PAYMENT_SERVICE_URL")
	if paymentURL == "" {
		paymentURL = "http://payment-service:8081"
	}

	http.HandleFunc("/process-order", func(w http.ResponseWriter, r *http.Request) {
		resp, err := http.Get(paymentURL + "/process-payment")
		if err != nil {
			w.WriteHeader(http.StatusServiceUnavailable)
			json.NewEncoder(w).Encode(map[string]string{
				"error": fmt.Sprintf("payment-service unreachable: %v", err),
			})
			return
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			w.WriteHeader(http.StatusBadGateway)
			json.NewEncoder(w).Encode(map[string]string{"error": "failed to read payment response"})
			return
		}

		var payment map[string]interface{}
		if err := json.Unmarshal(body, &payment); err != nil {
			w.WriteHeader(http.StatusBadGateway)
			json.NewEncoder(w).Encode(map[string]string{"error": "invalid payment response"})
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"order":   "confirmed",
			"payment": payment,
		})
	})

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})

	log.Println("order-processor listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
