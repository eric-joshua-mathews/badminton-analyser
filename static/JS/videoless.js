
// everything inside DOM to make sure materialize and other elements are fully loaded before JS runs
document.addEventListener("DOMContentLoaded",()=>{
    //court and wrapper

const court = document.getElementById("court");
const wrapper = document.getElementById("court-wrapper");

//state variables
let currentPlayer = 1; //1=user 2 = opponent
let rallyShots = [];
//court zones
const courtZones = {
    playable : document.getElementById("playable_area").getBBox(),
    playerRear : document.getElementById("player_rear").getBBox(),
    playerMid : document.getElementById("player_mid").getBBox(),
    playerFront: document.getElementById("player_front").getBBox(),
    shuttleRear : document.getElementById("shuttle_rear").getBBox(),
    shuttleMid : document.getElementById("shuttle_mid").getBBox(),
    shuttleFront: document.getElementById("shuttle_front").getBBox(),
    sideOutLeft : document.getElementById("side_out_left").getBBox(),
    sideOutRight : document.getElementById("side_out_right").getBBox()
}
// function to check SHUTTLE positions out the side or rear or front
function isOutOfBounds(x,y){
    if (x < courtZones.sideOutLeft.x || x> courtZones.sideOutRight.x ){
        return true;
    }
    if (y> courtZones.shuttleFront.y + courtZones.shuttleFront.height || y<courtZones.shuttleRear.y ){
        return true;
    }
    return false;
}

//function to place marker
function placeMarker(x, y, shuttle) {
    return undefined;
}

wrapper.addEventListener("click",handleLeftClick); //Player
wrapper.addEventListener("contextmenu",handleRightClick); //Shuttle


function handleRightClick(e) {
    e.preventDefault()
    const rect = wrapper.getBoundingClientRect();
    const x= e.clientX - rect.left;
    const y = e.clientY-rect.top;
    const out = isOutOfBounds(x,y);
    const marker = placeMarker(x,y,"shuttle");
    if (out){
        M.toast({html: 'The shuttle is out.Pressing any button will mark end of rally, press clear to undo.',classes: 'red darken-2'});
    }

}

function handleLeftClick(e) {
    e.preventDefault()
}
});