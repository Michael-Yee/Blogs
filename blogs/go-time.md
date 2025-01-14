---
title: Go time!
author: Michael Yee
published: True
---

# Overview

My little scrtach pad in my journey of learning Go.

---

# Hello World!

## Structure of a Go program

- package main lets the Go compiler know that we want this code to compile and run as a standalone program, as opposed to being a library that's imported by other programs.
- import fmt imports the fmt (formatting) package. The formatting package exists in Go's standard library and let's us do things like print text to the console.
- func main() defines the main function. main is the name of the function that acts as the entry point for a Go program.


```go
package main

import "fmt"

func main() {
    // How to add a single line comment
    fmt.Println("Hello World!")
}
```

## Declaring variables

Go's basic variable types are:

- bool
- string
- int  int8  int16  int32  int64 uint uint8 uint16 uint32 uint64 uintptr
- byte // alias for uint8
- rune // alias for int32 and represents a Unicode code point
- float32 float64
- complex64 complex128

NOTE: Unless memory is limited, the most used number variable types are: int, uint, float64 and complex12

```go
package main

import "fmt"

func main() {
    var item int
    var cost float64
    var isValid bool
    var username string

    fmt.Printf("%v %f %v %q\n", item, cost, isValid, username)
}
```

### Short Variable Declaration

Inside a function, the := short assignment statement can be used in place of a var declaration. The := operator infers the type of the new variable based on the value.

```go
package main

import "fmt"

func main() {
    message, year := "The year is ", 2023

    fmt.Printf(message, year)
}
```

## Type Casting

Type casting is the process of converting the value of one data type (integer, float, string) to another data type. For example,

```go
// variable of float type
var floatValue float = 3.14

// convert float to int
var intValue int = int(floatValue)
```

Here, int(floatValue) specifies that we are converting the float value 3.14 to 3.

## Declaring constants

Constants are declared like variables but use the const keyword. Constants can't be defined using the := short declaration syntax.

Constants can be character, string, boolean, or numeric values. They can not be more complex types like slices, maps and structs.

```go
package main

import "fmt"

func main() {
    const helloWorld = "Hello World!"

    fmt.Println(helloWorld)
}
```

## Strings

fmt.Printf - Prints a formatted string to standard out.
fmt.Sprintf() - Returns the formatted string

### Examples:


The %v variant prints the Go syntax representation of a value. You can usually use this if you're unsure what else to use. That said, it's better to use the type-specific variant if you can.

```go
fmt.Printf("I am %v years old", 29)
```

Interpolate a string

```go
message := fmt.Sprintf("I am %s years old", "very")
fmt.Printf(message)
```

Interpolate an integer in decimal form

```go
fmt.Printf("I am %d years old", 99)
```

Interpolate a decimal

```go
fmt.Printf("I am %f years old", 7.5)

// The ".2" rounds the number to 2 decimal places
fmt.Printf("I am %.2f years old", 5.555)
```

## Conditions

```go
if bankAccount > 1000 {
    fmt.Println("You are super rich!")
} else if bankAccount >= 100 {
    fmt.Println("You are not poor!")
} else {
    fmt.Println("You are poor!")
}
```

An if conditional can have an "initial" statement. The variable(s) created in the initial statement are only defined within the scope of the if body.

```go
if INITIAL_STATEMENT; CONDITION {
}
```

Example:

```go
result := getResult()

if result < .5 {
    fmt.Println("Above average")
}

```

Better:

```go
if result := getResult(); result < .5 {
    fmt.Println("Above average")
}
```

Not only is this code a bit shorter, but it also removes result from the parent scope, which is convenient because we don't need it there - we only need access to it while checking a condition.

## Functions

Example

```go
func add(x int, y int) int {
  return x + y
}
```

Shorter if the arguments are the same type:

```go
func add(x, y int) int {
  return x + y
}
```

A function can return a value that the caller doesn't care about. We can explicitly ignore variables by using an underscore: _

```go
func getPoint() (lat int, lon int) {
  return 8.88, 7.77
}

// ignore y value
x, _ := getPoint()
```

NOTE: (x int, y int) signifies multiple return values

```go
func getCoords() (x, y int){
  // x and y are initialized with zero values

  return // automatically returns x and y
}
```

Is the same as:

```go
func getCoords() (int, int){
  var x int
  var y int
  return x, y
}
```

## Structs

We use structs in Go to represent structured data. It's often convenient to group different types of variables together. For example, if we want to represent a car we could do the following:

```go
type car struct {
  Make string
  Model string
  Height int
  Width int
}
```

This creates a new struct type called car. All cars have a Make, Model, Height and Width.


In Go, you will often use a struct to represent information that you would have used a dictionary for in Python, or an object literal for in JavaScript.

Structs can be nested to represent more complex entities:

