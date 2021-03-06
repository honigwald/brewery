var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser');

const fs = require('fs');

var app = express();

app.set('view engine', 'ejs');
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

//get all recipes indexpage
app.get('/index', function (req, res) {
    var recipeList = [];
    fs.readdir('recipes/', (err, files) => {
        files.forEach(file => {
            recipeList.push(file)
            console.log(file);
        });
        res.render('index', { files: recipeList });
    });

});

//get all recipes
app.get('/recipes', function (req, res) {
    var recipeList = [];
    fs.readdir('recipes/', (err, files) => {
        files.forEach(file => {
            recipeList.push(file)
            });
        res.render('recipes', { files: recipeList });
    });

});

//detail recipes
app.get('/recipe', function (req, res) {
    var contents = fs.readFileSync('recipes/' + req.query.name);
    var jsonContent = JSON.parse(contents);
    res.render('recipe', {data : jsonContent});

});


//create Recipe
app.post('/addRecipe', function(req, res) {

    var o = {
        recipe:"",
        Step:[]
    };
    var objObj = req.body;

    o.recipe = req.body.recipeName;
        Object.keys(objObj).forEach(function(key) {
            if(key.includes("Id")){
                let s = objObj[key];

                let sName = "schritt" + s+"Name";
                let sTemp = "schritt" + s+"Temp";
                let sZeit = "schritt" + s+"Zeit";
                console.log(sName);
                let obj = {
                    id: s,
                    name: objObj[sName],
                    target_temp: objObj[sTemp],
                    duration: objObj[sZeit]
                };
                o.Step.push(obj);
                };


        });

    fs.writeFile("recipes/" + req.body.recipeName , JSON.stringify(o) , function(err) {
        if(err) {
            res.send(err);
        }
        else {
            res.redirect('/recipes');
        }
        console.log("The file was saved!");
    });
});

//start Brewery
app.post('/start', function(req, res) {

    var exec = require('child_process').exec;
    exec('python ../brew.py ' + req.body.selectRecipe);

    res.redirect('/index');
});



module.exports = app;
