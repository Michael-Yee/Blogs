---
title: Scala
author: Michael Yee
published: True
---

# Overview

My little scrtach pad in my journey of learning Scala.

---

# [Install Scala on your computer](https://docs.scala-lang.org/getting-started/index.html)

---

# The basics

```Scala
object HelloWorld extends App {
  println("Hello World1")
}
```

object HelloWorld: Creates the class HelloWord
extends App:  Makes the code executable

NOTE: We use camel case in Scala for objects

## Definding a value (constant)

```Scala
val greeting: String = "Hello world!"

or

val greeting = "Hello world!"


object HelloWorld extends App {
  println( greeting )
}
```

NOTE: Values are immutable and defining the type is optional as the complier can figure this out usually.

## Types

There are nine predefined value types and they are non-nullable: Double, Float, Long, Int, Short, Byte, Char, Unit, Boolean and String.

The Unit type returns no meaningful value or "void" in other languages.  The value of Unit type is `()`

## Strings

Concatenation:

```Scala
val greeting = "Hello" + " " + "world!"
```

Note: Operators are methods in Scala

Interpolation

```Scala
val name = "Mike"
val greeting = s"Hello, $name"
```

## If, else if and else


```Scala
val ifExpression = if (age < 18) -1
val ifElseExpression = if (age < 18) -1 else 1
val ifElseIfElseExpression = 
  if (age < 18) -1 
  else (age > 100) 0
  else 1
```

# Code block

```Scala
val codeBlock = {
  val x = 1
  val y =2

  x + y
}
```

Note: The return value of the code black is the value of the last expression

## Function

```Scala
def myFunction(luckyNumber: Int, name: String): String = {
  s"Hello, $name.  Your lucky number is $luckyNumber."
}
```

```Scala
def myUnitFunction(luckyNumber: Int, name: String): Unit = {
  println(s"Hello, $name.  Your lucky number is $luckyNumber.")
}
```

The myUnitFunction is an example of a function that contains a side effect and returns the Unit type

## Recursion - No loops or iteration!

```Scala
def factorial(n: Int): Int = {
  if (n <= 1) 1
  else n * factorial(n -1)
```
}

# Object Orientated

## Class and instantiate

```Scala
class Car {
  val wheels: Int = 0

  def engineNoise() = println("Vroom Vroom!")
}

val aCar = new Car
```

NOTE: All fields and methods are public by default. You can restrict by add one of the two: 
`private`:  Only the class as access
`protected`: Only the class its decedants as access

## Inheritance

```Scala
class Honda extends Car

or

class Honda extends Car {
   def hornNoise() = println("Honk Honk!")
}
```

## Class arguments

```Scala
class Toyota(hornNoise: String) extends Car {
   def hornNoise() = println(s"$hornNoise!")
}

val aToyotaType = new Toyota("Beep Beep")
```

NOTE: is an contructor arugment are NOT fields
i.e. aToyotaType.hornNoise, the complier will not resolve `name` as it does not exist outside the class definition

To make the contructor arguement a field, place val infront contructor arugment

```Scala
class Toyota(val hornNoise: String) extends Car {
}

val aToyotaType = new Toyota("Beep Beep")
aToyotaType.hornNoise
```

## Subtype polymorphism

```Scala
val anCar: Car = new Honda()
anCar.hornNoise()
```

NOTE: hornNoise -> the most derived mothod will be called at runtime

## Abstract class

```Scala
class Car {
  val hasWheels = tue
  val speed(): Unit
}
```

NOTE: speed() method would be defined in a child class

## Interface

Ultimate abstract type where everything is unimplemented

```Scala
trait Transportation {
  def land(car: Car): Unit
}
```

## Single class inheritance and mult-trait ("mixing")

```Scala
class Audi extends Car with Transportation {
  override def land(car: Car): Unit = println("I use roads")
}
```

## Infix notation

```Scala
val anAudi = new Audi
anAudi.fuel("GAS")

or 

anAudi fuel "GAS"
```

NOTE: Only works with methods with one argument

## Anonymous classes

```Scala
val aHummer = new Transportation {
  override def land(car: Car): Unit = println("I drive on anything")
}
```

## Singleton object

```Scala
object MySingleton {
  val mySpecialValue = 42
  def mySpecialMethod(): String = "Special"
  def apply(x: Int): Int: x + 1 
}

MySingleton.apply(1)

or 

MySingleton(1)
```

NOTE:  The only instance of the MySingleton type.  
Special method call `apply` can be used in any class or object.

## Companion object

```Scala
class Car {
  val wheels: Int = 0

  def engineNoise() = println("Vroom Vroom!")
}

object Car {
  val fuelType = "GAS"
}

val carFuelType = Car.fuelType
```

NOTE: Can be applied to classes or trait.  Can access each other's private fields and methods.  Singleton and instances of Car are different things.

// Case classes

Case classes are lightweight data structures with some boilerplate
- sensible equals and hash code
- serilaization
- companion and apply

```Scala
case class Person(name: String, age: Int)

val bob = Person("Bob", 42)
```

Note: May be constructed without `new`

# Exceptions

```Scala
def toInt(s: String): Int = {
    try {
      Integer.parseInt(s)
    } catch {
      case e: Exception => "Input not valid"
    } finally {
      // executes some code no matter happened
    }
}
```

