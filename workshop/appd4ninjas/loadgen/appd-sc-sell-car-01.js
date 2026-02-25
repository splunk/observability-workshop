var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading
 
/*********SETTINGS*********************/
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36';
page.settings.javascriptEnabled = true;
page.settings.loadImages = true;//Script is much faster with this field set to false
phantom.cookiesEnabled = true;
phantom.javascriptEnabled = true;
/*********SETTINGS END*****************/
 
console.log('All settings loaded, start with execution');
page.onConsoleMessage = function(msg) {
    console.log(msg);
};
/**********DEFINE STEPS THAT FANTOM SHOULD DO***********************/
steps = [
 

    //Step 01 - Open Sell page and POST new car to sell
    function(){
        console.log('Step 01 - Open Sell page');
        page.open("http://localhost:8080/Supercar-Trader/sell.do", function(status){
            
        });
    },
    function(){
        console.log('Step 01 - Populate and submit the sell form');
        page.evaluate(function(){
            document.getElementById("manufacturer").value="5";
            document.getElementById("carModel").value="Mercedes CLS 63 AMG";
            document.getElementById("carEngine").value="V8 Turbo";
            document.getElementById("carColor").value="Silver";
            document.getElementById("carYear").value="2017";
            document.getElementById("carPrice").value="88569";
            document.getElementById("carSummary").value="2017 Silver Mercedes-Benz CLS 63 AMG 7-Speed Automatic Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats";
            document.getElementById("carDetails").value=" Transmission: 7-Speed Automatic, Exterior Color: White, Interior Color: Black, Maximum Seating: 4 seats, Gas Mileage: 18 MPG City 24 MPG Highway, Engine: V8 Turbo, Drivetrain: RWD, Fuel Type: Gasoline";
            document.getElementById("sellForm").submit();
        });
    },
    //Get a screenshot
    function(){
        console.log("Step 01 - Get a screen capture");
        page.render('sell-car-01.png');
    },
    //Get a second screenshot
    function(){
        console.log("Step 01 - Get a second screen capture");
        page.render('sell-car-01.png');
    },





    //Step 02 - Open Sell page and POST new car to sell
    function(){
        console.log('Step 02 - Open Sell page');
        page.open("http://localhost:8080/Supercar-Trader/sell.do", function(status){
            
        });
    },
    function(){
        console.log('Step 02 - Populate and submit the sell form');
        page.evaluate(function(){
            document.getElementById("manufacturer").value="1";
            document.getElementById("carModel").value="Porsche 911";
            document.getElementById("carEngine").value="Flat 6 Turbo";
            document.getElementById("carColor").value="Black";
            document.getElementById("carYear").value="2011";
            document.getElementById("carPrice").value="75241";
            document.getElementById("carSummary").value="2011 Black Porsche Turbo 7-Speed Automatic Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats";
            document.getElementById("carDetails").value="Transmission: 7-Speed Automatic, Exterior Color: Black, Interior Color: Black, Maximum Seating: 2 seats, Gas Mileage: 18 MPG City 24 MPG Highway";
            document.getElementById("sellForm").submit();
        });
    },
    //Get a screenshot
    function(){
        console.log("Step 02 - Get a screen capture");
        page.render('sell-car-01.png');
    },
    //Get a second screenshot
    function(){
        console.log("Step 02 - Get a second screen capture");
        page.render('sell-car-01.png');
    },



];
/**********END STEPS THAT FANTOM SHOULD DO***********************/
 
//Execute steps one by one
interval = setInterval(executeRequestsStepByStep,100);
 
function executeRequestsStepByStep(){
    if (loadInProgress == false && typeof steps[testindex] == "function") {
        //console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex++;
    }
    if (typeof steps[testindex] != "function") {
        console.log("test complete!");
        page.close();
        phantom.exit();
    }
}
 
/**
 * These listeners are very important in order to phantom work properly. Using these listeners, we control loadInProgress marker which controls, weather a page is fully loaded.
 * Without this, we will get content of the page, even a page is not fully loaded.
 */
page.onLoadStarted = function() {
    loadInProgress = true;
    console.log('Loading started');
};

page.onLoadFinished = function() {
    loadInProgress = false;
    console.log('Loading finished');
};

page.onConsoleMessage = function(msg) {
    console.log(msg);
};