#enter envinronment with source .venv/bin/activate, exit with deactivate
#have to be in checkersAI

#use these lines to change between modes
#export FLASK_ENV=development
#export FLASK_ENV=production

import logic
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

class getComputerMove(Resource):
    def get(self, userBoard):

        if logic.player =="redMax":
            logic.player = "whiMin"
        else:
            logic.player = "redMax"
        userBoard = userBoard.split(",") #this is just a 1D array with all pieces, need to transform
        userBoardFormatted = [] #this is the in right format for minimax, a 2D array
        n=0
        for row in range(8):
            tempRow = []
            for piece in range(8):
                tempRow.append(userBoard[n])
                n +=1
            userBoardFormatted.append(tempRow)


        evalNum, updatedState = logic.minimax(
            userBoardFormatted, 6, logic.player, float("-inf"), float("inf")
        )

        if logic.player =="redMax":
            logic.player = "whiMin"
        else:
            logic.player = "redMax"

   
        
        allStates = logic.getSuccessors(updatedState, logic.player)


        return [{"updatedState": updatedState},{"allStates": allStates}, {"player": logic.player}]




class loadInformation(Resource):
    def get(self, userBoard):
        userBoard = userBoard.split(",") #this is just a 1D array with all pieces, need to transform
        userBoardFormatted = [] #this is the in right format for minimax, a 2D array
        n=0
        for row in range(8):
            tempRow = []
            for piece in range(8):
                tempRow.append(userBoard[n])
                n +=1
            userBoardFormatted.append(tempRow)
        allStates = logic.getSuccessors(userBoardFormatted, logic.player)
        return [{"allStates": allStates}, {"player": logic.player}]
    








    
api.add_resource(getComputerMove, "/getComputerMove/<string:userBoard>")

api.add_resource(loadInformation, "/loadInformation/<string:userBoard>")


if __name__ == "__app__":
    app.run(debug=True)


