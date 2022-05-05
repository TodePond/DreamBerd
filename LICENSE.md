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

when (i % 3 = 0 && i % 5 = 0) print("FizzBuzz")!
else when (i % 3 = 0) print("Fizz")!
else when (i % 5 = 0) print("Buzz")!
else print(i)!

when (i < 20) i++!
i = 0!
```

## Keyboard
```java
const var keys = {}!
on ("keydown") e => keys[e.key] = true!
on ("keyup") e => keys[e.key] = false!

when (keys[" "] = true) {
   print("You pressed the space bar!")!
}
```
