var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading
 
/*********SETTINGS*********************/
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/605.1';
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
 
	//Step 1 - Open home page
    function(){
        console.log('Step 1 - Open home page');
        page.open("http://localhost:8080/Supercar-Trader/home.do", function(status){
			
		});
    },
	//Step 2 - Get a screenshot
    function(){
		console.log("Step 2 - Get a screen capture");
		page.render('session-09.png');
    },
    //Step 3 - Get a second screenshot
    function(){
		console.log("Step 3 - Get a second screen capture");
		page.render('session-09.png');
    },


    //Step 4 - Open inventory page
    function(){
        console.log('Step 4 - Open inventory page');
        page.open("http://localhost:8080/Supercar-Trader/supercars.do", function(status){
            
        });
    },
    //Step 5 - Get a screenshot
    function(){
        console.log("Step 5 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 6 - Get a second screenshot
    function(){
        console.log("Step 6 - Get a second screen capture");
        page.render('session-09.png');
    },


    //Step 7 - Open Aston Martins page
    function(){
        console.log('Step 7 - Open Aston Martins page');
        page.open("http://localhost:8080/Supercar-Trader/cars.do?query=manu&mid=3", function(status){
            
        });
    },
    //Step 8 - Get a screenshot
    function(){
        console.log("Step 8 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 9 - Get a second screenshot
    function(){
        console.log("Step 9 - Get a second screen capture");
        page.render('session-09.png');
    },


    //Step 10 - Open BMWs page
    function(){
        console.log('Step 10 - Open BMWs page');
        page.open("http://localhost:8080/Supercar-Trader/cars.do?query=manu&mid=4", function(status){
            
        });
    },
    //Step 11 - Get a screenshot
    function(){
        console.log("Step 11 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 12 - Get a second screenshot
    function(){
        console.log("Step 12 - Get a second screen capture");
        page.render('session-09.png');
    },


    //Step 13 - Open Ferraris page
    function(){
        console.log('Step 13 - Open Ferraris page');
        page.open("http://localhost:8080/Supercar-Trader/cars.do?query=manu&mid=2", function(status){
            
        });
    },
    //Step 14 - Get a screenshot
    function(){
        console.log("Step 14 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 15 - Get a second screenshot
    function(){
        console.log("Step 15 - Get a second screen capture");
        page.render('session-09.png');
    },



    //Step 16 - Open Ferrari Pista page
    function(){
        console.log('Step 16 - Open Ferrari Pista page');
        page.open("http://localhost:8080/Supercar-Trader/car.do?query=car&cid=4", function(status){
            
        });
    },
    //Step 17 - Get a screenshot
    function(){
        console.log("Step 17 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 18 - Get a second screenshot
    function(){
        console.log("Step 18 - Get a second screen capture");
        page.render('session-09.png');
    },





    //Step 22 - Open Sell page
    function(){
        console.log('Step 22 - Open Sell page');
        page.open("http://localhost:8080/Supercar-Trader/sell.do", function(status){
            
        });
    },
    //Step 23 - Get a screenshot
    function(){
        console.log("Step 23 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 24 - Get a second screenshot
    function(){
        console.log("Step 24 - Get a second screen capture");
        page.render('session-09.png');
    },



    //Step 25 - Open Insurance page
    function(){
        console.log('Step 25 - Open Insurance page');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do", function(status){
            
        });
    },
    //Step 26 - Get a screenshot
    function(){
        console.log("Step 26 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 27 - Get a second screenshot
    function(){
        console.log("Step 27 - Get a second screen capture");
        page.render('session-09.png');
    },



    //Step 28 - Open Enquire page
    function(){
        console.log('Step 28 - Open Enquire page');
        page.open("http://localhost:8080/Supercar-Trader/enquire.do", function(status){
            
        });
    },
    //Step 29 - Get a screenshot
    function(){
        console.log("Step 29 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 30 - Get a second screenshot
    function(){
        console.log("Step 30 - Get a second screen capture");
        page.render('session-09.png');
    },



    //Step 31 - Open Enquire page
    function(){
        console.log('Step 31 - Open Enquire page');
        page.open("http://localhost:8080/Supercar-Trader/enquire.do", function(status){
            
        });
    },
    //Step 32 - Get a screenshot
    function(){
        console.log("Step 32 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 33 - Get a second screenshot
    function(){
        console.log("Step 33 - Get a second screen capture");
        page.render('session-09.png');
    },



    //Step 34 - Open About page
    function(){
        console.log('Step 34 - Open About page');
        page.open("http://localhost:8080/Supercar-Trader/about.do", function(status){
            
        });
    },
    //Step 35 - Get a screenshot
    function(){
        console.log("Step 35 - Get a screen capture");
        page.render('session-09.png');
    },
    //Step 36 - Get a second screenshot
    function(){
        console.log("Step 36 - Get a second screen capture");
        page.render('session-09.png');
    },






];
/**********END STEPS THAT FANTOM SHOULD DO***********************/
 
//Execute steps one by one
interval = setInterval(executeRequestsStepByStep,12000);
 
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