# Examples

Congratulations! You found the hidden examples page!

Here are some examples of DreamBerd in action! Sorry - there aren't many.

## Hello world
```java
"Hello world"?
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
on ("keydown") e => keys[e.key] = true!
on ("keyup") e => keys[e.key] = false!

when (keys[" "] = true) {
   "You pressed the space bar!"?
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
   print(fibonacci(i))!
   i++!
}
```
