/**
 *
 * This script will go through the history of a slack channel and count up the total number of messages sent by
 * each user in any given channel.  NOTE: The maximum number of messages that can be counted is 1000.
 *
 * Use --help for usage information
 *
 * Resources:
 *     https://slack.dev/node-slack-sdk/
 *     https://api.slack.com/methods
 *
 * TODO: Move code into functions so that count_messages.js can be included in app.js
 * TODO: If no bot token is provided, start up a temporary http server to allow the user to auth with slack (OAuth 2.0) and use that token instead.
 */

const { WebClient } = require("@slack/web-api");

let argv = require("yargs")
    .option("token", {
        alias: "t",
        description: "The access token used to retrieve messages",
        demandOption: true,
        type: "string"
    })
    .option("from", {
        description: "The earliest message to receive",
        type: "string"
    })
    .option("to", {
        description: "The latest message to receive",
        type: "string"
    })
    .argv;

const slack = new WebClient(argv.token);

let users = {};
let channels = {};
let messages = {};

// Wait for all asynchronous ajax requests to complete
Promise.all([
    slack.users.list().then(function(result){
        result["members"].forEach(function(user){
            users[user["id"]] = user["real_name"];
        });
    }),
    slack.conversations.list().then(function(result){

        // requests is a list of promises that need to be complete before moving on
        let requests = [];
        result["channels"].forEach(function(channel){
            channels[channel["id"]] = channel["name"];

            let options = {
                channel: channel["id"],
                count: 1000 // Default is only 100, but max is 1000
            };
            // Slack's timestamps are milliseconds from the unix epoch.
            if(argv.from) options["oldest"] = new Date(argv.from).getTime() / 1000;
            if(argv.to) options["latest"] = new Date(argv.to).getTime() / 1000;

            // Add the promise to requests so that we can wait for them all to complete
            requests.push(slack.channels.history(options).then(function(result){
                messages[channel["id"]] = result["messages"];
            }));
        });

        // Returning a promise will require that promise to be resolved for the outer one to be resolved.
        // Basically, this waits for all channel history calls to complete before moving onto the final
        // then block at the bottom.
        return Promise.all(requests);
    }, function(err, e){
        console.log(err, e)
    })
]).then(function(){
    // All information is collected, add up the messages and print them out in a human readable format
    for(let channel in messages){

        let count = {};
        messages[channel].forEach(function(message){
            let user = message["user"];

            if(!count[user]) count[user] = 0;
            count[user]++;
        });

        console.log(channels[channel] + ":");
        for(let user in count){
            console.log("\t" + users[user] + ": " + count[user]);
        }
    }
});