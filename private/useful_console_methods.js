// USEFUL CONSOLE METHODS



// run a cloud code function
curl -X POST \
  -H "X-Parse-Application-Id: AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ" \
  -H "X-Parse-REST-API-Key: i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS" \
  -H "X-Parse-Master-Key: LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv" \
  -H "Content-Type: application/json" \
  -d '{}' \
  https://api.parse.com/1/functions/copy_to_Firebase


// add a user to a role's user relations list (give user that role)
curl -X PUT \
  -H "X-Parse-Application-Id: AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ" \
  -H "X-Parse-REST-API-Key: i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS" \
  -H "X-Parse-Master-Key: LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv" \
  -H "Content-Type: application/json" \
  -d '{
        "users": {
          "__op": "AddRelation",
          "objects": [
            {
              "__type": "Pointer",
              "className": "_User",
              "objectId": "V5nGbG2rOS"
            }]
        }
      }' \
  https://api.parse.com/1/roles/eOl0Sb1OYH




// add sample data into Firebase

curl -X PUT -d '{
  "alanisawesome": {
    "name": "Alan Turing",
    "birthday": "June 23, 1912"
  }
}' 'https://burning-fire-8681.firebaseio.com/BLARGH.json'








// test connecting to a CloudCode Webhook function defined in server.js
curl -X POST \
  -H "X-Parse-Application-Id: AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ" \
  -H "X-Parse-REST-API-Key: i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS" \
  -H "X-Parse-Master-Key: LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv" \
  -H "Content-Type: application/json" \
  -d '' \
  https://api.parse.com/1/functions/test_connecting_to_heroku












































