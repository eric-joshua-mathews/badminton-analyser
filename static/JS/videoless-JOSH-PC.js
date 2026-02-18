
// everything inside DOM to make sure materialize and other elements are fully loaded before JS runs
document.addEventListener("DOMContentLoaded",()=>{
const svg = document.getElementById("courtSvg")
const state = {
    currentPlayer : 1,
    playerPos: null,
    shuttlePos: null,
    rallyShots: []
};
//Player
court.addEventListener("click",handleLeftClick);
//Shuttle
court.addEventListener("contextmenu",handleRightClick);

function getClickContext (e){ //
    const target=e.target;
    const group = e.target.closest("g")
    const rect = e.target.closest("rect")
    if (!group || !court.contains(group))
    return null; return {group : group , zone: rect.id}; }

function handleRightClick(e) { //shuttle
    e.preventDefault() const {group, zone} = getClickContext(e)
    if(!group) return null;
    state.shuttlePos = group.dataset.zone; //parent -> shuttle or player side
    const out = isOutOfBounds(state.shuttlePos); //
    const marker = placeMarker(x,y,"shuttle");

if (out){
M.toast({html: 'Please be aware the shuttle is out.',classes: 'red darken-2'}); }
}


function isOutOfBounds(type){
    return type!=="Shuttle";
}
function handleLeftClick(e) { //player
 e.preventDefault() const {group, zone} = getClickContext(e)
 if(!group) return null;
  state.playerPos = group.dataset.zone;
  const invalidPlayer = isNotValidPlayer(state.playerPos);
   //for debugging
    console.log(type, "- group")
    console.log(state.playerPos, "- zone")
    //place marker
     if (invalidPlayer){
        M.toast({html: 'Please be aware the player cannot be there.',classes: 'red darken-2'}); }
      }
 function isNotValidPlayer(type){
        return type==="Shuttle"||type===undefined ;
     }
});