var express = require('express');
var router = express.Router();
var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
const co = require('co');
const User = require('../User');
const { response } = require('express');
var url = 'mongodb://0.0.0.0:27017/'; //for server tests
//var url = 'mongodb://localhost:27014/'; //for local tests

var datab = 'suri-project'
var userID = null;
let users = [];
var totalQs = 50;
//get user instance function
let getUserInstance = uid => users.find(user => user.id === uid);
//snooze function
const snooze = ms => new Promise(resolve => setTimeout(resolve, ms));
//
//Get home page
//


router.get('/', function(req, res, next) {
 res.render('index');
});
//
//Create user and load first activity
//
router.post('/activity/', function(req,res,next){
 //prompt to enter username if null
 if (!req.body.userID) {
   res.render('index', {error: "ERROR: Please enter a username"});
   return;
 }
 //Fetch current user
 let currentUser = getUserInstance(req.body.userID);
 //add new user if not already exists based on id
 if (!currentUser) {
   users.push(new User(req.body.userID));
   currentUser = getUserInstance(req.body.userID);
 }
 questionNum = currentUser.selectQuestion()
 console.log(questionNum)

 //store user in db

 co(function* () {

   let client = yield MongoClient.connect(url, { useNewUrlParser: true, useUnifiedTopology: true });
   var db = client.db(datab)
   let usersCol = db.collection('users')
   check = yield usersCol.findOne({"user" : currentUser.id})

   if(check === null) {
      var item = {
        "user": currentUser.id,
        "key2pay": null,
        "surveyResults": null,
        "score": null
      };

      usersCol.insertOne(item);

      res.render('activity', {time: 30, userID: currentUser.id, question: questionNum, sequence: currentUser.index})
   }
   else {
     res.render('index', {error: "ERROR: Already completed activity!"})
   }

 });
});




//
//load activity
//




router.post('/activity/:userID/', function(req,res,next){


  //Fetch current user
  let currentUser = getUserInstance(req.params.userID);
  prevTime = currentUser.getPrevTime();

  //check to ensure previous response was posted
  co(function* () {

    yield snooze(1000)

    let client = yield MongoClient.connect(url, { useNewUrlParser: true, useUnifiedTopology: true });
    const db = client.db(datab)
    let responseCol = db.collection('responses')
    let usersCol = db.collection('users')

    check = yield responseCol.findOne({"user" : currentUser.id, "question" : currentUser.currentQ()})

    /*if (check == null){


      res.render('activity',
                  {time: prevTime -1,
                    userID: currentUser.id,
                    question: currentUser.currentQ(),
                    sequence: currentUser.index,
                    error: "ERROR: Please answer all questions!"
      })


    }else{*/


      currentUser.nextquestion()
      questionNum = currentUser.selectQuestion()


      if (currentUser.index <= totalQs){
        console.log("Q no: " + currentUser.index);
        res.render('activity', {time: 30, userID: currentUser.id, question: questionNum, sequence: currentUser.index})
      }
      else{
        //change Ground Truth Array
          var correct = []
          var truth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 2,2,2,2, 1,1,1, 2, 3, 5]; //40 none, 5 knife, 3 gun, 1 wrench, 1 scissor


        //get results
        for(i = 0; i < totalQs; i++){


          var response = yield responseCol.findOne({"user": currentUser.id, "question" : i+1})
          console.log(response)
          if (response == null){
            console.log('null response')
          }
          else if (response["q1"] == truth[i]){
            correct.push(1)
          } else{
            correct.push(0)
          }
        //}


        var sum = 0


        //save score of user
        for(i = 0; i < totalQs; i++){
     sum = sum + correct[i]
        }


        newItem = {"score" : sum}


        usersCol.updateOne({"user": currentUser.id}, { $set: newItem });


        //get leaderboard
        leaders = usersCol.find().sort({score: -1}).toArray(function(err, leaderboard) {
          if (err) throw err;
          leaderboard = leaderboard.slice(0,5)
          res.render('leaderboard', {userID: currentUser.id, total: sum, leaderboard})
        });
      }


    }
  });


});






//
//Store data
//


router.post('/activity/:userID/data', function(req,res,next){


  userID = req.params.userID;


  let currentUser = getUserInstance(userID);


  question = currentUser.currentQ()


  let group = Object.keys(req.body)
  group = JSON.parse(group)
  console.log(group)


  TimeLeft = group[0]
  currentUser.setPrevTime(TimeLeft)
  time = 30 - TimeLeft


  console.log('timeLeft  ', TimeLeft)
  console.log('time spent  ', time)


  //store response in db
  co(function* () {


    let client = yield MongoClient.connect(url,{ useNewUrlParser: true, useUnifiedTopology: true });
    const db = client.db(datab)
    let responseCol = db.collection('responses')


    console.log("GROUP 2 DATA: ");
    console.log(group[2]);
    console.log("GROUP 1 DATA: ");
    console.log(group[1]);
    var item = {
      "user": userID,
      "question": question,
      "time": time,
      "q1": group[1],
      "boundingBox": group[2],
      "mouseArray" : group[3]
    };


    if (group[1] != -2){


      yield responseCol.insertOne(item);
      console.log('posted to db!')


    }else{
      console.log("invalid input, retry")
    }


  });


});


router.post('/activity/:use/:userID/data', function(req,res,next){


  userID = req.params.userID;


  let currentUser = getUserInstance(userID);


  question = currentUser.currentQ()


  let group = Object.keys(req.body)
  group = JSON.parse(group)


  TimeLeft = group[0]
  currentUser.setPrevTime(TimeLeft)
  time = 30 - TimeLeft


  console.log('timeLeft  ', TimeLeft)
  console.log('time spent  ', time)


  //store response in db
  co(function* () {


    let client = yield MongoClient.connect(url, { useNewUrlParser: true, useUnifiedTopology: true });
    const db = client.db(datab)
    let responseCol = db.collection('responses')


    var item = {
      "user": userID,
      "question": question,
      "time": time,
      "q1": group[1],
      "boundingBox" : group[2],
      "mouseArray" : group[3]

    };


    if (group[1] != -2){


      yield responseCol.insertOne(item);
      console.log('posted to db!')




    }else{
      console.log("invalid inuput, retry")
    }


  });


});


module.exports = router;
