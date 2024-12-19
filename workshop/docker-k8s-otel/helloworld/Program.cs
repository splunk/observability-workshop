using System.Globalization;

using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

string Hello([FromServices]ILogger<Program> logger, string? name)
{
    if (string.IsNullOrEmpty(name))
    {
        logger.LogInformation("Hello, World!);
    }
    else
    {
        logger.LogInformation("Hello, {result}!", name);
    }

    return result.ToString(CultureInfo.InvariantCulture);
}

app.MapGet("/hello/{name?}", Hello);

app.Run();
