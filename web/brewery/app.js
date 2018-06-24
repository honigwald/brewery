var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser');

const fs = require('fs');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser());

app.use('/', indexRouter);
app.use('/users', usersRouter);

var recipeList = [];
//app.get("/", (req, res) => { res.render("recipe", { recName: req.body.recipeName }); });
app.get('/', function (req, res) {

    fs.readdir('recipes/', (err, files) => {
        files.forEach(file => {
            console.log(file);
            recipeList.add(file);
            //res.render("index", { recName: req.body.recipeName });
            /*var obj = JSON.parse(file);
            var keys = Object.keys(obj);
            for (var i = 0; i < keys.length; i++) {
                console.log(obj[keys[i]]);
            }*/
            //res.send(req.body.recipeName);

        });
    });
});

app.post('/addRecipe', function(req, res) {


    //var obj = { step1 :{name : req.body.schritt1Name, temp : req.body.schritt1Temp, time : req.body.schritt1Zeit}, step2: {name : req.body.schritt2Name, temp : req.body.schritt2Temp, time : req.body.schritt2Zeit}};
    //obj.step3 = {name : req.body.schritt3Name, temp : req.body.schritt3Temp, time : req.body.schritt3Zeit};
    //var jsonObj = JSON.stringify(obj);


    var jsonObj2 = JSON.stringify(req.body);
    fs.writeFile("recipes/" + req.body.recipeName + ".txt", jsonObj2 , function(err) {
        if(err) {
            res.send(err);
        }
        else {


            res.redirect('/recipe.html');
        }
        console.log("The file was saved!");

    });


});



module.exports = app;
