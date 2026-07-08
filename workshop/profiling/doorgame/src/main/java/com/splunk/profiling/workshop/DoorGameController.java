package com.splunk.profiling.workshop;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import static com.splunk.profiling.workshop.Util.sleep;

@RestController
public class DoorGameController {

    private final DoorGame doorGame;

    public DoorGameController(DoorGame doorGame) {
        this.doorGame = doorGame;
    }

    @GetMapping("/test")
    public String test() {
        return "OK";
    }

    @GetMapping("/new-game")
    public String newGame() {
        return doorGame.startNew();
    }

    @PostMapping("/game/{uid}/pick/{picked}")
    public String pick(@PathVariable String uid, @PathVariable int picked) {
        sleep(600);
        doorGame.pick(uid, picked);
        return "OK";
    }

    @GetMapping("/game/{uid}/reveal")
    public String reveal(@PathVariable String uid) {
        return String.valueOf(doorGame.reveal(uid));
    }

    @GetMapping("/game/{uid}/picked/{picked}/outcome")
    public String outcome(@PathVariable String uid, @PathVariable int picked) {
        return doorGame.getOutcome(uid, picked);
    }
}
