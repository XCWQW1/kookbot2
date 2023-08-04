var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var appConfig = require("./appConfig")

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

// initialize the node server configuration with the appConfig.json file
Object.assign(process.env, appConfig)

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

module.exports = app;
