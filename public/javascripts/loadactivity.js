var timeText
var rotations = 0

// Mouse pointer location
var mouse_x = null;
var mouse_y = null;

function drawCanvas(imageSource) {
    imageObj = new Image();
    imageObj.onload = function () {
        ctx.drawImage(imageObj, 0, 0, imgWidth, imgHeight);
    };
    imageObj.src = imageSource;
    canvas.addEventListener('mousemove', function(e){trackMouse(duration,e)}, false);
    canvas.addEventListener('mousedown', mouseDown, false);
    canvas.addEventListener('mouseup', mouseUp, false);
    canvas.addEventListener('mousemove', mouseMove, false);
}

//BOUNDING BOX
function mouseDown(e) {
  rect.startX = e.offsetX;
  rect.startY = e.offsetY;
  drag = true;
}

function mouseUp() {
    drag = false;
}

function mouseMove(e) {
  mousex = e.offsetX;
  mousey = e.offsetY;

  if(drag){
      ctx.clearRect(0, 0, canvas.width, canvas.height); //clear canvas
      ctx.drawImage(imageObj, 0, 0, imgWidth, imgHeight);
      ctx.beginPath();
      rect.w = mousex - rect.startX;
      rect.h = mousey - rect.startY;
      ctx.strokeStyle = 'red';
      ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
      ctx.closePath();
  }

    //Output
    $('#output').html('current: ' + mousex + ', ' + mousey + '<br/>last: ' + rect.startX + ', ' + rect.startY + '<br>height: ' + rect.h + ', width: ' + rect.w + '<br/>' + '<br/>mousedown: ' + drag + '<br>offset: ' + this.offsetLeft + ', ' + this.offsetTop + '</br>');
}

//MOUSE TRACKING
mouseArray = [];
var timeChange2 = setInterval(function() {duration = Math.round((duration - .1) * 10) / 10}, 100);

function trackMouse(duration,e) {
  mouseArray.push([duration,e.offsetX,e.offsetY]);

  zoomctx.drawImage(imageObj, e.offsetX, e.offsetY, 100, 100, 0, 0, imgWidth, imgHeight)
}

function renderQuestion(userID, sequence, duration) {
    exercise_img_src = "/images/sixray/" + sequence + ".jpg";

    obj_img = "/images/objects/targetobjects.png";

    if (duration > 0) {
        drawCanvas(exercise_img_src);

        document.getElementById("img2find").src = obj_img;
        document.getElementById("img2find").width = "200"
    } else {
        document.getElementById("canvas").style.visibility = "hidden";
        document.getElementById("imgText").innerHTML = "Times up! Submit your answer.";
        display.textContent = " 00:00";
    }

    var canvas = document.getElementById("canvas");

    var w = window.innerWidth;

    //
    //Button
    //
    d3.select(".btn-outline-success").on("click", function () {
      console.log("BUTTON PRESSED");
        var q1 = [];

        //
        //Get time
        //
        var timeLeft = document.getElementById("time").innerHTML
        console.log(timeLeft)

        timeLeft = timeLeft.substring(timeLeft.length - 2)
        timeLeft = parseInt(timeLeft)
        console.log(timeLeft)

        //
        //Question 1
        //

        var radio00 = document.getElementById('00')
        var radio01 = document.getElementById('01')
        var radio02 = document.getElementById('02')
        var radio03 = document.getElementById('03')
        var radio04 = document.getElementById('04')
        var radio05 = document.getElementById('05')
        var radio06 = document.getElementById('06')



        if (radio00.checked){
            q1[0] = 0;
            rect.X = null
            rect.Y = null
            rect.w = null
            rect.h = null

            document.getElementById("popup").innerText = "";

        }
        else if (radio01.checked){
            q1[0] = 1;
        }
        else if (radio02.checked){
            q1[0] = 2;
        }
        else if (radio03.checked){
            q1[0] = 3;
        }
        else if (radio04.checked){
            q1[0] = 4;
        }
        else if (radio05.checked){
            q1[0] = 5;
        }
        else if (radio06.checked){
            q1[0] = 6;
        }
        console.log(q1)

        sendData(userID, timeLeft, q1, rect, mouseArray);

    })
}


function sendData(userID, time, q1, bb, array) {
    console.log("sending data")

    url2go = userID + "/data"
    data2send = [time, q1, bb, array]
    console.log("time: " + time +
                " q1: " + q1 +
                " boundingBox: {" + bb.startX + ", " + bb.startX + ", " + bb.w + ", " + bb.h + "}" +
                " mouseArray: {" + array + "}");

    //add ajax function
    new Promise((resolve, reject) => {
        $.ajax({
            dataType: "json",
            url: url2go,
            type: "POST",
            data: JSON.stringify(data2send),
            success: resolve
        });
    });
}

function startTimer(duration, display, captionText, userID) {
    var timer = duration, minutes, seconds;
    var timeChange = setInterval(function () {
        if (--timer < 0) {
            clearInterval(timeChange)
            document.getElementById("canvas").style.visibility = "hidden";
            document.getElementById("imgText").innerHTML = "Times up! Submit your answer.";
            display.textContent = " 00:00";

            return
        } else {
            minutes=0;
            seconds = parseInt(timer % 60, 10);
            seconds = seconds < 10 ? "0" + seconds : seconds;
            display.textContent = "0:" + seconds;
            captionText.innerHTML = "Time remaining is " + timeText;
            timeText = "0:" + seconds;
        }

    }, 1000);
}
