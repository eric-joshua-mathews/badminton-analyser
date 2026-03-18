
// everything inside DOM to make sure materialize and other elements are fully loaded before JS runs
document.addEventListener("DOMContentLoaded",()=>{

//court and wrapper
const appBody = document.getElementById("appBody");
const svg = document.getElementById("courtSVG");
const winnerOverlay=document.getElementById("winnerOverlay");
const state = {
    currentPlayer:1,
    playerPos:null,
    shuttlePos:null,
    shotType: null,
    rally : [],
    server:1,
    score:{1:0,2:0}
}
//on load
updateTheme();
updateLabels();
updateServeUI();
updateScoreUI();
//calling mouse handlers
svg.addEventListener("click",handleClick);
svg.addEventListener("contextmenu",handleClick);

//Serve subroutines
function setServer(player){
    state.server=player;
    state.currentPlayer=player;
    updateTheme();
    updateLabels();
    updateServeUI();

}

const serveCheckbox=document.getElementById("serveCheckbox")
serveCheckbox.addEventListener("change",(e)=>{setServer(e.target.checked?2:1)})

function updateServeUI() {
    document.getElementById("serveCheckbox").checked = state.server === 2;
    document.getElementById("serveDotP1").textContent = state.server === 1 ? "▶" : "";
    document.getElementById("serveDotP2").textContent = state.server === 2 ? "▶" : "";
}

////score subroutines
function updateScoreUI(){
 document.getElementById("scoreP1").textContent=state.score[1];
 document.getElementById("scoreP2").textContent=state.score[2];
}

//finish rally stuff
function finishRally(winner){
    state.score[winner]++;
    updateScoreUI();
    state.server=winner;
    state.currentPlayer=winner;
    updateServeUI();
    updateTheme();
    updateLabels();
    state.rally=[];
    ClearBtnFn();
    updateRallyHistory();
    M.toast({html:`Player ${winner} wins the point`, classes:"green-darken-1"});
}

//End rally button
const endRallyBtn = document.getElementById("EndRallyBtn");
endRallyBtn.addEventListener("click",EndRallyFn);

function EndRallyFn() {
    if (state.rally.length === 0 && !state.playerPos && !state.shuttlePos) {
        M.toast({ html: 'No shots recorded yet.', classes: 'blue darken-1' });
        return;
    }

    let winner;

    if (state.playerPos && state.shuttlePos) {
        const isOut = shuttleWrongSide(state.shuttlePos.zoneType);
        const finalLabel = isOut ? "Out" : "Rally End";
        state.rally.push({
            playerPos : state.playerPos,
            shuttlePos: state.shuttlePos,
            Player    : state.currentPlayer,
            shotType  : finalLabel,
            isFinal   : true,
        });
        updateRallyHistory();
        if (isOut) {
            // shuttle went out
            winner = state.currentPlayer === 1 ? 2 : 1;
        } else {
            //the player who hit last wins
            winner = state.currentPlayer;
        }
    } else {
        //whoever hit last in the rally wins
        const lastShot = state.rally[state.rally.length - 1];
        winner = lastShot.Player;
    }
    finishRally(winner);
}

//clear button
const ClearBtn = document.getElementById("ClearBtn");
ClearBtn.addEventListener("click",()=>{ClearBtnFn()});
function ClearBtnFn(){
    document.getElementById("playerMarker")?.remove();
    document.getElementById("shuttleMarker")?.remove();
    state.playerPos=null;
    state.shuttlePos=null;
}

//undo button -----------------------------------------> fully fix/test/implement
const undoBtn = document.getElementById("undoBtn");
undoBtn.addEventListener("click",()=>{UndoBtnFn()});
function UndoBtnFn(){
   if (state.rally.length===0){
    M.toast({html:"No shots in rally."});
    return;
   }
   state.rally.pop();
   updateRallyHistory();
}

//rally stuff
function updateRallyHistory(){
    const historyDiv = document.getElementById("rallyHistory");
    historyDiv.innerHTML="";
    for(let i=0;i<state.rally.length;i+=2){
        const moveNum = Math.floor(i/2)+1;
        const p1= state.rally[i];
        const p2= state.rally[i+1];
        const p1Shot= p1 ? p1.shotType:"";
        const p2Shot= p2 ? p2.shotType:"";

        historyDiv.innerHTML+=`
        <div class= "rallyRow">
            <div class="moveNum">${moveNum}</div>
            <div class="p1Move">${p1Shot}</div>
            <div class="p2Move">${p2Shot}</div>
        </div>`;
    }
}

//screen updates//////
function updateLabels(){
    const bottomLabel = document.getElementById("bottomLabel");
    const topLabel = document.getElementById("topLabel");
    if(state.currentPlayer===1){
        bottomLabel.textContent= "Player";
        topLabel.textContent = "Shuttle";
    }else{
        bottomLabel.textContent= "Shuttle";
        topLabel.textContent = "Player";
    }
}

function updateTheme(){
    appBody.classList.remove("player1-theme", "player2-theme");
    if (state.currentPlayer===1){
    appBody.classList.add("player1-theme")
    } else{
    appBody.classList.add("player2-theme")
    }
}

function placeMarker(x,y,type){
    // remove old markers limiting to 1 player and 1 shuttle
    const existing = document.getElementById(type + "Marker");
    if (existing) existing.remove();
    const marker =document.createElementNS("http://www.w3.org/2000/svg","image");
    const size = 24;
    marker.setAttributeNS(null,"href",type==="player" ? "/static/images/player.png" : "/static/images/shuttle.png");
    marker.setAttribute("x",x-size/2);
    marker.setAttribute("y",y-size/2);
    marker.setAttribute("width",size);
    marker.setAttribute("height",size);
    marker.setAttribute("id",type+"Marker");
    marker.classList.add("marker");
    svg.appendChild(marker);
}

//Next shot button
const nextShotBtn = document.getElementById("nextShotBtn");
nextShotBtn.addEventListener("click",()=>{nextShotBtnFn()});
function nextShotBtnFn(){
    //check both are placed
    if (!state.playerPos||!state.shuttlePos){
        M.toast({html: 'Please mark both player and shuttle first.',classes: 'blue darken-1'});
        return;
    }
    //check if player location makes sense
    if (isNotValidPlayerPos(state.playerPos.zoneType)) {
        M.toast({html: 'Please mark a valid player position.',classes: 'red darken-1'});
        return
    }
    //if shuttle is out, disable button ==> end rally button
    if (shuttleWrongSide(state.shuttlePos.zoneType)){
        M.toast({html: 'Shuttle is out.Please press end rally or mark again.',classes: 'red darken-1'});
        return;
    }

    const prevShuttlePos= {...state.shuttlePos};
    //send to guess Shot function

    let playerType = state.playerPos.zoneType;
    let shuttleType = state.shuttlePos.zoneType;
    // If Player 2 is hitting, swap meaning
    if (state.currentPlayer === 2) {
        playerType = playerType === "Player" ? "Shuttle" : "Player";
        shuttleType = shuttleType === "Player" ? "Shuttle" : "Player";
    }

    const playerLocation = playerType.toLowerCase() + "_" + state.playerPos.zoneName.toLowerCase();
    const shuttleLocation = shuttleType.toLowerCase() + "_" + state.shuttlePos.zoneName.toLowerCase();
    console.log("player",playerLocation,"11111 shuttle", shuttleLocation); //used for debugging
    fetch("/guess_shot",{
       method: "POST",
       headers: {"Content-Type":"application/json"},
       body:JSON.stringify({
           playerLocation:playerLocation,
           shuttleLocation:shuttleLocation,
           Px:state.playerPos.x,
           Sx:state.shuttlePos.x
           })
    })
    .then(res=>res.json())
    .then(data=>{ console.log("Shot guessed: ",data.shot);
        M.toast({html: data.shot ,classes: 'purple'}); //create a change button in notif
        //push state
        state.rally.push({
        playerPos: state.playerPos,
         shuttlePos: state.shuttlePos,
         Player: state.currentPlayer,
         shotType:data.shot});
         //switch current player
    state.currentPlayer===1? state.currentPlayer=2 : state.currentPlayer=1;
    ClearBtnFn();
    updateRallyHistory();
    //set current player's location to old shuttle's location
    if (prevShuttlePos.zoneType !== "Out")
        state.playerPos ={
        zoneType: prevShuttlePos.zoneType,
         zoneName: prevShuttlePos.zoneName,
         x:prevShuttlePos.x,
         y:prevShuttlePos.y};

    //M.toast({html: 'Shot recorded.',classes: 'green'});
    updateTheme();
    updateLabels();
    console.log("shot", state.rally);
    placeMarker(prevShuttlePos.x,prevShuttlePos.y, "player");
       });

}

//position validation
function shuttleWrongSide(zoneType){
    if (state.currentPlayer===1){
                return !(zoneType==="Shuttle");
            } else {
                return !(zoneType==="Player");
            }
}

function isNotValidPlayerPos(zoneType){
        if (state.currentPlayer===1){
            return zoneType!="Player";
        } else {
            return zoneType!="Shuttle";
        }
}

//svg handling
function getSVGCoords(e){
    const pt = svg.createSVGPoint();
    pt.x = e.clientX;
    pt.y = e.clientY;
    svgPt = pt.matrixTransform(svg.getScreenCTM().inverse())
    return {x:svgPt.x, y:svgPt.y}
}

function getClickContext (e){
    const group = e.target.closest("g")
    const rect = e.target.closest("rect")
    if (!group || !svg.contains(group)||!rect)
        return null;
    return {zoneType : group.dataset.zone, zoneName: rect.dataset.type};  //player or shuttle ,,,, rear mid front etc.
}

function handleClick(e){
     e.preventDefault();
     ctx= getClickContext(e)
     const {x,y} = getSVGCoords(e);
     if (!ctx) return;
     const {zoneType , zoneName} = ctx;
     //player
     if (e.type==="click"){
         state.playerPos = {
         zoneType: ctx.zoneType,
         zoneName: ctx.zoneName,
         x:x,
         y:y
         };
         const invalidPlayer = isNotValidPlayerPos(state.playerPos.zoneType);
         if (invalidPlayer){
            M.toast({html: 'Please be aware the player cannot be there.',classes: 'red darken-2'});
         }
         placeMarker(x,y,"player");
     }
     //shuttle
     if (e.type ==="contextmenu"){
         state.shuttlePos={
         zoneType: ctx.zoneType,
         zoneName: ctx.zoneName,
         x:x,
         y:y
         };
         if (shuttleWrongSide(ctx.zoneType)){
            M.toast({html: 'Please be aware the shuttle is out.',classes: 'red darken-2'});
         }
         placeMarker(x,y,"shuttle");
     }
 }
});