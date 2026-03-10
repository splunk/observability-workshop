package com.splunk.workshop;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;

@RestController
@RequestMapping("/inventory")
public class InventoryController {

    @GetMapping("/check")
    public Map<String, Object> checkInventory() {
        simulateWork(10, 50);
        return Map.of(
            "available", ThreadLocalRandom.current().nextInt(1, 100),
            "warehouse", "us-west-2",
            "lastUpdated", System.currentTimeMillis()
        );
    }

    private void simulateWork(int minMs, int maxMs) {
        try {
            Thread.sleep(ThreadLocalRandom.current().nextInt(minMs, maxMs));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
