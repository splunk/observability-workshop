var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading
 
/*********SETTINGS*********************/
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/74.0';
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

    //Step 1 - Open Insurance page start memory leak
    function(){
        console.log('Step 1 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=20000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 2 - Open Insurance page start memory leak
    function(){
        console.log('Step 2 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=20000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 3 - Open Insurance page start memory leak
    function(){
        console.log('Step 3 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=20000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 4 - Open Insurance page start memory leak
    function(){
        console.log('Step 4 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 5 - Open Insurance page start memory leak
    function(){
        console.log('Step 5 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 6 - Open Insurance page start memory leak
    function(){
        console.log('Step 6 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 7 - Open Insurance page start memory leak
    function(){
        console.log('Step 7 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 8 - Open Insurance page start memory leak
    function(){
        console.log('Step 8 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 9 - Open Insurance page start memory leak
    function(){
        console.log('Step 9 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 10 - Open Insurance page start memory leak
    function(){
        console.log('Step 10 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },


    //Step 11 - Open Insurance page start memory leak
    function(){
        console.log('Step 11 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=2000", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },



    //Step 12 - Open Insurance page start memory leak
    function(){
        console.log('Step 12 - Open Insurance page with memory leak');
        page.open("http://localhost:8080/Supercar-Trader/insurance.do?heapLeak=0", function(status){
        });
    },    
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
    },
    function(){
        console.log("Get a screen capture");
        page.render('mem-leak-01.png');
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