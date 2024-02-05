package com.splunk.profiling.workshop;

import static com.splunk.profiling.workshop.Util.sleep;

public class DoorChecker {

    public boolean isWinner(GameInfo gameInfo, int picked) {
        switch(picked){
            case 0:
                return checkDoorZero(gameInfo);
            case 1:
                return checkDoorOne(gameInfo);
            case 2:
                return checkDoorTwo(gameInfo);
        }
        throw new IllegalArgumentException("Invalid door number " + picked);
    }

    private boolean checkDoorZero(GameInfo gameInfo) {
        precheck(0);
        return gameInfo.isWinner(0);
    }

    private boolean checkDoorOne(GameInfo gameInfo) {
        precheck(1);
        return gameInfo.isWinner(1);
    }

    private boolean checkDoorTwo(GameInfo gameInfo) {
        precheck(2);
        return gameInfo.isWinner(2);
    }

    private void precheck(int doorNum) {
        long extra = (int)Math.pow(70, doorNum);
        sleep(300 + extra);
    }
}
