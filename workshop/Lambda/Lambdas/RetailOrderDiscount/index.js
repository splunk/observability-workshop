'strict';
const opentelemetry = require('@opentelemetry/api');

var log = console.log;

console.log = function(){
     const span = opentelemetry.trace.getSpan(opentelemetry.context.active());
     var ctx = span.spanContext();
     var o11yresource = process.env.OTEL_RESOURCE_ATTRIBUTES; 
     var o11yfind ="deployment.environment=";
     var o11yenv = o11yresource.slice(o11yresource.indexOf(o11yfind) + o11yfind.length);
     var o11yLogline = JSON.stringify({'trace_id': ctx.traceId,
                                        'span_id': ctx.spanId,
                                        'service.name': process.env.OTEL_SERVICE_NAME,
                                        'deployment.environment': o11yenv
                                        });
    // 1. Convert args to a normal array
    var args = Array.from(arguments);
 
    // 2. Prepend log prefix log string
    args.unshift(o11yLogline );
    // 3. Pass along arguments to console.log
    log.apply(console, args);
};



exports.handler = async (event,contecxt,callback) => {
    try {
        console.log("EVENT\n" + JSON.stringify(event, null, 2))
        var response= {}; 
        var discount= 99; // hardcoded.. could come from DB
        response = {
            statusCode: 200,
             body:JSON.stringify({'Discount': discount})
        };
        return response;
    }
    catch (err) {
        console.error(err);
    } 
};
