var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading
 
/*********SETTINGS*********************/
var webPage = require('webpage');
var page = webPage.create();

page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/74.0';
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
 
	//Step 1 - Open search page
    function(){
        console.log('Step 1 - Open search page');
        page.open("http://localhost:8080/Supercar-Trader/search.do", function(status){
			
		});
    },
	//Step 2 - Click on the Sign in button
	//function(){
        //console.log('Step 2 - Click on the Sign in button');
		//page.evaluate(function(){
			//document.getElementById("nav-link-yourAccount").click();
		//});
    //},
	//Step 3 - Populate and submit the login form
    function(){
        console.log('Step 2 - Populate and submit the search form');
		page.evaluate(function(){
			document.getElementById("criteria").value="A";
            document.getElementById("searchForm").submit();
		});


    },
	//Step 4 - Wait Amazon to login user. After user is successfully logged in, user is redirected to home page. Content of the home page is saved to AmazonLoggedIn.html. You can find this file where phantomjs.exe file is. You can open this file using Chrome to ensure that you are logged in.
    function(){
		console.log("Step 3 - Get a screen capture");
		page.render('search.png');
    },

    function(){
		console.log("Step 4 - Get a second screen capture");
		page.render('search.png');
    },

    //function(){
		//console.log("Step 4 - Wait Amazon to login user. After user is successfully logged in, user is redirected to home page. Content of the home page is saved to AmazonLoggedIn.html. You can find this file where phantomjs.exe file is. You can open this file using Chrome to ensure that you are logged in.");
         //var fs = require('fs');
		 //var result = page.evaluate(function() {
			//return document.querySelectorAll("html")[0].outerHTML;
		//});
        //fs.write('AmazonLoggedIn.html',result,'w');
    //},

];
/**********END STEPS THAT FANTOM SHOULD DO***********************/
 
//Execute steps one by one
interval = setInterval(executeRequestsStepByStep,6000);
 
function executeRequestsStepByStep(){
    if (loadInProgress == false && typeof steps[testindex] == "function") {
        //console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex++;
    }
    if (typeof steps[testindex] != "function") {
        console.log("test complete!");
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