const puppeteer = require('puppeteer');
function run () {
    return new Promise(async (resolve, reject) => {
        const browser = await puppeteer.launch({
            headless: true,
            defaultViewport: null
        });
        try {
            const wait_time = 1000;  //Set up delay between page interactions 
            for (let loop=0; loop < 1;loop++) {  // as part of the load we run multiple of this script to generate multiple session
                const context = await browser.createIncognitoBrowserContext();
                const page = await context.newPage();
                await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
                const urls= ["http://localhost:81/product/OLJCESPC7Z",
                            "http://localhost:81/product/9SIQT8TOJO",
                            "http://localhost:81/product/1YMWWN1N4O",
                            "http://localhost:81/product/LS4PSXUNUM"];
                for (let i=0; i < urls.length;i++) {
                   const url = urls[i];
                   await page.goto(`${url}`);
                   const text = await page.$eval('h2', element => element.textContent)
                   console.log('Product found in the shop: ' + text);
                   //add it to the cart
                   let inner_elements = await page.$x('//*[contains (text(), "Add to Cart")]');
                   await inner_elements[0].click();
                   await delay(wait_time );
               }
               // Grabbing the total price of the cart aas test
               let element = await page.waitForSelector('body > main > div > div > div.row.pt-2.my-3 > div > strong'); // select the element
               let spanValue = await element.evaluate(el => el.textContent); // grab the textContent from the element, by evaluating this function in the browser context
               console.log('Total Price: ' + spanValue);
               //page.setDefaultTimeout(0); // disable timeout for the following call
             
               const elements = await page.$x('//*[contains (text(), "Place order")]');
               await elements[0].click();
               console.log("- Checkout Clicked")
               element = await page.waitForSelector('body > main > div > div:nth-child(1) > div > div > p:nth-child(4) > strong'); // select the element
               //page.setDefaultTimeout(30000);
               spanValue = await element.evaluate(el => el.textContent); // grab the textContent from the element, by evaluating this function in the browser context
               console.log('order: ' + spanValue);
               await delay(wait_time);
               //Checking cookie, then deleting it
               console.log("cookies was")
               let before = await page.cookies()
               before.forEach(cookie => {
                  console.log("Before: ",cookie.name)
              })
              await page.deleteCookie({
                 name : "_splunk_rum_sid",
               })
               let after = await page.cookies()
               after.forEach(cookie => {
                  console.log("After: ",cookie.name)
              })
              await browser.close()
      }
        process.exit();
      } catch (e) {
        console.log (e)
      } finally {
        await browser.close();
      }
    })
}
run().then(console.log).catch(console.error);

function delay(time) {
   return new Promise(function(resolve) {
       setTimeout(resolve, time)
   });
}







