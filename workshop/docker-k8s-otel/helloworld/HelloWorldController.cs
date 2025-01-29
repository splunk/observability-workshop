using Microsoft.AspNetCore.Mvc;
using System.Net;

public class HelloWorldController : ControllerBase
{
    private ILogger<HelloWorldController> logger;

    public HelloWorldController(ILogger<HelloWorldController> logger)
    {
        this.logger = logger;
    }

    [HttpGet("/hello/{name?}")]
    public string Hello(string name)
    {
        if (string.IsNullOrEmpty(name))
        {
           logger.LogInformation("/hello endpoint invoked anonymously");
           return "Hello, World!";
        }
        else
        {
            logger.LogInformation("/hello endpoint invoked by {name}", name);
            return String.Format("Hello, {0}!", name);
        }
    }
}