```go
type car struct {
  Make string
  Model string
  Height int
  Width int
  FrontWheel Wheel
  BackWheel Wheel
}


type Wheel struct {
  Radius int
  Material string
}
```

The fields of a struct can be accessed using the dot . operator.

```go
myCar := car{}
myCar.FrontWheel.Radius = 5
```

Go is not an object-oriented language. However, embedded structs provide a kind of data-only inheritance that can be useful at times. Keep in mind, Go doesn't support classes or inheritance in the complete sense, embedded structs are just a way to elevate and share fields between struct definitions.

```go
type car struct {
  make string
  model string
}

type truck struct {
  // "car" is embedded, so the definition of a
  // "truck" now also additionally contains all
  // of the fields of the car struct
  car
  bedSize int
}
```

Embedded vs nested
An embedded struct's fields are accessed at the top level, unlike nested structs.
Promoted fields can be accessed like normal fields except that they can't be used in composite literals

```go
lanesTruck := truck{
  bedSize: 10,
  car: car{
    make: "toyota",
    model: "camry",
  },
}

fmt.Println(lanesTruck.bedSize)

// embedded fields promoted to the top-level
// instead of lanesTruck.car.make
fmt.Println(lanesTruck.make)
fmt.Println(lanesTruck.model)
```

While Go is not object-oriented, it does support methods that can be defined on structs. Methods are just functions that have a receiver. A receiver is a special parameter that syntactically goes before the name of the function.

```go
type rect struct {
  width int
  height int
}

// area has a receiver of (r rect)
func (r rect) area() int {
  return r.width * r.height
}

r := rect{
  width: 5,
  height: 10,
}

fmt.Println(r.area())
// prints 50
```

## Interfaces

A receiver is just a special kind of function parameter. Receivers are important because they will, as you'll learn in the exercises to come, allow us to define interfaces that our structs (and other types) can implement.

Interfaces are collections of method signatures. A type "implements" an interface if it has all of the methods of the given interface defined on it.

In the following example, a "shape" must be able to return its area and perimeter. Both rect and circle fulfill the interface.

```go
type shape interface {
  area() float64
  perimeter() float64
}

type rect struct {
    width, height float64
}
func (r rect) area() float64 {
    return r.width * r.height
}
func (r rect) perimeter() float64 {
    return 2*r.width + 2*r.height
}

type circle struct {
    radius float64
}
func (c circle) area() float64 {
    return math.Pi * c.radius * c.radius
}
func (c circle) perimeter() float64 {
    return 2 * math.Pi * c.radius
}
When a type implements an interface, it can then be used as the interface type.
```

Consider the following interface:

```go
type Copier interface {
  Copy(string, string) int
}
```
Based on the code alone, can you deduce what kinds of strings you should pass into the Copy function?

We know the function signature expects 2 string types, but what are they? Filenames? URLs? Raw string data? For that matter, what the heck is that int that's being returned?

Let's add some named arguments and return data to make it more clear.

```go
type Copier interface {
  Copy(sourceFile string, destinationFile string) (bytesCopied int)
}
```

Much better. We can see what the expectations are now. The first argument is the sourceFile, the second argument is the destinationFile, and bytesCopied, an integer, is returned.

When working with interfaces in Go, every once-in-awhile you'll need access to the underlying type of an interface value. You can cast an interface to its underlying type using a type assertion.

```go
type shape interface {
    area() float64
}

type circle struct {
    radius float64
}

// "c" is a new circle cast from "s"
// which is an instance of a shape.
// "ok" is a bool that is true if s was a circle
// or false if s isn't a circle
c, ok := s.(circle)
```

A type switch makes it easy to do several type assertions in a series.

A type switch is similar to a regular switch statement, but the cases specify types instead of values.

```go
func printNumericValue(num interface{}) {
    switch v := num.(type) {
    case int:
        fmt.Printf("%T\n", v)
    case string:
        fmt.Printf("%T\n", v)
    default:
        fmt.Printf("%T\n", v)
    }
}

func main() {
    printNumericValue(1)
    // prints "int"

    printNumericValue("1")
    // prints "string"

    printNumericValue(struct{}{})
    // prints "struct {}"
}
```

fmt.Printf("%T\n", v) prints the type of a variable.

## Error

Go programs express errors with error values. An Error is any type that implements the simple built-in error interface:

```go
type error interface {
    Error() string
}
```

When something can go wrong in a function, that function should return an error as its last return value. Any code that calls a function that can return an error should handle errors by testing whether the error is nil.

```go
// Atoi converts a stringified number to an interger
i, err := strconv.Atoi("42b")
if err != nil {
    fmt.Println("couldn't convert:", err)
    // because "42b" isn't a valid integer, we print:
    // couldn't convert: strconv.Atoi: parsing "42b": invalid syntax
    // Note:
    // 'parsing "42b": invalid syntax' is returned by the .Error() method
    return
}
// if we get here, then
// i was converted successfully
```

