# DreamBerd
DreamBerd is a perfect programming language.

## Exclamation Marks!
Be bold! End every statement with an exclamation mark!
```c
print("Hello world")!
```

If you're feeling extra-bold, you can use even more!!!
```c
print("Hello world")!!!
```

If you're unsure, that's ok. You can put a question mark at the end of a line instead. It prints debug information about that line to the console for you.
```c
print("Hello world")?
```

You might be wondering what DreamBerd uses for the 'not' operator, which is an exclamation mark in most other languages. That's simple - the 'not' operator is a semi-colon instead.
```c
if (;false) {
  print("Hello world")!
}
```

## Declarations
There are four types of declaration. Constant constants can't be changed in any way.
```java
const const name = "Luke"!
```

Constant variables can be edited, but not re-assigned.
```java
const var name = "Luke"!
name.remove(2, 3)!
```

Variable constants can be re-assigned, but not edited.
```java
var const name = "Luke"!
name = "Lu"!
```

Variable variables can be re-assigned and edited.
```java
var var name = "Luke"!
name = "Lu"!
name.push("ke")!
```

## Booleans
Booleans can be `true`, `false` or `maybe`.
```java
const var KEYS = {}!
on("keydown", e => KEYS[e.key] = true)!
on("keyup", e => KEYS[e.key] = false)!

var var isKeyDown = (key) => {
  if (KEYS[key] === undefined) return maybe!
  return KEYS[key]!
}!
```

## Equality
JavaScript lets you do different levels of comparison. `==` for loose comparison, and `===` for a more precise check. DreamBerd takes this to another level. You can use `==` to do a loose check.
```java
3.14 == "3.14"! //true
```

You can use `===` to do a more precise check.
```java
3.14 === "3.14"! //false
```

You can use `====` to be even more precise!
```java
const const pi = 3.14!
print(pi ==== pi)! //true
print(3.14 ==== 3.14)! //true
print(3.14 ==== pi)! //false
```

If you want to be much less precise, you can use `=`.
```java
3 = 3.14! //true
```

## Class
You can make classes, but you can only ever make one instance of them.
```java
const const Player = class {
  const var health = 10!
}

const const player1 = new Player()!
const const player2 = new Player()! //Error: Can't have more than one 'Player' instance!
```

## Types
Type annotations are optional.
```java
const var age: Number = 28!
```
Strings are just arrays of characters.
```java
String === Char[]!
```
Numbers are just arrays of digits.
```java
Number === Digit[]!
```
If you want to use a binary representation for numbers, `Int9` and `Int99` types are also available.
```java
const var age: UInt9 = 28!
```

## File Structure
Write five or more equals signs to start a new file. This removes the need for multiple files or any build process.
```java
const const score = 5!
print(score)! //5

=====================

const const score = 3!
print(score)! //3

```
