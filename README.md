<img align="right" height="100" src="https://user-images.githubusercontent.com/15892272/166904563-1967ac5c-a149-499e-a05d-6cd610808da9.png">

# DreamBerd
DreamBerd is a perfect programming language. These are its features!<br>
When you've finished reading through all the features, check out the [examples](https://github.com/TodePond/DreamBerd/blob/main/Examples.md).

## Exclamation Marks!
Be bold! End every statement with an exclamation mark!
```c
print("Hello world")!
```

If you're feeling extra-bold, you can use even more!!!
```c
print("Hello world")!!!
```

If you're unsure, that's ok. You can put a question mark at the end of a line instead. It prints debug info about that line to the console for you.
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
name.pop()!
name.pop()!
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
name.push("k")!
name.push("e")!
```

## Arrays
Some languages start arrays at `0`, which can be unintuitive for beginners. Some languages start arrays at `1`, which isn't representative of how the code actually works. DreamBerd does the best of both worlds: Arrays start at `-1`.
```java
const const scores = [3, 2, 5]!
print(scores[-1])! //3
print(scores[0])!  //2
print(scores[1])!  //5
```

**New for 2022!**<br>
You can now use floats for indexes too!
```java
const var scores = [3, 2, 5]!
scores[0.5] = 4
print(scores) //[3, 2, 4, 5]!
```

## When
Mutating variables is **very dangerous** and must be **avoided at all costs**. But in case you really need to vary variables, the `when` keyword lets you check a variable each time it mutates.
```java
const var health = 10!
when (health = 0) {
   print("You lose")!
}
```

## Installation
To install DreamBerd to your command line, first install the DreamBerd installer.<br>
To install the DreamBerd installer, install the DreamBerd installer installer.

**New for 2022!**<br>
Due to the complicated installation process, you can now install the 'Create DreamBerd App' app that installs everything for you!

## Booleans
Booleans can be `true`, `false` or `maybe`.
```java
const var keys = {}!
after ("keydown") e => keys[e.key] = true!
after ("keyup") e => keys[e.key] = false!

function isKeyDown(key) => {
   if (keys[key] = undefined) return maybe!
   return keys[key]!
}
```

**Technical info:** Booleans are stored as one-and-a-half bits.

## Conditionals
You can use the `perhaps` keyword for deciding what to do when a condition is `maybe`.
```java
const const isTuesday = maybe!

if (isTuesday) {
   print("It's Tuesday")!
} else {
   print("It's not Tuesday")!
} perhaps {
   print("It's maybe Tuesday")!
}
```

## Indents
When it comes to indentation, DreamBerd strikes a happy medium that can be enjoyed by everyone: All indents must be 3 spaces long.
```java
function main() => {
   print("DreamBerd is the future")!
}
```

-3 spaces is also allowed.
```java
   function main() => {
print("DreamBerd is the future")!
   }
```

## Equality
JavaScript lets you do different levels of comparison. `==` for loose comparison, and `===` for a more precise check. DreamBerd takes this to another level.

You can use `==` to do a loose check.
```java
3.14 == "3.14"! //true
```

You can use `===` to do a more precise check.
```java
3.14 === "3.14"! //false
```

You can use `====` to be EVEN MORE precise!
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

## Function
To declare a function, you can use any letters from the word `function` (as long as they're in order):
```java
function add (a, b) => a + b!
func multiply (a, b) => a * b!
fun subtract (a, b) => a - b!
fn divide (a, b) => a / b!
functi power (a, b) => a ** b!
```

## Types
Type annotations are optional.
```java
const var age: Int = 28!
```
By the way, strings are just arrays of characters.
```java
String == Char[]!
```
Similarly, integers are just arrays of digits.
```java
Int == Digit[]!
```

If you want to use a binary representation for integers, `Int9` and `Int99` types are also available.
```java
const var age: Int9 = 28!
```

**Technical info:** Type annotations don't do anything, but they help some people to feel more comfortable.

## Previous
The `previous` keyword lets you see into the past!<br>
Use it to get the previous value of a variable.
```java
const var score = 5!
score++!
print(score)! //6
print(previous score)! //5
```

Similarly, the `next` keyword lets you see into the future!
```java
const var score = 5!
after ("click") score++!
print(await next score)! //6 (when you click)
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

**New for 2022!**<br>
Thanks to recent advances in technology, you can give files names.
```java
======= add.db =======
function add(a, b) => {
   return a + b!
}
```

## Export
Many languages allow you to import things from specific files. In DreamBerd, importing is simpler. Instead, you export _to_ specific files!
```java
===== add.db ==
function add(a, b) => {
   return a + b!
}

export add to "main.db"!

===== main.db ==
import add!
add(3, 2)!
```

By the way, to see DreamBerd in action, check out [this page](https://github.com/TodePond/DreamBerd/blob/main/LICENSE.md).

## Loops
Loops are a complicated relic of archaic programming languages. With DreamBerd, just use the new `return` keyword to 'return' to the previous line.

```js
print("cheep")! //cheep, cheep, cheep...
return!
```

Use more exclamation marks to go back further!!
```js
var const i = 10!
print(i)!
i--!
if (i > 0) return!!
print("Blast off")!
```

If you want to get a value from a function, just `export` it!

```js
function add(a, b) => {
   export a + b!
}
print(add(3, 2)! //5
```

## Class
You can make classes, but you can only ever make one instance of them. This shouldn't affect how most object-oriented programmers work.
```java
class Player {
   const var health = 10!
}

const var player1 = new Player()!
const var player2 = new Player()! //Error: Can't have more than one 'Player' instance!
```

This is how you could do this:
```java
class PlayerMaker {
   function makePlayer() => {
      class Player {
         const var health = 10!
      }
      const const player = new Player()!
      return player!
   }
}

const const playerMaker = new PlayerMaker()!
const var player1 = playerMaker.makePlayer()!
const var player2 = playerMaker.makePlayer()!
```

## Now
Use `Date.now()` to get the current date and time.
```js
Date.now()
```

By the way, you can set the time.<br>

```js
// Move the clocks back one hour
Date.now() -= 3600000
```

**Important!**<br>
Please remember to do this when the clocks change.

## Time Travel
You can use this to your advantage!<br>
Let's say you're keeping track of whether the space bar is down or up...
```js
let down = maybe!
after ("keydown") e => {
   if (e.key = " ") down = true!
}

after ("keyup") e => {
   if (e.key = " ") down = false!
}
```

You can check the state of the space bar in the past..
```js
Date.now() -= 5000
if (down) {
   print("5 seconds ago, the space bar was down")!
}
```

Or the future!
```js
Date.now() += 3000
if (down) {
   print("3 seconds from now, the space bar will be down")!
}
```

## Delete
To avoid confusion, the `delete` statement only works with primitive values like numbers, strings, and booleans.

```js
delete 3!
print(2 + 1)! // Error: 3 has been deleted
```

DreamBerd is a multi-paradigm programming language, which means that you can `delete` the keywords and paradigms you don't like.

```js
delete class!
class Player {} // Error: class was deleted
```

When perfection is achieved and there is nothing left to `delete`, you can do this:

```js
delete delete!
```

## Examples

For examples of DreamBerd in action, check out the [examples page](https://github.com/TodePond/DreamBerd/blob/main/test/Examples.md)!
