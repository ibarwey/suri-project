module.exports = class User {
    constructor(id) {
        this.id = id;
        this.index = 1;
        this.questionArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 2,2,2,2, 1,1,1, 2, 3, 5]; //40 none, 5 knife, 3 gun, 1 wrench, 1 scissor
        this.currentQuestion = 0;
        this.prevTime = 30;
    }

    currentQ(){
        return this.currentQuestion
    }

    nextquestion(){
        this.index = this.index + 1
    }

    setPrevTime(time){
        this.prevTime = time
    }

    getPrevTime(){
        return this.prevTime
    }

    selectQuestion(){

        var candidates = []

        for(var i = 0, length = this.questionArray.length; i < length; i++){
            if (this.questionArray[i] == 0){
                candidates.push(i)
            }
        }
        console.log(candidates)

        var questionNumber = candidates[Math.floor(Math.random() * candidates.length)]
        this.questionArray[questionNumber] = 1
        questionNumber = questionNumber + 1
        this.currentQuestion = questionNumber
        return questionNumber
    }
};
