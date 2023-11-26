//MAKE IT SO THAT MY LOGIC CAN HANDLE WHEN THE USER JUMPS!!!!!!!!!!!!!!!

selectedCell = null;
currentPlayer = "";
currentMoves = []
let updatedBoard = [];//empty array filled with objects of pieces
let currentStringBoard = [
  //string of starter board, will be updated
  ["r", ".", "r", ".", "r", ".", "r", "."],
  [".", "r", ".", "r", ".", "r", ".", "r"],
  ["r", ".", "r", ".", "r", ".", "r", "."],
  [".", ".", ".", ".", ".", ".", ".", "."],
  [".", ".", ".", ".", ".", ".", ".", "."],
  [".", "w", ".", "w", ".", "w", ".", "w"],
  ["w", ".", "w", ".", "w", ".", "w", "."],
  [".", "w", ".", "w", ".", "w", ".", "w"],
];
let proposedMove = [
  ["r", ".", "r", ".", "r", ".", "r", "."],
  [".", "r", ".", "r", ".", "r", ".", "r"],
  ["r", ".", "r", ".", "r", ".", "r", "."],
  [".", ".", ".", ".", ".", ".", ".", "."],
  [".", ".", ".", ".", ".", ".", ".", "."],
  [".", "w", ".", "w", ".", "w", ".", "w"],
  ["w", ".", "w", ".", "w", ".", "w", "."],
  [".", "w", ".", "w", ".", "w", ".", "w"],
]

class piece {
  constructor(piece, row, column) {
    this.piece = piece;
    this.row = row;
    this.column = column;
  }
}


function updateBoard(sentArray) {
  //takes in a list and turns it into an array of objects
  updatedBoard = []
 

  for (let row = 0; row < 8; row++) {
    for (let column = 0; column < 8; column++) {
      updatedBoard.push(new piece(sentArray[row][column], row, column)); //objectify strings
    }
  }

  for (let i = 0; i < updatedBoard.length; i++) {
    //use array of objects to display board
    if (updatedBoard[i].piece == "r") {
      document.getElementById(
        updatedBoard[i].row + "" + updatedBoard[i].column
      ).innerHTML =
        "<div class='piece' style='padding: 12px;width: 40px; height: 40px; background-color: red;border: 2px solid white;border-radius: 50px; '></div>";
    } else if (updatedBoard[i].piece == "w") {
      document.getElementById(
        updatedBoard[i].row + "" + updatedBoard[i].column
      ).innerHTML =
        "<div class='piece'style='padding: 12px;width: 40px; height: 40px; background-color: black;border: 2px solid white;border-radius: 50px; '></div>";
    } else if (updatedBoard[i].piece == "R") {
      document.getElementById(
        updatedBoard[i].row + "" + updatedBoard[i].column
      ).innerHTML =
        "<div class='piece'style='padding: 12px;width: 40px; height: 40px; background-color: orange;border: 2px solid white;border-radius: 50px; '></div>";
    } else if (updatedBoard[i].piece == "W") {
      document.getElementById(
        updatedBoard[i].row + "" + updatedBoard[i].column
      ).innerHTML =
        "<div class='piece'style='padding: 12px;width: 40px; height: 40px; background-color: purple;border: 2px solid white;border-radius: 50px; '></div>";
    } else {
      document.getElementById(
        updatedBoard[i].row + "" + updatedBoard[i].column
      ).innerHTML = ""; //set location to blank
    }
  }


  
} //update board

