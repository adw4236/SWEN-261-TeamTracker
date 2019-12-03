/**
 * NOTE: app.js is not implemented and is here purely as a skeleton in case
 * it is to be implemented in the future.  This provides a graphical outlet
 * to interpret data.
 *
 * The high level goal here is to provide charts to show team activity like
 * git does for commits, but for Trello and Slack instead, but that will require
 * a lot of work.
 */

const express = require("express");
const { createEventAdapter } = require("@slack/events-api");

let argv = require("yargs")
    .option("port", {
        alias: "p",
        description: "The port to run the web server on",
        default: "3000",
        type: "number"
    })
    .option("secret", {
        alias: "s",
        description: "The slack signing secret for verification",
        demandOption: true,
        type: "string"
    })
    .argv;

const app = express();
const slackEvents = createEventAdapter(argv.secret);

app.use("/slack/events", slackEvents.requestListener());

app.get("/", (req, res) => {
    // This is the home page of the web app
    res.send("Hello World!")
});

// Slack events can be handled like this, or any other part of the slack API can be used
slackEvents.on("message", (event) => {
    console.log(JSON.stringify(event, null, 2));
});

// Start the web app
app.listen(argv.port, () => console.log(`Server started at localhost:${argv.port}`));