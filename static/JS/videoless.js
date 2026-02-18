
// everything inside DOM to make sure materialize and other elements are fully loaded before JS runs
document.addEventListener("DOMContentLoaded",()=>{
    //court and wrapper

const court = document.getElementById("court");
const state = {
    player:1,
    playerPos:null,
    shuttlePos:null,
    rally : []
}

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
} //maybe useless


court.addEventListener("click",handleClick);
court.addEventListener("contextmenu",handleClick);

function getClickContext (e){
    //const target=e.target;
    const group = e.target.closest("g")
    const rect = e.target.closest("rect")
    if (!group || !court.contains(group)||!rect)
        return null;

    return {group : group , zone: rect.id};
}

function isOutOfBounds(type){
      return type!=="Shuttle";
}
function isNotValidPlayer(type){
        return type==="Shuttle"||type===undefined ;
}
function getSVGCoords(e){
const pt = court.createSVGPoint();
pt.x = e.clientX;
pt.y = e.clientY;
return pt.matrixTransform(court.getScreenCTM().inverse())
}
function handleClick(e){
     e.preventDefault();
     ctx= getClickContext(e)
     if (!ctx) return;
     const {group , zone} = ctx;
     if (!group){
         return null
     }
     if (e.type==="click"){ //left click
         state.playerPos = group.dataset.zone; //CHECK TO SEE IF IT NEEDA BE TYPE
         const invalidPlayer = isNotValidPlayer(state.playerPos);
         //add marker
         if (invalidPlayer){
            M.toast({html: 'Please be aware the player cannot be there.',classes: 'red darken-2'});
         }
     }
     if (e.type ==="contextmenu"){ // right click
         state.shuttlePos=group.dataset.zone //CHECK TO SEE IF IT NEEDA BE TYPE
         if (isOutOfBounds(state.shuttlePos)){
            M.toast({html: 'Please be aware the shuttle is out.',classes: 'red darken-2'});
         }
     }
 }
});