function handleCellClick(){
  borderIf : if (event.target.closest(".cell")){
    if( event.target.closest(".piece")){
    cellId = event.target.closest(".cell").id //if click on circle, all good and assign cell id like 00 or 54
    } else {
      break borderIf; //if click on square but not circle
    }

    if(currentPlayer == "redMax"){ //exit the entire function if click on wrong colour of piece (do nothing)

      if(event.target.closest(".piece").style["background-color"] =="black"  || event.target.closest(".piece").style["background-color"] =="purple"){
        return;
      }
    } else {


      if(event.target.closest(".piece").style["background-color"] =="red" || event.target.closest(".piece").style["background-color"] =="orange"){
        return;
      }
    }

    if(updatedBoard.length ==0){
      break borderIf; 
    }//if board is empty
    
    
    if(selectedCell){// if a cell already is clicked, unselect the old one
      
      selectedCell.innerHTML = selectedCell.innerHTML.replace("green", "white")
      selectedCell = null;
    }//when unselecting a piece
    
    selectedCell = event.target.closest(".cell")
    event.target.closest(".piece").style.border = "2px solid green"

  }  else {
    selectedCell = null

  }//if
  
  moveIf : if(selectedCell && event.target.closest(".cell") ){
    
    for(let i = 0; i< updatedBoard.length; i++){
      if(updatedBoard[i].row + "" + updatedBoard[i].column == event.target.closest(".cell").id &&  ["w", "r", "R", "W"].includes(updatedBoard[i].piece) ){
        break moveIf; //if click on empty square
      }//if
    }//for

    //checking if proposed move is in allowed moves




    for(let i = 0; i<currentStringBoard.length;i++){
      proposedMove[i] = [...currentStringBoard[i]]
    }

    //swap proposed pieces, find legal proposed move
    let targettedCellId =  event.target.closest(".cell").id
    let targettedCellRow = parseInt(targettedCellId.charAt(0))
    let targettedCellColumn = parseInt(targettedCellId.charAt(1))
    let cellIdRow= parseInt(cellId.charAt(0))
    let cellIdColumn = parseInt(cellId.charAt(1))

    if(Math.abs(cellIdRow-targettedCellRow) ==1 && Math.abs(cellIdColumn-targettedCellColumn) ==1){ //if diagonal
      if(currentPlayer == "redMax" && targettedCellRow == 7 || currentPlayer == "whiMin" && targettedCellRow ==0){
        proposedMove[targettedCellId.charAt(0)][targettedCellId.charAt(1)] = proposedMove[cellId.charAt(0)][cellId.charAt(1)].toUpperCase()
  
        proposedMove[cellId.charAt(0)][cellId.charAt(1)] = "."

      } else {
      proposedMove[targettedCellId.charAt(0)][targettedCellId.charAt(1)] = proposedMove[cellId.charAt(0)][cellId.charAt(1)]

      proposedMove[cellId.charAt(0)][cellId.charAt(1)] = "."
      } //if going to last rank promote, else just swap
    } else {



  
      //dfs
      //pass in og board, see if you can reach the final position for that piece
      jumpStates = []
      dfs(proposedMove, cellIdRow, cellIdColumn, targettedCellRow, targettedCellColumn)
      if(jumpStates.length ==1){
        proposedMove = jumpStates[0]
      } else {
        return //not a valid jump
      }
      


    }

    


    

    for(let i = 0; i<currentMoves.length; i++){


  
      if(JSON.stringify(currentMoves[i]) ==JSON.stringify(proposedMove)){  //if this returns true its a valid board!
        //move is allowed
    
        
        for(let i = 0; i<currentStringBoard.length;i++){
          currentStringBoard[i] = [...proposedMove[i]]
        }


        //display move
        updateBoard(currentStringBoard)
        //get computer move and possible next plapyer moves
        
        fetch(baseURL + "getComputerMove/" + currentStringBoard).then(
          //send array as strings to the server
          (response) => {
            response.json().then((resp) => {

              currentStringBoard = resp[0].updatedState;

              updateBoard(currentStringBoard);
              currentMoves = resp[1].allStates
              
      
              currentPlayer = resp[2].player
            });
          }
        );
        break;
      } 
    }   
 }

}//handleCellClick


