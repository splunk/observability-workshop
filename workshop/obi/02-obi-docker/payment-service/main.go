package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

func newTxID() string {
	b := make([]byte, 8)
	rand.Read(b)
	return fmt.Sprintf("txn-%x", b)
}

func main() {
	http.HandleFunc("/process-payment", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":         "success",
			"transaction_id": newTxID(),
			"amount":         42.00,
		})
	})

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})

	log.Println("payment-service listening on :8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
