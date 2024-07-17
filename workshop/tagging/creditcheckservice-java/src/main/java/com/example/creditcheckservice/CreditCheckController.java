package com.example.creditcheckservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Tracer;
// import io.opentelemetry.api.trace.SpanKind;
// import io.opentelemetry.api.trace.Span;
// import io.opentelemetry.instrumentation.annotations.WithSpan;
// import io.opentelemetry.instrumentation.annotations.SpanAttribute;

@RestController
public class CreditCheckController {

    private final Tracer tracer;

    private static final String CATEGORY_IMPOSSIBLE = "impossible";

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    CreditCheckController(OpenTelemetry openTelemetry) {
        tracer = openTelemetry.getTracer(CreditCheckApplication.class.getName());
    }

    @GetMapping("/")
    public String hello() {
        return "Hello";
    }

    @GetMapping("/test")
    public String testIt() {
        return "OK";
    }

    @GetMapping("/check")
    // @WithSpan(kind=SpanKind.SERVER)
    public ResponseEntity<String> creditCheck(@RequestParam("customernum") String customerNum) {
        // Get Credit Score
        int creditScore;
        try {
            String creditScoreUrl = "http://creditprocessorservice:8899/getScore?customernum=" + customerNum;
            creditScore = Integer.parseInt(restTemplate.getForObject(creditScoreUrl, String.class));
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error getting credit score");
        }
        // Span currentSpan = Span.current();
        // currentSpan.setAttribute("credit.score", creditScore);

        String creditScoreCategory = getCreditCategoryFromScore(creditScore);
        // currentSpan.setAttribute("credit.score.category", creditScoreCategory);

        // Run Credit Check
        String creditCheckUrl = "http://creditprocessorservice:8899/runCreditCheck?customernum=" + customerNum + "&score=" + creditScore;
        String checkResult;
        try {
            checkResult = restTemplate.getForObject(creditCheckUrl, String.class);
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error running credit check");
        }
        // currentSpan.setAttribute("credit.check.result", checkResult);

        return ResponseEntity.ok(checkResult);
    }

    private String getCreditCategoryFromScore(int score) {
        if (score > 850) {
            return CATEGORY_IMPOSSIBLE;
        } else if (score >= 800 && score <= 850) {
            return "exceptional";
        } else if (score >= 740 && score < 800) {
            return "very good";
        } else if (score >= 670 && score < 740) {
            return "good";
        } else if (score >= 580 && score < 670) {
            return "fair";
        } else if (score >= 300 && score < 580) {
            return "poor";
        } else {
            return CATEGORY_IMPOSSIBLE;
        }
    }

}