A nil error denotes success; a non-nil error denotes failure.

Because errors are just interfaces, you can build your own custom types that implement the error interface. Here's an example of a userError struct that implements the error interface:

```go
type userError struct {
    name string
}

func (e userError) Error() string {
    return fmt.Sprintf("%v has a problem with their account", e.name)
}
```

It can then be used as an error:

```go
func sendSMS(msg, userName string) error {
    if !canSendToUser(userName) {
        return userError{name: userName}
    }
    ...
}
```

The Go standard library provides an "errors" package that makes it easy to deal with errors.

Read the godoc for the errors.New() function, but here's a simple example:

```go
var err error = errors.New("something went wrong")
```

## Loops

The basic loop in Go is written in standard C-like syntax:

```go
for INITIAL; CONDITION; AFTER{
  // do something
}
```

INITIAL is run once at the beginning of the loop and can create variables within the scope of the loop.

CONDITION is checked before each iteration. If the condition doesn't pass then the loop breaks.

AFTER is run after each iteration.

For example:

```go
for i := 0; i < 10; i++ {
  fmt.Println(i)
}
// Prints 0 through 9
```

Loops in Go can omit sections of a for loop. For example, the CONDITION (middle part) can be omitted which causes the loop to run forever.

```go
for INITIAL; ; AFTER {
  // do something forever
}
```

Most programming languages have a concept of a while loop. Because Go allows for the omission of sections of a for loop, a while loop is just a for loop that only has a CONDITION.

for CONDITION {
  // do some stuff while CONDITION is true
}
For example:

```go
plantHeight := 1
for plantHeight < 5 {
  fmt.Println("still growing! current height:", plantHeight)
  plantHeight++
}
fmt.Println("plant has grown to ", plantHeight, "inches")
```

Which prints:

still growing! current height: 1
still growing! current height: 2
still growing! current height: 3
still growing! current height: 4
plant has grown to 5 inches

The continue keyword stops the current iteration of a loop and continues to the next iteration. continue is a powerful way to use the "guard clause" pattern within loops.

```go
for i := 0; i < 10; i++ {
  if i % 2 == 0 {
    continue
  }
  fmt.Println(i)
}
// 1
// 3
// 5
// 7
// 9
```

break
The break keyword stops the current iteration of a loop and exits the loop.

```go
for i := 0; i < 10; i++ {
  if i == 5 {
    break
  }
  fmt.Println(i)
}
// 0
// 1
// 2
// 3
// 4
```

## Arrays

Arrays are fixed-size groups of variables of the same type.

The type [n]T is an array of n values of type T

To declare an array of 10 integers:

```go
var myInts [10]int
```
or to declare an initialized literal:

```go
primes := [6]int{2, 3, 5, 7, 11, 13}
```

99 times out of 100 you will use a slice instead of an array when working with ordered lists.

Arrays are fixed in size. Once you make an array like [10]int you can't add an 11th element.

A slice is a dynamically-sized, flexible view of the elements of an array.

Slices always have an underlying array, though it isn't always specified explicitly. To explicitly create a slice on top of an array we can do:

```go
primes := [6]int{2, 3, 5, 7, 11, 13}
mySlice := primes[1:4]
// mySlice = {3, 5, 7}
```

The syntax is:

```go
arrayname[lowIndex:highIndex]
arrayname[lowIndex:]
arrayname[:highIndex]
arrayname[:]
```

Where lowIndex is inclusive and highIndex is exclusive

Either lowIndex or highIndex or both can be omitted to use the entire array on that side.

Make

Most of the itme we don't need to think about the underlying arroay of a slice.  We can create a new slice using the `make` funcation:

```go
// func make ([]T len, cap) []T
mySlice := make([]int 5, 10)

// the capacity argument is usually omitted and defaults to the length
mySlice := make([]int 5)
```

Slices create with `make` will be filled with zero values of the type.

If we want to create a slice with a specific set of values, we can use a slice literal:

```go
mySlice := []string {"I", "love", "you"}
```

Note that the arry brackets do not have a `3` in them.  If they did, you'd have an array of instead of a slice.

Lenght

The lenght of a slice is simple the number of elements it contains.  It is accessed using the built-in len() function:

```go
mySlice := []string {"I", "love", "you"}
fmt.Println(len(myslice))  // 3
```

Capacity

The capacity of a slice in the number os elements in the underlying array, counting from the first element in the slice.  It is accessed using the buld-in cap() function:

```go
mySlice := []string {"I", "love", "you"}
fmt.Println(cap(myslice))  // 3
```

Variadic

Many functions, especially those in the standard library, can take an arbitrary number of final arguments. This is accomplished by using the "..." syntax in the function signature.

