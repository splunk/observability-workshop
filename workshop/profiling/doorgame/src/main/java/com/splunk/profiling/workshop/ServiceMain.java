package com.splunk.profiling.workshop;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class ServiceMain {

    @Bean
    public DoorGame doorGame() {
        return new DoorGame();
    }

    public static void main(String[] args) {
        BackgroundWorker.start();
        SpringApplication.run(ServiceMain.class, args);
    }
}
