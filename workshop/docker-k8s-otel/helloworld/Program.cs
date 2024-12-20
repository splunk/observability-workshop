using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

string Hello([FromServices]ILogger<Program> logger, string? name)
{
    string result;

    if (string.IsNullOrEmpty(name))
    {
       logger.LogInformation("/hello endpoint invoked anonymously");
       result = "Hello, World!";
    }
    else
    {
        logger.LogInformation("/hello endpoint invoked by {name}", name);
        result = String.Format("Hello, {0}!", name);
    }

    return result;
}

app.MapGet("/hello/{name?}", Hello);

app.Run();
