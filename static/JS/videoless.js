
// everything inside DOM to make sure materialize and other elements are fully loaded before JS runs
document.addEventListener("DOMContentLoaded",()=>{
    //court and wrapper

const court = document.getElementById("court");
const wrapper = document.getElementById("court-wrapper"); //maybe not needed
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


court.addEventListener("click",handleLeftClick); //Player
court.addEventListener("contextmenu",handleRightClick); //Shuttle

function getClickContext (e){
    //const target=e.target;
    const group = e.target.closest("g")
    const rect = e.target.closest("rect")
    if (!group || !court.contains(group))
        return null;

    return {group : group , zone: rect.id};
}


function handleRightClick(e) { //shuttle
    e.preventDefault()
    const {group, zone} = getClickContext(e)
    if(!group)
        return null;
    state.shuttlePos = group.dataset.zone; //parent -> shuttle or player side
    const out = isOutOfBounds(state.shuttlePos);
    //const marker = placeMarker(x,y,"shuttle");
    if (out){
        M.toast({html: 'Please be aware the shuttle is out.',classes: 'red darken-2'});
    }

}
function isOutOfBounds(type){
      return type!=="Shuttle";
}

function handleLeftClick(e) { //player
    e.preventDefault()
    const {group, zone} = getClickContext(e)
    if(!group)
        return null;
    state.playerPos = group.dataset.zone;
    const invalidPlayer = isNotValidPlayer(state.playerPos);

//for debugging
    console.log(type, "- group")
    console.log(state.playerPos, "- zone")


    //place marker
    if (invalidPlayer){
        M.toast({html: 'Please be aware the player cannot be there.',classes: 'red darken-2'});
    }
}
function isNotValidPlayer(type){
        return type==="Shuttle"||type===undefined ;


 function handleClick(e){
     e.preventDefault()
     const {group , zone} = getClickContext(e)
     if (!group){
         return null
     }
     if (e.type==="click"){ //right
         state.playerPos = group.dataset.zone; //CHECK TO SEE IF IT NEEDA BE TYPE
         const invalidPlayer = isNotValidPlayer(state.playerPos);
         //add marker
         if (invalidPlayer){
            M.toast({html: 'Please be aware the player cannot be there.',classes: 'red darken-2'});
         }
     }
     if (e.type ==="contextmenu"){
         state.shuttlePos=group.dataset.zone //CHECK TO SEE IF IT NEEDA BE TYPE
         if (isOutOfBounds(state.shuttlePos)){
            M.toast({html: 'Please be aware the shuttle is out.',classes: 'red darken-2'});
         }
     }

 }
}
});