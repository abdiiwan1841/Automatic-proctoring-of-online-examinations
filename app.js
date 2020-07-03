let express=require('express');
let app=express();

let fs = require("fs");

let spawn = require("child_process").spawn;

app.use(express.static(__dirname + '/node_modules'));
app.use(express.static('public'));

let server = require('http').Server(app);  
let io = require('socket.io')(server);
exports.io = io;

app.get('/', function(req,res){
    res.sendFile(__dirname + "/index.html");
});

app.get('/training', function(req,res){
    res.sendFile(__dirname + "/training.html");
    
});
app.get('/exam', function(req,res){
    res.sendFile(__dirname + "/exam.html");
    
});

//////////////////////////////////
let index = 1;
let videoName,audioName;
io.on('connection', (client) => {  
    
    console.log('Client connected...');

    client.on('exam', (data) => {
        console.log(index);
        videoName= "media/exam/video" + index + ".avi";
        fs.writeFile(videoName, data["y"], 'base64', (err) => {
            if (err) throw err
            console.log('It\'s saved!');
        });
        //index += 1;

        //Call Python File
        //let process = spawn('python', ["./exam.py",index]);
    });

    client.on('training', (data) => {
        //index++;
        let base64Data = data["img"].replace(/^data:image\/jpeg;base64,/, "");
        imageName= "media/training/examinee_image" + ".jpeg";
        fs.writeFile(imageName, base64Data, 'base64', (err) => {
            if (err) throw err
            console.log('It\'s saved!');
        });

        //Call Python File
        let process = spawn('python', ["./training.py",index]);

    });
});

/////////////////////////////////
server.listen(3000, () => {
    console.log("server has started");
});