A variadic function receives the variadic arguments as a slice.

```go
func sum(nums ...int) int {
    // nums is just a slice
    for i := 0; i < len(nums); i++{
        num := nums[i]
    }
}

func main() {
    total := sum(1, 2, 3)
    fmt.Println(total)
    // prints "6"
}
```

The familiar fmt.Println() and fmt.Sprintf() are variadic! fmt.Println() prints each element with space delimiters and a newline at the end.

```go
func Println(a ...interface{}) (n int, err error)
```

Spread operator

The spread operator allows us to pass a slice into a variadic function. The spread operator consists of three dots following the slice in the function call.

```go
func printStrings(strings ...string) {
    for i := 0; i < len(strings); i++ {
        fmt.Println(strings[i])
    }
}

func main() {
    names := []string{"bob", "sue", "alice"}
    printStrings(names...)
}
```

Append

The built-in append function is used to dynamically add elements to a slice:

```go
func append(slice []Type, elems ...Type) []Type
```

If the underlying array is not large enough, append() will create a new underlying array and point the slice to it.

Notice that append() is variadic, the following are all valid:

```go
slice = append(slice, oneThing)
slice = append(slice, firstThing, secondThing)
slice = append(slice, anotherSlice...)
```

Slices can hold other slices, effectively creating a matrix, or a 2D slice.

rows := [][]int{}

Range
Go provides syntactic sugar to iterate easily over elements of a slice:

```go
for INDEX, ELEMENT := range SLICE {
}
```

For example:

```go
fruits := []string{"apple", "banana", "grape"}
for i, fruit := range fruits {
    fmt.Println(i, fruit)
}
// 0 apple
// 1 banana
// 2 grape
```

## Maps
Maps are similar to JavaScript objects, Python dictionaries, and Ruby hashes. Maps are a data structure that provides key->value mapping.

The zero value of a map is nil.

We can create a map by using a literal or by using the make() function:

```go
ages := make(map[string]int)
ages["John"] = 37
ages["Mary"] = 24
ages["Mary"] = 21 // overwrites 24
ages = map[string]int{
  "John": 37,
  "Mary": 21,
}
```

The len() function works on a map, it returns the total number of key/value pairs.

```go
ages = map[string]int{
  "John": 37,
  "Mary": 21,
}
fmt.Println(len(ages)) // 2
```

Mutations

Insert and element

```go
m[key] = elem
```

Get an element

```go
elem = m[key]
```

Delete an element

```go
delete(m, key)
```

Check if a key exists

```go
elem, ok := m[key]
```

If key is in m, then ok is true. If not, ok is false.

If key is not in the map, then elem is the zero value for the map's element type.

Key Types
Any type can be used as the value in a map, but keys are more restrictive.

Read the following section of the official Go blog:

As mentioned earlier, map keys may be of any type that is comparable. The language spec defines this precisely, but in short, comparable types are boolean, numeric, string, pointer, channel, and interface types, and structs or arrays that contain only those types. Notably absent from the list are slices, maps, and functions; these types cannot be compared using ==, and may not be used as map keys.

It's obvious that strings, ints, and other basic types should be available as map keys, but perhaps unexpected are struct keys. Struct can be used to key data by multiple dimensions. For example, this map of maps could be used to tally web page hits by country:

hits := make(map[string]map[string]int)
This is map of string to (map of string to int). Each key of the outer map is the path to a web page with its own inner map. Each inner map key is a two-letter country code. This expression retrieves the number of times an Australian has loaded the documentation page:

```go
n := hits["/doc/"]["au"]
```go

Unfortunately, this approach becomes unwieldy when adding data, as for any given outer key you must check if the inner map exists, and create it if needed:

```go
func add(m map[string]map[string]int, path, country string) {
    mm, ok := m[path]
    if !ok {
        mm = make(map[string]int)
        m[path] = mm
    }
    mm[country]++
}
add(hits, "/doc/", "au")
```

On the other hand, a design that uses a single map with a struct key does away with all that complexity:

```go
type Key struct {
    Path, Country string
}
hits := make(map[Key]int)
```

When a Vietnamese person visits the home page, incrementing (and possibly creating) the appropriate counter is a one-liner:

```go
hits[Key{"/", "vn"}]++
And it’s similarly straightforward to see how many Swiss people have read the spec:

n := hits[Key{"/ref/spec", "ch"}]
```

Remember that you can check if a key is already present in a map by using the second return value from the index operation.

```go
names := map[string]int{}

if _, ok := names["elon"]; !ok {
    // if the key doesn't exist yet,
    // initialize its value to 0
    names["elon"] = 0
}
```

Nested

Maps can contain maps, creating a nested structure. For example:

```go
map[string]map[string]int
map[rune]map[string]int
map[int]map[string]map[string]int
```

## defer

## closers












































































































































































































































