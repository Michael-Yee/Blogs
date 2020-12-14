---
title: To TypeScript, or not to TypeScript, that is the question
author: Michael Yee
published: True
---


# Overview

In this blog, I will explore the advantages betweeen JavaScript and TypeScript.

TLDR: Not only does TypeScript have all the advantages of Javascript, it was meant to ease the writing of scalable code.

## HTML

HTML is the markup language that is use to structure a webpage; for example, defining paragraphs, data tables or embedding images/videos.

HTML Snippet:

```
<!DOCTYPE html>
<html>
<body>
<p>Hello World!</p>
</body>
</html>
```

## CSS 

CSS is a language of style rules that is applied styling to our HTML; for example, setting text colors, fonts size or lay out.

HTML + CSS Snippet:

```
<!DOCTYPE html>
<html>
<head>
<style>
p {font-family: 'Times New Roman', Times, serif;}
</style>
</head>
<body>
<p>Hello World!</p>
</body>
</html>
```

## JavaScript

JavaScript (JS) is a scripting language that enables you to create dynamically updating content, control multimedia, animate images, etc...

HTML + CSS + JS Snippet:

```
<!DOCTYPE html>
<html>
<head>
<style>
p {font-family: 'Times New Roman', Times, serif;}
</style>
</head>
<body>
<p id="JavaScript"></p>
<script>
document.getElementById("JavaScript").innerHTML = "Hello World!";
</script>
</body>
</html>
```

## TypeScript

TypeScript is an open-source language which builds on JavaScript by adding static type definitions.

Types provide a way to describe the shape of an object, providing better documentation, and allowing TypeScript to validate that your code is working correctly.

TS Snippet:

```
class Greetings {
    //field 
    name:string; 

    //constructor 
    constructor(name: string) { 
        this.name = name 
    } 

    //function 
    sayHello() { 
      return "Hello " + this.name + "!";
    } 
}

var greetings = new Greetings("World");
document.body.innerHTML = greetings.sayHello();
```

HTML + CSS Snippet:

```
<!DOCTYPE html>
<html>
<head>
<style>
p {font-family: 'Times New Roman', Times, serif;}
</style>
</head>
<body>
<p><script src='greetings.js'></script></p>
</body>
</html>
```

## TypeScript Advantages 

* Correnctness or errors at compile time
* TS to JS or JS to TS
* Will run on any browser, device or operating system.

## JavaScript Advantages

* The most popular choice by far leading to a large online community and resource reference

# Summation

Typescript will help you write better quality code and find more bugs.
