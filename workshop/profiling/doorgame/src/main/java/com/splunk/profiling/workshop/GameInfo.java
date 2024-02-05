package com.splunk.profiling.workshop;

import java.util.Random;

class GameInfo {
    private final String uuid;
    private final int winningDoor;
    private int doorPicked = -1;
    private int doorToReveal = -1;

    GameInfo(String uuid, int winningDoor) {
        this.uuid = uuid;
        this.winningDoor = winningDoor;
    }

    int getDoorToReveal(){
        if(doorPicked == -1){
            throw new IllegalStateException("Must pick a door first");
        }
        if(doorToReveal != -1) { // already picked
            return doorToReveal;
        }
        doorToReveal = new Random().nextInt(3);
        while((doorToReveal == doorPicked) || (doorToReveal == winningDoor)){
            doorToReveal = new Random().nextInt(3);
        }
        return doorToReveal;
    }

    void pick(int doorNum){
        doorPicked = doorNum;
    }

    boolean isWinner(int doorNum) {
        return doorNum == winningDoor;
    }

    public String getUuid() {
        return uuid;
    }
}
