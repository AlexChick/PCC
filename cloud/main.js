
Parse.initialize("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "eyHtd5bpdJufw1JDinRBMNnFx2poEGJETHxAnzuV")

// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:
Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello world!");
});

// Not sure how to use this.
Parse.Cloud.define("Logger", function(request, response) {
  console.log(request.params);
  response.success();
});

// Connect to Heroku app, which runs a Python script that creates a test Event object.
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

Parse.Cloud.define("test_connecting_to_heroku", function (request, response) {
    Parse.Cloud.httpRequest({
            url: "https://daeious-dev.herokuapp.com/",
        success: function(httpResponse) {
            response.success(httpResponse.text); // {"result":"\"True\""}
        },
        error: function(error) {
            response.error(error);
        }
    })
});







///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// copy_from_Parse_to_Firebase
// request.params:
//          <e_serial>, the serial of this Event. (Ex: "000024")
//          <classname>, a string of the Parse class for which we want to copy data into Firebase. (Ex: "Question")
// (0) Log in.
// (1) query_from_Parse(classname).
// (2) convert_Parse_data_to_Firebase_data()
// (2) update_in_Firebase(url, body).
Parse.Cloud.define("copy_from_Parse_to_Firebase", function (request, response) {
    // (0) Log in.
    Parse.User.logIn("alex", "1234"
    ).then( function (user) {
        // (1) Query from Parse.
        return Parse.Cloud.run("query_from_Parse", { 
            classname : request.params.classname
        });
    }).then( function (results) {
        // (2) Update in Firebase.
        var di_object_dicts = {};
        for (var i = 0; i < results.length; i++) {
            var dict = {};
            var li_attr = results[i].get("li_attr");
            for (var j = 0; j < li_attr.length; j++) {
                dict[li_attr[j]] = results[i].get(li_attr[j]);
            }
            // dict["num"] = results[i].get("num");
            // dict["serial"] = results[i].get("serial");
            // dict["ID"] = results[i].get("ID");
            di_object_dicts[dict["ID"]] = dict;
        };

        str_di_object_dicts = JSON.stringify(di_object_dicts);

        return Parse.Cloud.run("update_in_Firebase", {
            e_serial : request.params.e_serial,
            classname : request.params.classname,
            str_didi : str_di_object_dicts
        });
    }).then( function (results) {
        // (-1) Return.
        response.success(results);
    }, function (error) {
        response.error(error);
    });
});

// query_from_Parse
Parse.Cloud.define("query_from_Parse", function (request, response) {
    // Return a list of one dictionary for each Parse <classname> object, sorted by "num".
    // request.params: 
    //          <classname>, a string of the class to query from. Ex: "Question"
    // response.success: 
    //          <results>, a sorted list of dictionaries of Parse object attributes and values. Ex: [{},{},{}]
    // FIX: Only gets first 1000 objects.
    var query = new Parse.Query(request.params.classname).limit(1000).ascending("num");
    query.find({
        success: function (results) {
            response.success(results);
        }, error: function (error) {
            response.error(error);
        }
    });
});

// update_in_Firebase
Parse.Cloud.define("update_in_Firebase", function (request, response) {
    // Return a message stating that everything was updated in Firebase.
    // request.params:
    //      <e_serial>, a string representing the data path to PATCH to. Ex: "https://burning-fire-8681.firebaseio.com/Event/Event_000001/Question"
    //      <classname>, a string of the class to update in Firebase. Ex: "Question"
    //      <body>, a dictionary of all data to update in Firebase. Ex: { "num": 1, ID: "Question_000001"} (quotes around keys are optional)
    var e_serial = request.params.e_serial;
    var classname = request.params.classname;
    var str_didi = request.params.str_didi;

    var url = "https://burning-fire-8681.firebaseio.com/";
    if (classname.match("Question|IPad|EventUser|Config")) { // Should all classes be included in Event/Event_000001/ ?
        url += "Event/Event_" + e_serial + "/" + classname + "/";
    } else if (classname.match("User|Answer|Employee")) {
        url += classname + "/";
    }
    url += ".json?x-http-method-override=PATCH";

    Parse.Cloud.httpRequest({
        method: "POST",
        url: url,
        body: str_didi,
        success: function(httpResponse) {
            response.success(httpResponse.text); // {"result":"\"True\""}
        }, error: function(error) {
            response.error(error);
        }
    });    
});

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



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


















////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////


/*

button_tapped
    setup_event
    check_in
        create_a_daeious_account
        register_for_this_event
        arrive_at_this_event
    start_event
    practice
        make_practice
        start_practice
        end_practice
    make_round
        make_r1
        make_r2
        make_r3
    start_round
        start_r1
        start_r2
        start_r3
    end_round
        end_r1
        end_r2
        end_r3
    end_event
    teardown_event

check_params

*/


