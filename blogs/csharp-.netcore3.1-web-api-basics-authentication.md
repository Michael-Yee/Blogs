---
title: .NET Core 3.1 Web API using basic authentication
author: Michael Yee
published: True
---


# Overview

In this blog, I will explore basics authentication for a .NET Core 3.1 Web API.

# Background

Basic authentication is a simple authentication scheme built into the HTTP protocol. The client sends HTTP requests with the Authorization header that contains the word Basic word followed by a space and a base64-encoded string username:password. For example, to authorize as demo / p@55w0rd the client would send

```Text
Authorization: Basic ZGVtbzpwQDU1dzByZA==
```
Note: Because base64 is easily decoded (https://www.base64decode.net/), Basic authentication should only be used together with other security mechanisms such as HTTPS/SSL.

# Getting started

We will pick up where we left off in a previous blog on `.NET Core 3.1 Web API basics`.

Before exploring basic authentication, we need to have a service that will validate credentials against the credentials store. In most cases this would be a database or external service, but in this blog, I'll keep things simple and hard code validation logic.

Create a new folder call `Services` and within this folder, create a new class called `UserService` with the following content:

```CSharp
using System;

namespace WebAPIBasics.Services
{  
    public interface IUserService  
    {  
        bool ValidateCredentials(String username, String password);  
    }

    public class UserService : IUserService  
    {  
        public bool ValidateCredentials(string username, string password)  
        {  
            return username.Equals("demo") && password.Equals("P@55w0rd");  
        }  
    }  
}  
```

# Authentication handler

The authentication handler implementation which will take care of encoding header value and pass the credentials to UserService instance to validate them.

Create a new folder call `Handlers` and within this folder, create a new class called `BasicAuthenticationHandler` with the following content:

```CSharp
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System;
using System.Linq;
using System.Net.Http.Headers;
using System.Security.Claims;
using System.Text;
using System.Text.Encodings.Web;
using System.Threading.Tasks;
using WebAPIBasics.Services;

namespace WebAPIBasics.Handlers
{
    public class BasicAuthenticationHandler : AuthenticationHandler<AuthenticationSchemeOptions>
    {
        readonly IUserService _userService;

        public BasicAuthenticationHandler(
            IUserService userService,
            IOptionsMonitor<AuthenticationSchemeOptions> options,
            ILoggerFactory logger,
            UrlEncoder encoder,
            ISystemClock clock)
            : base(options, logger, encoder, clock)
        {
            _userService = userService;
        }

        protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
        {
            string username = null;
            try
            {
                var authHeader = AuthenticationHeaderValue.Parse(Request.Headers["Authorization"]);
                var credentials = Encoding.UTF8.GetString(Convert.FromBase64String(authHeader.Parameter)).Split(':');
                username = credentials.FirstOrDefault();
                var password = credentials.LastOrDefault();

                if (!_userService.ValidateCredentials(username, password))
                    throw new ArgumentException("Invalid credentials");
            }
            catch (Exception ex)
            {
                return AuthenticateResult.Fail($"Authentication failed: {ex.Message}");
            }

            var claims = new[] {
                new Claim(ClaimTypes.Name, username)
            };
            var identity = new ClaimsIdentity(claims, Scheme.Name);
            var principal = new ClaimsPrincipal(identity);
            var ticket = new AuthenticationTicket(principal, Scheme.Name);

            return AuthenticateResult.Success(ticket);
        }
    }
}
```

# Fixing up the plumbing in Startup.cs

BasicAuthenticationHandler and UserService needs to be added to dependency injection.

Luckily, the pipeline has authorization, but we will need to add authentication where both will be utilize in BasicAuthenticationHandler.

```CSharp
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.Extensions.Hosting;
using WebAPIBasics.Handlers;
using WebAPIBasics.Services;

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
            services.AddScoped<IUserService, UserService>();
            services.AddAuthentication("BasicAuthentication")  
                .AddScheme<AuthenticationSchemeOptions, BasicAuthenticationHandler>("BasicAuthentication", null);
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

            app.UseAuthentication();

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

# Are we there yet?

And finally, a controller needs to be decorated with [Authorize] attribute which indicates this controller will allow only authenticated user to access its methods

```CSharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace WebAPIBasics.Controllers
{
    [Authorize]
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
                APIName = "WebAPIBasics"
            };

            // TODO: Log any failures
            return responseObject;
        }
    }
}
```

# Next steps

* Swagger 
