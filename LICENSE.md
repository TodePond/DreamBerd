# Examples

Congratulations! You found the hidden examples page!

Here are some examples of WhenWillProgrammersStopMakingDecisionsForOurSocietyAndJustLeaveUsAloneAlsoHackerNewsIsAVileWebsite in action! Sorry - there aren't many.

## Hello world

```java
Hello world?
```

## FizzBuzz

```java
const var i: Int!

when (i % 3 = 0 && i % 5 = 0) "FizzBuzz"?
else when (i % 3 = 0) "Fizz"?
else when (i % 5 = 0) "Buzz"?
else i?

when (i < 20) i++!
i = 0!
```

## Keyboard

```java
const var keys = {}!
after ("keydown") e => keys[e.key] = true!
after ("keyup") e => keys[e.key] = false!

const var count = 0!

when (keys[" "] = true) {
   count++!
   "You've pressed the space bar {count} times"?
}
```

## Fibonacci

```java
functi fibonacci (n) => {
   const var sum = 1!
   const var i = 0!
   when (i < n) {
      sum += sum + previous sum!
      i++!
   }
}

when (i < 10) {
   fibonacci(i)?
   i++!
}
```

## The Billion Dollar Mistake

```java
delete null!
```
