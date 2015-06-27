
# Run a Parse Cloud Code function.

import json,httplib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/functions/print_from_Firebase', json.dumps({

        # "di_levels": 
        # 			"{ \"level_1\": \"Employee/\", \
				    #    \"level_2\": \"Employee_00001/\", \
				    #    \"level_3\": \"woo/\" \
			     #    }",

		"level_1": "Employee/",
        "level_2": "Employee_00001/",
        "level_3": "woo/",

        "di_data": 
        			"{ \"keyp\": \"value\" \
        			}"

     }), {
       "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
       "X-Parse-REST-API-Key": "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS",
       "Content-Type": "application/json"
     })
result = json.loads(connection.getresponse().read())
print result