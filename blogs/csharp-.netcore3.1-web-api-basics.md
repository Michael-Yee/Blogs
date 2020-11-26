---
title: .NET Core 3.1 Web API basics
author: Michael Yee
published: True
---


# Overview

In this blog, I will explore the basics in creating a .NET Core 3.1 Web API.

# Getting started

Create an ASP.NET Core Web API project and run the solution.

You will see the following outputs:

Brower:
```Text
[{"date":"2020-11-27T11:00:16.7821494-05:00","temperatureC":-14,"temperatureF":7,"summary":"Mild"},{"date":"2020-11-28T11:00:16.7824709-05:00","temperatureC":22,"temperatureF":71,"summary":"Scorching"},{"date":"2020-11-29T11:00:16.7824733-05:00","temperatureC":-13,"temperatureF":9,"summary":"Bracing"},{"date":"2020-11-30T11:00:16.7824737-05:00","temperatureC":31,"temperatureF":87,"summary":"Cool"},{"date":"2020-12-01T11:00:16.7824741-05:00","temperatureC":-3,"temperatureF":27,"summary":"Mild"}]
```

Console:
```Text
info: Microsoft.Hosting.Lifetime[0]
      Now listening on: https://localhost:5001
info: Microsoft.Hosting.Lifetime[0]
      Now listening on: http://localhost:5000
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: C:\Users\Amphagory\source\repos\WebAPIBasics\WebAPIBasics
```

# What just happen?

To explain what just happened, we let's look at the sample controller class that came with the project template, Controllers/WeatherForecastController.cs:
```CSharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace WebAPIBasics.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IEnumerable<WeatherForecast> Get()
        {
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = rng.Next(-20, 55),
                Summary = Summaries[rng.Next(Summaries.Length)]
            })
            .ToArray();
        }
    }
}

```

The controller class and its method define the endpoint and its behavior. The [Route] and [HttpGet] attributes signals ASP.NET to route a HTTP GET method request from the path /weathterforecast to the Get() method.

All of the elements contained in Controllers/WeatherForecastController.cs are set up in Startup.cs:
```CSharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace WebAPIBasics
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
```

The ConfigureServices() method is where service registration occurs with the IServiceCollection. AddControllers() is the Web API middleware which will register all the controllers.

UseRouting() and UseEndpoints() are the key configuration elements that add to ASP.NET’s middleware pipeline decision points for routing (as defined by attributes like [Route("[controller]")] and [HttpGet] seen in the controller class).

# Making your own API

Right now, nothing will respond at the root of the application. We can fix this easily by adding a Controller that will respond to “/”. 

Add a DefaultController.cs to the Controllers directory with the following content:
```CSharp
using System;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace WebAPIBasics.Controllers
{
	[ApiController]
	[Route("")]
	public class DefaultController : ControllerBase
	{
		private readonly ILogger<DefaultController> _logger;

		public DefaultController(ILogger<DefaultController> logger)
		{
			_logger = logger;
		}

		[HttpGet]
		public object Get()
		{
			var responseObject = new
			{
				apiName = "WebAPIBasics"
			};

			// TODO: Log any failures
			return responseObject;
		}
	}
}
```

Change the launch URL setting within Properties/launchSettings.json from /weatherforecast to the application root and run the project. You should see {"apiName":"WebAPIBasics"} in your browser.

# Stay Healthy

Like most apis, we need a way to monitor its health.  This can be simply done by adding two lines of code as follows in Startup.cs:
```CSharp
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.Extensions.Hosting;

namespace WebAPIBasics
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();
            services.AddHealthChecks();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthorization();

            app.UseHealthChecks("/health", new HealthCheckOptions {ResponseWriter = JsonResponseWriter});

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }

        private async Task JsonResponseWriter(HttpContext context, HealthReport report)
        {
            context.Response.ContentType = "application/json";
            await JsonSerializer.SerializeAsync(context.Response.Body, new {Status = report.Status.ToString()},
                new JsonSerializerOptions {PropertyNamingPolicy = JsonNamingPolicy.CamelCase});
        }
    }
}
```

Volia, our api will now respond to the /health endpoint. To add more interesting data to our repsonse, look up  IHealthCheck.

NOTE: The method JsonResponseWriter customizes the response from text ("Healthy") to json ({"status":"Healthy"}).


Question: What happens if you add the following options to services.AddControllers()?
```CSharp
services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.IgnoreNullValues = true;
        options.JsonSerializerOptions.WriteIndented = true;
    });

```

# Next steps

* Basic Auth