function button_tapped (params) {

    // params MUST include reason, event_num
    if (!params_are_valid(f_name = "button_tapped", f_params = params)) {
        return false;
    } else {
        console.log("Button in Config App was tapped with valid params: " + params);
    }

    // set vars from <params>
    var reason = params.reason;
    var event_num = params.event_num;

    // use a switch on <reason> to call the desired function
    switch (reason) {

        case "setup_event":                             // 1
            setup_event(event_num = event_num);
            break;

        case "create_a_daeious_account":                // 3
        case "register_for_this_event":                 // 4
        case "arrive_at_this_event":                    // 5
            check_in(command = reason);
            break;

        case "start_event":                             // 6
            start_event();
            break;

        case "make_practice":
        case "start_practice":                          // 7
        case "end_practice":                            // 8
            practice(command = reason.split('_')[0]);
            break;

        case "make_r1":                                 // 9
        case "make_r2":                                 // 10
        case "make_r3":                                 // 11
            make_round(r_num = +reason.slice(-1));
            break;

        case "start_r1":                                // 12
        case "start_r2":                                // 13
        case "start_r3":                                // 14
            start_round(r_num = +reason.slice(-1));
            break;

        case "end_r1":                                  // 15
        case "end_r2":                                  // 16
        case "end_r3":                                  // 17
            end_round(r_num = +reason.slice(-1));
            break;

        case "end_event":                               // 18
            end_event();
            break;

        case "teardown_event":                          // 19
            teardown_event();
            break;

        default:
            break;
    }
    return true;
}

function check_params (params) {
    if (params == null) {
        console.log("ERROR: <params> not provided or doesn't exist");
        return false;
    }
    if (params.function_name == null) {
        console.log("ERROR: <function_name> not provided or doesn't exist");
        return false;
    }
    switch (params.function_name) {


        /* JavaScript Functions */

        case "setup_event":
            // check params; return false if incorrect
            break;

        case "check_in":
            // check params; return false if incorrect
            break;

        case "create_a_daeious_account":
            // check params; return false if incorrect
            break;

        case "register_for_this_event":
            // check params; return false if incorrect
            break;

        case "arrive_at_this_event":
            // check params; return false if incorrect
            break;

        case "start_event":
            // check params; return false if incorrect
            break;

        case "practice":
            // check params; return false if incorrect
            break;

        case "make_practice":
            // check params; return false if incorrect
            break;        

        case "start_practice":
            // check params; return false if incorrect
            break;

        case "end_practice":
            // check params; return false if incorrect
            break;

        case "make_round":
            // check params; return false if incorrect
            break;

        case "make_r1":
        case "make_r2":
        case "make_r3":
            // check params; return false if incorrect
            break;

        case "start_round":
            // check params; return false if incorrect
            break;

        case "start_r1":
        case "start_r2":
        case "start_r3":
            // check params; return false if incorrect
            break;

        case "end_round":
            // check params; return false if incorrect
            break;

        case "end_r1":
        case "end_r2":
        case "end_r3":
            // check params; return false if incorrect
            break;

        case "end_event":
            // check params; return false if incorrect
            break;

        case "teardown_event":
            // check params; return false if incorrect
            break;


        /* Parse Cloud Code Functions */

        default:
            console.log("ERROR: Incorrect function_name provided");
            return false;
    }
}



////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/* 

1st-level Functions

setup_event
check_in
start_event
practice
make_round
start_round
end_round
end_event
teardown_event

*/

function setup_event (params) {
    return true;
}

function check_in (params) {
    if (params.command == "create_a_daeious_account") {
        create_a_daeious_account(params);
        register_for_this_event(params);
        arrive_at_this_event(params);
    } else if (params.command == "register_for_this_event") {
        register_for_this_event(params);
        arrive_at_this_event(params);
    } else if (params.command == "arrive_at_this_event") {
        arrive_at_this_event(params);
    }
    return true;
}

function start_event (params) {
    return true;
}

function practice (params) {
    return true;
}

function make_round (params) {
    return true;
}

function start_round (params) {
    return true;
}

function end_round (params) {
    return true;
}

function end_event (params) {
    return true;
}

function close_event (params) {
    return true;
}



////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/* 

2nd-level Functions

    create_a_daeious_account
    register_for_this_event
    arrive_at_this_event
    make_practice
    start_practice
    end_practice
    make_r1
    make_r2
    make_r3
    start_r1
    start_r2
    start_r3
    end_r1
    end_r2
    end_r3

*/

function create_a_daeious_account (params) {
    return true;
}

function register_for_this_event (params) {
    return true;
}

function arrive_at_this_event (params) {
    return true;
}

function make_practice (params) {
    return true;
}

function start_practice (params) {
    return true;
}

function end_practice (params) {
    return true;
}

function make_r1 (params) {
    return true;
}

function make_r2 (params) {
    return true;
}

function make_r3 (params) {
    return true;
}

function start_r1 (params) {
    return true;
}

function start_r2 (params) {
    return true;
}

function start_r3 (params) {
    return true;
}

function end_r1 (params) {
    return true;
}

function end_r2 (params) {
    return true;
}

function end_r3 (params) {
    return true;
}



////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/* 

Cloud Code Functions

*/









