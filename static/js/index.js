// wait for the content of the window element 
// to load, then performs the operations. 
// This is considered best practice. 
var mode = "pen";
window.addEventListener('load', () => {

    resize(); // Resizes the canvas once the window loads 
    document.addEventListener('mousedown', startPainting);
    document.addEventListener('mouseup', stopPainting);
    document.addEventListener('mousemove', sketch);
    window.addEventListener('resize', resize);

    document.getElementById("pen").click(function() {
        mode = "pen";
    });
    document.getElementById("eraser").click(function() {
        console.log("bivjlkd;b");
        mode = "eraser";
    });

});

const canvas = document.querySelector('#canvas');

/*const detectButton = document.querySelector('#btn')

detectButton.onclick = function() {

    var imgURL = canvas.toDataURL();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("url").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/main/detect", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("img=" + imgURL.replace("data:image/png;", '').replace('+', '$'));


};*/


// Context for the canvas for 2 dimensional operations 
const ctx = canvas.getContext('2d');

// Resizes the canvas to the available size of the window. 
function resize() {
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
}

// Stores the initial position of the cursor 
let coord = { x: 0, y: 0 };

// This is the flag that we are going to use to  
// trigger drawing 
let paint = false;

// Updates the coordianates of the cursor when  
// an event e is triggered to the coordinates where  
// the said event is triggered. 
function getPosition(event) {
    coord.x = event.clientX - canvas.offsetLeft;
    coord.y = event.clientY - canvas.offsetTop;
}

// The following functions toggle the flag to start 
// and stop drawing 
function startPainting(event) {
    paint = true;
    getPosition(event);

}

function stopPainting() {
    paint = false;
    var imgURL = canvas.toDataURL();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("url").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/main/detect", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("img=" + imgURL.replace("data:image/png;", '').replace('+', '$'));
}



function sketch(event) {
    if (!paint) return;
    console.log(mode)

    if (mode == "pen") {

        ctx.lineWidth = 2;
        // Sets the end of the lines drawn 
        // to a round shape. 
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'skyblue';

        // The cursor to start drawing 
        // moves to this coordinate 
        ctx.moveTo(coord.x, coord.y);

        // The position of the cursor 
        // gets updated as we move the 
        // mouse around. 
        getPosition(event);

        // A line is traced from start 
        // coordinate to this coordinate 
        ctx.lineTo(coord.x, coord.y);

        // Draws the line. 
        ctx.stroke();
    } else {
        ctx.globalCompositeOperation = "destination-out";
        ctx.arc(lastX, lastY, 8, 0, Math.PI * 2, false);
        ctx.fill();
    }
}