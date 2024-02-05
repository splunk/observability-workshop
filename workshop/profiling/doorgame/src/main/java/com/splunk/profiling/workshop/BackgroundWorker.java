package com.splunk.profiling.workshop;


import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static com.splunk.profiling.workshop.Util.sleep;

/**
 * This class simply serves as a long-running background process
 * that will show a deep stack in the flamegraph.
 */
public class BackgroundWorker implements Runnable {

    static ExecutorService exec = Executors.newSingleThreadExecutor();

    static void start(){
        exec.submit(new BackgroundWorker());
    }

    @Override
    public void run() {
        while(true){
            work(25);
        }
    }

    void work(int depth){
        if(depth == 0){
            sleep(333);
            return;
        }
        sleep(25);
        work(depth-1);
        sleep(25);
    }
}
