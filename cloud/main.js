
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
// yep