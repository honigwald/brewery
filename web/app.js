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
            console.log(file);
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


    var jsonObj2 = JSON.stringify(req.body);
    fs.writeFile("recipes/" + req.body.recipeName , jsonObj2 , function(err) {
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
        exec('python brew.pyv ' + req.body.selectRecipe);

        res.redirect('/index');
});



module.exports = app;
