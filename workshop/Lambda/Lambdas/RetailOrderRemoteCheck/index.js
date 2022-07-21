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


exports.handler = async (event) => {
    let data = {};
    let statuscode=200;
    let aproval= 'Aproved from cross-account Lambda!';
    const span = opentelemetry.trace.getSpan(opentelemetry.context.active());
    console.log("EVENT\n" + JSON.stringify(event, null, 2));
    if (event){
        try {
            data = JSON.parse(JSON.stringify(event, null, 2));
        } catch (e) {
            return {
                statusCode: 400,
                body: JSON.stringify({message: 'There was an error parsing the JSON data posted to this endpoint', error:e})
            };
        }
    }
    console.log("Data recieved: " + JSON.stringify(data));
    var  phoneType = data.ProductName;
    console.log("phone: " + phoneType);
    if (phoneType == "Test Phone") {
        span.recordException(Error ("Disaproved - Needs Senior Managment to aprove"));
        span.setStatus({ code: opentelemetry.SpanStatusCode.ERROR });
        statuscode = 418;
        aproval = "Disaproved - Needs Senior Managment to aprove";
    }
    const response = {
        'statusCode' : statuscode,
        'aproval'    : aproval
    };
    console.log ("response: "+ JSON.stringify((response)));
    return response; 
};