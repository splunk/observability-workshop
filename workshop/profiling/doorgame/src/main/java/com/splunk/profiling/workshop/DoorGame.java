package com.splunk.profiling.workshop;

import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.extension.annotations.WithSpan;

import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class DoorGame {

    private final DoorChecker gameOfficial = new DoorChecker();
    private final Map<String, GameInfo> games = new ConcurrentHashMap<>();

    @WithSpan(kind = SpanKind.INTERNAL)
    public String startNew() {
        String uuid = UUID.randomUUID().toString();
        Random random = new Random();
        int winningDoor = random.nextInt(3);
        games.put(uuid, new GameInfo(uuid, winningDoor));
        Util.sleep(1500);
        return uuid;
    }

    @WithSpan(kind = SpanKind.INTERNAL)
    public int reveal(String uid) {
        GameInfo gameInfo = games.get(uid);
        return gameInfo.getDoorToReveal();
    }

    @WithSpan(kind = SpanKind.INTERNAL)
    public void pick(String uid, int picked) {
        GameInfo gameInfo = games.get(uid);
        gameInfo.pick(picked);
    }

    @WithSpan(kind = SpanKind.INTERNAL)
    public String getOutcome(String uid, int picked) {
        GameInfo gameInfo = games.get(uid);
        return gameOfficial.isWinner(gameInfo, picked) ? "WIN" : "LOSE";
    }
}
