'use strict ';
const https = require('https');
const opentelemetry = require('@opentelemetry/api');

var log = console.log;

console.log = function(){
     const span = opentelemetry.trace.getSpan(opentelemetry.context.active());
     var ctx = span.spanContext();
     var o11yresource = process.env.OTEL_RESOURCE_ATTRIBUTES; 
     var o11yfind ="deployment.environment=";
     var o11yenv = o11yresource.slice(o11yresource.indexOf(o11yfind) + o11yfind.length);
     var o11yLogline = JSON.stringify("{trace_id: " + ctx.traceId + " span_id: " + ctx.spanId + " service.name: " + process.env.OTEL_SERVICE_NAME + " deployment.environment: " + o11yenv + "}");
    // 1. Convert args to a normal array
    var args = Array.from(arguments);
 
    // 2. Prepend log prefix log string
    args.unshift(o11yLogline );
    // 3. Pass along arguments to console.log
    log.apply(console, args);
};
// function to handle callback from HTTP call in Node JS
async function getDiscount(options) {
    return new Promise((resolve, reject) => {
        let body = "";
 //
        const req = https.get("https://e64fva75mh.execute-api.eu-west-1.amazonaws.com/default/RetailorderDiscount", function(res) {
            console.log('statusCode: ' + res.statusCode);
            res.on('data', chunk => {
                body += chunk;
                console.log("body: "+ body);
            });
            res.on('error', error => {
                console.error(error);
                // If failed
                reject(error);
            });
            res.on('end', () => {
                resolve(JSON.parse(body).Discount);
        });
    
        });
    });
}

exports.handler = async function(event, context) {
    try {
        console.log("EVENT\n" + JSON.stringify(event, null, 2));
        //  Setting Price hardcoded .. could fetch it from DataBase if required
        var price = 499;

        /// Set option for an other HTTPS call to a LAMBDA
        var discount_URL = process.env.DISCOUNT_URL;
        console.log("Dicount URL\n" + discount_URL)
        var discount = 0; // No discount unless call returns it
        // const options = {
        //     hostname:  discount_Hostname,
        //     port: 443,
        //     path: discount_Path,
        //     method: 'GET'
        // };

        //Fetch discount
        discount = await getDiscount(discount_URL);
        
        // calc new price and send it back    
        var totalPrice = price - discount;
        var response = {
            statusCode: 200,
            body: JSON.stringify({'Price':totalPrice})
        };
        return response;
    }
    catch (err) {
        console.error(err);
    }
};
