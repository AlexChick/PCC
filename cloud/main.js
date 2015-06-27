
Parse.initialize("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "eyHtd5bpdJufw1JDinRBMNnFx2poEGJETHxAnzuV")


// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:
Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello world!");
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

// Parse.Cloud.run("copy_Parse_class_into_Firebase", {}, {});



function query_all(classname_to_query, callback) {
    // here you can perform a Parse.Query,
    // then call callback.success from within
    // its success block, or callback.error if
    // it fails

    // ...

    var query = new Parse.Query(classname_to_query);
    query.limit(1000);
    query.find({
        success: function(results) {
            // callback.success(results.length);
            var a = "Success: " + results.length + " " + classname_to_query + "s were found in Parse";
            callback.success(a);
        },
        error: function() {
            callback.error("Error: " + classname_to_query + " lookup failed");
        }
    });
}


Parse.Cloud.define("copy_to_Firebase", function (request, response) {
    query_all("Answer", {
        success: function(request) {
            response.success(request);
        },
        error: function(error) {
            response.error(error);
        }
    });
})










