NOTE: The finally section is optional

# Generic

Generic classes take a type as a parameter within square brackets []. 

```Scala
abstract class MyList[T] {
  def head: T
  def tail: MyList[T]
}

// using a generic with a concrete type
val aList: List[Int] = List(1,2,3) // List.apply(1,2,3)
val first = aList.head // int
val rest = aList.tail

val aStringList = List("one", "two", "three")
val firstString = aStringList.head // string
```

Point #1: in Scala we usually operate with IMMUTABLE values/objects

Any modification to an object must return ANOTHER object

  Benefits:
  1) works miracles in multithreaded/distributed env
  2) helps making sense of the code ("reasoning about")

  val reversedList = aList.reverse // returns a NEW list

Point #2: Scala is closest to the OO ideal

# Functional programming

Functional programming:
- compose functions
- pass functions as args
- return functions as results

Scala runs on the JVM, we need 1st class functions 
Solution: FunctionX = Function1, Function2, ... Function22

```Scala
val simpleIncrementer = new Function1[Int, Int] {
    override def apply(arg: Int): Int = arg + 1
}

  simpleIncrementer.apply(23) // 24
  simpleIncrementer(23) // simpleIncrementer.apply(23)
  // defined a function!
```
NOTE: ALL SCALA FUNCTIONS ARE INSTANCES OF THESE FUNCTION_X TYPES

## Sytax Sugar - part 1

```Scala
val simpleIncrementer = new Function1[Int, Int] {
    override def apply(arg: Int): Int = arg + 1
}

==

val simpleIncrementer: Int => Int = (arg: Int) => arg + 1

==

val simpleIncrementer = (arg: Int) => arg + 1

```

## Higher order functions

Higher order functions take other functions as parameters or return a function as a result.

```Scala
val aMappedList: List[INT] = List(1, 2, 3).map(x => x + 1)

==

val aMappedList = List(1, 2, 3).map {
  x => x + 1
}
```

## Sytax Sugar - part 2

```Scala
val aMappedList = List(1, 2, 3, 4 ,5).filter(x => x <= 3)

==

val aMappedList = List(1, 2, 3, 4 ,5).filter(_ <= 3)  
```

## Comprehension

```Scala
// all pairs between the numbers 1, 2, 3 and the letters 'a', 'b', 'c'
val allPairs1 = List(1,2,3).flatMap(number => List('a', 'b', 'c').map(letter => s"$number-$letter"))

==

val allPairs2 = for {
  number <- List(1,2,3)
  letter <- List('a', 'b', 'c')
} yield s"$number-$letter"
```

NOTE: `for` is not a for loop

# Collections

## Lists

```Scala
val aList = List(1, 2, 3, 4, 5)

val firstElement = aList.head
val rest = aList.tail

val aPrependedList = 0 :: aList // returns List(0, 1, 2, 3, 4, 5)
val anExtendedList = 0 +: aList :+ 6 // returns List(0, 1, 2, 3, 4, 5, 6)
```

## Sequences

```Scala
val aSequence: Seq[Int] = Seq(1,2,3) // Seq.apply(1,2,3)
val accessedElement = aSequence(1) // the element at index 1: 2
```

## Vectors

```Scala
// vectors: fast Seq implementation
val aVector = Vector(1,2,3,4,5)
```

## Sets

```Scala
// sets = no duplicates
val aSet = Set(1,2,3,4,1,2,3) // Set(1,2,3,4)
val setHas5 = aSet.contains(5) // false
val anAddedSet = aSet + 5 // Set(1,2,3,4,5)
val aRemovedSet = aSet - 3 // Set(1,2,4)
```

## Ranges

```Scala
val aRange = 1 to 1000
val twoByTwo = aRange.map(x => 2 * x).toList // List(2,4,6,8..., 2000)
```

## Tuples

```Scala
val aTuple = ("Bon Jovi", "Rock", 1982)
```

## Maps

```Scala
val aPhonebook: Map[String, Int] = Map(
  ("Daniel", 6437812),
  "Jane" -> 327285 // ("Jane", 327285)
)
```

# Pattern Matching

## Switch expression

Pattern matching is a mechanism for checking a value against a pattern. A successful match can also deconstruct a value into its constituent parts. Can be used in place of a series of if/else statements.

```Scala
val anInteger = 55
val order = anInteger match {
  case 1 => "first"
  case 2 => "second"
  case 3 => "third"
  case _ => anInteger + "th"
}
```

## Deconstruct

```Scala
case class Person(name: String, age: Int)
val bob = Person("Bob", 43)

val personGreeting = bob match {
  case Person(n, a) => s"Hi, my name is $n and I am $a years old."
  case _ => "Something else"
}
```

```Scala
val aTuple = ("Bon Jovi", "Rock")
val bandDescription = aTuple match {
  case (band, genre) => s"$band belongs to the genre $genre"
  case _ => "I don't know what you're talking about"
}
```

```Scala
val aList = List(1,2,3)
val listDescription = aList match {
  case List(_, 2, _) => "List containing 2 on its second position"
  case _ => "unknown list"
}
```

NOTE ONE: If pattern matching doesn't match anything, it will throw a MatchError
NOTE Two: Pattern matching will try all cases in sequence

# Advance Topics

# Contextual Abstractions (Scala 3 only)




Read more on

`?!`` method
