function dfs(root, initialRow, initialColumn, goalRow, goalColumn){

  

  if(currentPlayer =="redMax"){//if red's turn
    if(root[initialRow][initialColumn] == "r"){ //if not queen
      
      
      

      if(initialColumn <6 && initialRow <6 && root[initialRow+1][initialColumn+1].toLowerCase() == "w" && root[initialRow+2][initialColumn+2] == "."){ //check forwards left jump, assuming not too close to edge, and clear spaces
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }

        if(initialRow+2 == 7){
          newRoot[initialRow+2][initialColumn+2] = newRoot[initialRow][initialColumn].toUpperCase()
        } else {
          newRoot[initialRow+2][initialColumn+2] = newRoot[initialRow][initialColumn]
        }
        
        newRoot[initialRow+1][initialColumn+1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow+2 == goalRow && initialColumn+2 == goalColumn){
          jumpStates.push(newRoot) //add it to the right move list!
          return //quit!
        } else {
          dfs(newRoot, initialRow+2, initialColumn+2, goalRow, goalColumn) //go deeper
        }
        
        
      }

      if(initialColumn >1 && initialRow <6 && root[initialRow+1][initialColumn-1].toLowerCase() == "w" && root[initialRow+2][initialColumn-2] == "."){//check forwards right jump, not too close and clear
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }
        if(initialRow+2 == 7){
          newRoot[initialRow+2][initialColumn-2] = newRoot[initialRow][initialColumn].toUpperCase()
        } else {
          newRoot[initialRow+2][initialColumn-2] = newRoot[initialRow][initialColumn]
        }
        newRoot[initialRow+1][initialColumn-1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow+2 == goalRow && initialColumn-2 == goalColumn){
          jumpStates.push(newRoot)
          return
        } else {
          dfs(newRoot, initialRow+2, initialColumn-2, goalRow, goalColumn)
        }
      }

    } else {//if queen

      if(initialColumn <6 && initialRow <6 && root[initialRow+1][initialColumn+1].toLowerCase() == "w" && root[initialRow+2][initialColumn+2] == "."){ //check forwards left jump, assuming not too close to edge, and clear spaces
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }

        newRoot[initialRow+2][initialColumn+2] = newRoot[initialRow][initialColumn]
        newRoot[initialRow+1][initialColumn+1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow+2 == goalRow && initialColumn+2 == goalColumn){
          jumpStates.push(newRoot) //add it to the right move list!
          return //quit!
        } else {
          dfs(newRoot, initialRow+2, initialColumn+2, goalRow, goalColumn) //go deeper
        }
        
        
      }

      if(initialColumn >1 && initialRow <6 && root[initialRow+1][initialColumn-1].toLowerCase() == "w" && root[initialRow+2][initialColumn-2] == "."){//check forwards right jump, not too close and clear
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }
        newRoot[initialRow+2][initialColumn-2] =newRoot[initialRow][initialColumn]
        newRoot[initialRow+1][initialColumn-1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow+2 == goalRow && initialColumn-2 == goalColumn){
          jumpStates.push(newRoot)
          return
        } else {
          dfs(newRoot, initialRow+2, initialColumn-2, goalRow, goalColumn)
        }
      }

      if(initialColumn <6 && initialRow >1 && root[initialRow-1][initialColumn+1].toLowerCase() == "w" && root[initialRow-2][initialColumn+2] == "."){ //check backwards left jump, assuming not too close to edge, and clear spaces
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }

        newRoot[initialRow-2][initialColumn+2] = newRoot[initialRow][initialColumn]
        newRoot[initialRow-1][initialColumn+1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow-2 == goalRow && initialColumn+2 == goalColumn){
          jumpStates.push(newRoot) //add it to the right move list!
          return //quit!
        } else {
          dfs(newRoot, initialRow-2, initialColumn+2, goalRow, goalColumn) //go deeper
        }
        
        
      }

      if(initialColumn >1 && initialRow >1 && root[initialRow-1][initialColumn-1].toLowerCase() == "w" && root[initialRow-2][initialColumn-2] == "."){//check backwards right jump, not too close and clear
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }
        newRoot[initialRow-2][initialColumn-2] =newRoot[initialRow][initialColumn]
        newRoot[initialRow-1][initialColumn-1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow-2 == goalRow && initialColumn-2 == goalColumn){
          jumpStates.push(newRoot)
          return
        } else {
          dfs(newRoot, initialRow-2, initialColumn-2, goalRow, goalColumn)
        }
      }




    }
    

    
  } else{ //if whiMin


    if(root[initialRow][initialColumn] == "w"){ //if not queen
      
      
      

      if(initialColumn >1 && initialRow >1 && root[initialRow-1][initialColumn-1].toLowerCase() == "r" && root[initialRow-2][initialColumn-2] == "."){ //check forwards left jump, assuming not too close to edge, and clear spaces
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }

        if(initialRow-2 ==0){
          newRoot[initialRow-2][initialColumn-2] = newRoot[initialRow][initialColumn].toUpperCase()
        } else {
          newRoot[initialRow-2][initialColumn-2] = newRoot[initialRow][initialColumn]
        }
        
        newRoot[initialRow-1][initialColumn-1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow-2 == goalRow && initialColumn-2 == goalColumn){
          jumpStates.push(newRoot) //add it to the right move list!
          return //quit!
        } else {
          dfs(newRoot, initialRow-2, initialColumn-2, goalRow, goalColumn) //go deeper
        }
        
        
      }

      if(initialColumn <6 && initialRow >1 && root[initialRow-1][initialColumn+1].toLowerCase() == "r" && root[initialRow-2][initialColumn+2] == "."){//check forwards right jump, not too close and clear
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }
        if(initialRow-2 ==0){
          newRoot[initialRow-2][initialColumn+2] = newRoot[initialRow][initialColumn].toUpperCase()
        } else {
          newRoot[initialRow-2][initialColumn+2] = newRoot[initialRow][initialColumn]
        }
        newRoot[initialRow-1][initialColumn+1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow-2 == goalRow && initialColumn+2 == goalColumn){
          jumpStates.push(newRoot)
          return
        } else {
          dfs(newRoot, initialRow-2, initialColumn+2, goalRow, goalColumn)
        }
      }

    } else {//if queen

      if(initialColumn >1 && initialRow >1 && root[initialRow-1][initialColumn-1].toLowerCase() == "r" && root[initialRow-2][initialColumn-2] == "."){ //check forwards left jump, assuming not too close to edge, and clear spaces
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }

        newRoot[initialRow-2][initialColumn-2] = newRoot[initialRow][initialColumn]
        newRoot[initialRow-1][initialColumn-1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow-2 == goalRow && initialColumn-2 == goalColumn){
          jumpStates.push(newRoot) //add it to the right move list!
          return //quit!
        } else {
          dfs(newRoot, initialRow-2, initialColumn-2, goalRow, goalColumn) //go deeper
        }
        
        
      }

      if(initialColumn <6 && initialRow >1 && root[initialRow-1][initialColumn+1].toLowerCase() == "r" && root[initialRow-2][initialColumn+2] == "."){//check forwards right jump, not too close and clear
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }
        newRoot[initialRow-2][initialColumn+2] =newRoot[initialRow][initialColumn]
        newRoot[initialRow-1][initialColumn+1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow-2 == goalRow && initialColumn+2 == goalColumn){
          jumpStates.push(newRoot)
          return
        } else {
          dfs(newRoot, initialRow-2, initialColumn+2, goalRow, goalColumn)
        }
      }

      if(initialColumn >1 && initialRow <6 && root[initialRow+1][initialColumn-1].toLowerCase() == "r" && root[initialRow+2][initialColumn-2] == "."){ //check backwards left jump, assuming not too close to edge, and clear spaces
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }

        newRoot[initialRow+2][initialColumn-2] = newRoot[initialRow][initialColumn]
        newRoot[initialRow+1][initialColumn-1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow+2 == goalRow && initialColumn-2 == goalColumn){
          jumpStates.push(newRoot) //add it to the right move list!
          return //quit!
        } else {
          dfs(newRoot, initialRow+2, initialColumn-2, goalRow, goalColumn) //go deeper
        }
        
        
      }

      if(initialColumn <6 && initialRow <6 && root[initialRow+1][initialColumn+1].toLowerCase() == "r" && root[initialRow+2][initialColumn+2] == "."){//check backwards right jump, not too close and clear
        let newRoot = []
        for(let i = 0; i<root.length;i++){
          newRoot[i] = [...root[i]]
        }
        newRoot[initialRow+2][initialColumn+2] =newRoot[initialRow][initialColumn]
        newRoot[initialRow+1][initialColumn+1] ="."
        newRoot[initialRow][initialColumn] ="."
        if(initialRow+2 == goalRow && initialColumn+2 == goalColumn){
          jumpStates.push(newRoot)
          return
        } else {
          dfs(newRoot, initialRow+2, initialColumn+2, goalRow, goalColumn)
        }
      }




    }

  }


}


let baseURL = "http://127.0.0.1:5000/";



fetch(baseURL + "loadInformation/" + currentStringBoard).then(
  //send array as strings to the server
  (response) => {
    response.json().then((resp) => {
      currentPlayer = resp[1].player
      currentMoves = resp[0].allStates

      updateBoard(currentStringBoard);
    });
  }
);


document.addEventListener("click", handleCellClick);


