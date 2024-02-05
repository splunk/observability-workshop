
console.log('doorgame starting.');

let gameId = null;
let revealedDoor = null;
let chosenDoor = null;

function startGame(){
    console.log('Starting new game');
    show('throbber1');
    hide('start-button');
    document.getElementById('game-heading').innerText = 'THE DOOR GAME';
    return fetch(`/new-game`)
        .then(res => res.text())
        .then(id => {
            gameId = id;
            console.log(`New game started: ${gameId}`);
            enableDoors();
            show('door-row');
            show('choose-a-door');
            hide('start-button');
            hide('throbber1');
        });
}

async function doorClicked(num) {
    console.log(`Door ${num} picked.`);
    chosenDoor = num;
    disableDoors();
    doorThrob(num);

    const url = `/game/${gameId}/pick/${num}`;
    await fetch(url, { method: 'POST'})
        .then(res => res.text())
        .then(res => {
            console.log(`Response: ${res}`);
            show(`door${num}`);
            hide(`door${num}-throb`);
        });
    hide('choose-a-door');
    showChoice(num);
    fetch(`/game/${gameId}/reveal`)
        .then(res => res.text())
        .then(res => parseInt(res))
        .then(res => {
            console.log(`Revealing door ${res}`);
            revealedDoor = res;
            showZonk(res);
        });
}

function doorThrob(num){
    hide(`door${num}`);
    show(`door${num}-throb`);
}

function disableDoors(){
    ['door0', 'door1', 'door2'].forEach(sel => {
        document.getElementById(sel).style.cursor = 'default';
        document.getElementById(sel).onclick = () => {};
    });
}

function enableDoors(){
    [0, 1, 2].forEach(n => {
        document.getElementById(`door${n}`).style.cursor = 'pointer';
        document.getElementById(`door${n}`).onclick = () => doorClicked(n);
    });
}

function showChoice(doorNum){
    show(`choose${doorNum}`);
}

function showZonk(){
    document.getElementById('change-prompt').innerHTML = `You picked door #${chosenDoor+1}.<br/>There was a ZONK behind door #${revealedDoor+1}.<br/>Final decision:`;
    show('change-prompt');
    hide(`door${revealedDoor}`);
    show('change-button');
    document.getElementById('stay-button').innerText = `Stay with door #${chosenDoor+1}`;
    // this is a clever way of finding the remaining door..._too_ clever
    const remaining = 3 - (chosenDoor + revealedDoor);
    document.getElementById('change-button').innerText = `Switch to door #${remaining+1}`;
    show('stay-button');
    show(`zonk${revealedDoor}`);
}

async function choiceKeep(){
    const otherDoor = 3 - (chosenDoor + revealedDoor);
    doorThrob(otherDoor);
    doorThrob(chosenDoor);
    finishGame(chosenDoor, otherDoor);
}

async function choiceChange() {
    const changeTo = 3 - (chosenDoor + revealedDoor);
    doorThrob(changeTo);
    doorThrob(chosenDoor);
    finishGame(changeTo, chosenDoor);
}

async function finishGame(finalChoice, otherDoor){

    hide(`choose${otherDoor}`);
    show(`choose${finalChoice}`);
    const outcome = await getOutcome(finalChoice);
    console.log(outcome);
    hide(`door${finalChoice}`);
    hide(`door${otherDoor}`);
    hide(`door${otherDoor}-throb`);
    hide(`door${finalChoice}-throb`);
    hide('change-prompt');
    hide('stay-button');
    hide('change-button');
    if(outcome === 'WIN'){
        show(`money${finalChoice}`);
        show(`zonk${otherDoor}`);
        document.getElementById('win-lose').innerText = "YOU WIN!";
    }
    else {
        show(`zonk${finalChoice}`);
        show(`money${otherDoor}`);
        document.getElementById('win-lose').innerText = "YOU LOSE!";
    }
    show('win-lose');
    show('play-again');
}

async function getOutcome(doorNum) {
    const url = `/game/${gameId}/picked/${doorNum}/outcome`;
    return fetch(url)
        .then(res => res.text());
}

function playAgain(){
    gameId = null;
    revealedDoor = null;
    chosenDoor = null;
    hide('win-lose');
    hide('play-again');
    [0,1,2].forEach(n => {
        hide(`zonk${n}`);
        hide(`choose${n}`);
        hide(`money${n}`);
        show(`door${n}`);
    });
    enableDoors();
    show('throbber1');
    startGame();
}

function show(sel){
    document.getElementById(sel).classList.remove('visually-hidden');
}
function hide(sel){
    document.getElementById(sel).classList.add('visually-hidden');
}