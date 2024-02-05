package com.splunk.profiling.workshop;

import java.util.concurrent.TimeUnit;

public class Util {

    static void sleep(long ms){
        try {
            TimeUnit.MILLISECONDS.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Interrupted while sleeping", e);
        }
    }
}
