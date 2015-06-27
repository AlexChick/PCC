
Parse.initialize("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "eyHtd5bpdJufw1JDinRBMNnFx2poEGJETHxAnzuV")

// var Firebase = require("firebase.js");


// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:
Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello world!");
});


Parse.Cloud.define("Logger", function(request, response) {
  console.log(request.params);
  response.success();
});



Parse.Cloud.define("makeTestEventObject", function(request, response) {
    // Set up to modify user data
    Parse.Cloud.httpRequest({
        url: 'https://daeious-ex-machina.herokuapp.com/',
        success: function(httpResponse) {
            console.log(httpResponse.text);
            response.success("Test Event Object created successfully in Parse.");
        },
        error: function(httpResponse) {
            console.error('Request failed with response code ' + httpResponse.response);
            response.success("Oops.... something went wrong.");
        }
    })
});

function gotData(data) {
    console.log(data);
}

Parse.Cloud.define("print_from_Firebase", function(request, response) {
    // Grab a simple data member from Firebase to show it can be done.
    // For some reason, "PATCH" doesn't work, so we have to manually override "POST".
    var str_body = "";
    if (request.params.di_data) {str_body = request.params.di_data}

    // var str_url = "https://burning-fire-8681.firebaseio.com/";
    // var di_levels = request.params.di_levels;
    // for (var level in di_levels) {
    //     str_url += di_levels[level];
    // }
    // str_url += ".json?x-http-method-override=PATCH";

    if (request.params.level_1 != null) {var level_1 = request.params.level_1}
    if (request.params.level_2 != null) {var level_2 = request.params.level_2}
    if (request.params.level_3 != null) {var level_3 = request.params.level_3}
    var url_root = "https://burning-fire-8681.firebaseio.com/";
    var str_url = url_root + level_1 + level_2 + level_3 + ".json?x-http-method-override=PATCH&callback=gotData";

    Parse.Cloud.httpRequest({
        method: "POST",
        url: str_url,
        body: str_body,
        success: function(httpResponse) {
            response.success(httpResponse.text); // {"result":"\"True\""}
        },
        error: function(error) {
            response.error(error);
        }
    })
})





// Parse.Cloud.define("copy_Parse_class_into_Firebase", function(request, response) {
//     // Copy all objects in a given classname in Parse to Firebase.

//     var query = new Parse.Query("Question");
//     query.limit(1000);
//     query.find({
//         success: function(results) {
//             response.success("Success -- " + results.length + " Questions were found in Parse");
//         },
//         error: function() {
//             response.error("Question lookup failed");
//         }
//     });
//     console.log("does this print?");

// });


// function query_all(classname, callback) {
//     // here you can perform a Parse.Query,
//     // then call callback.success from within
//     // its success block, or callback.error if
//     // it fails
//     var cn = classname;
//     var query = new Parse.Query(cn).limit(1000);
//     query.find({
//         success: function(results) {
//             callback.success("Success: " + results.length + " " + cn + "s were found in Parse");
//         },
//         error: function() {
//             callback.error("Error: " + classname_to_query + " lookup failed");
//         }
//     });
// };


// Log in, then do several asynchronous tasks.
Parse.Cloud.define("copy_to_Firebase", function (request, response) {
    //  (0) Log in.
    Parse.User.logIn("alex", "1234").then(function(user) {
    //  (1) Query Parse for "Question" class.
        var query = new Parse.Query("Question").limit(1000);
        var promise = query.find();
        return promise; // This works just as well as > return query.find();
    }).then(function(results) {
    //  (2) Query Parse for "Answer" class.
        var query = new Parse.Query("Answer").limit(1000);
        return query.find();
    }).then(function(results) {
    //  (3) Query Parse for "IPad" class.
        var query = new Parse.Query("IPad").limit(1000);
        return query.find();
    }).then(function(results) {
    //  (4) Connect to Firebase, just to show it can be done.
        return Parse.Cloud.httpRequest({
            url: "https://burning-fire-8681.firebaseio.com/Event.json"
        });
    }).then(function(results) {
    //  (5) Run a simple Python script (hosted on Heroku) that creates an empty "Event" object in Parse.
        return Parse.Cloud.httpRequest({
            url: "https://daeious-ex-machina.herokuapp.com/"
        });
    }).then(function(results) {
    //  (6) Run another PCC function defined here somewhere.
        return Parse.Cloud.run("makeTestEventObject");
    }).then(function(results) {
    //  (7) Run another PCC function to show we can get print data from Firebase.
        return Parse.Cloud.run("print_from_Firebase", {
            level_1: "Employee",
            level_2: "Employee_00001",
            level_3: "object_id"
        });
    }).then(function(results) {
        // response.success("All asynchronous tasks completed successfully!");
        console.log(results);
        response.success(results);
    }, function(error) {
        response.error(error);
    });
});

    // Parse.Cloud.httpRequest({
    //     url: 'https://daeious-ex-machina.herokuapp.com/',
    //     success: function(httpResponse) {
    //         console.log(httpResponse.text);
    //         response.success("Test Event Object created successfully in Parse.");
    //     },
    //     error: function(httpResponse) {
    //         console.error('Request failed with response code ' + httpResponse.response);
    //         response.success("Oops.... something went wrong.");
    //     }
    // })








































