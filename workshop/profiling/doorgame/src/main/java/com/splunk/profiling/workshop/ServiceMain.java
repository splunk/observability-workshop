package com.splunk.profiling.workshop;

import static com.splunk.profiling.workshop.Util.sleep;
import static java.lang.Integer.parseInt;
import static spark.Spark.get;
import static spark.Spark.port;
import static spark.Spark.post;
import static spark.Spark.staticFiles;

public class ServiceMain {

    private final static DoorGame doorGame = new DoorGame();

    public static void main(String[] args) {
        BackgroundWorker.start();
        port(9090);
        staticFiles.location("/public"); // Static files

        get("/new-game", (req, res) -> doorGame.startNew());
        post("/game/:uid/pick/:picked", (req, res) -> {
            sleep(600);
            String uid = req.params(":uid");
            String picked = req.params(":picked");
            doorGame.pick(uid, parseInt(picked));
            return "OK";
        });
        get("/game/:uid/reveal", (req, res) -> {
            String uid = req.params(":uid");
            return doorGame.reveal(uid);
        });
        get("/game/:uid/picked/:picked/outcome", (req,res) -> {
            String uid = req.params(":uid");
            String picked = req.params(":picked");
            return doorGame.getOutcome(uid, parseInt(picked));
        });
    }
}
