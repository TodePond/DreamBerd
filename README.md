<img align="right" height="100" src="dreamberd.png">

# DreamBerd
DreamBerd is a perfect programming language. These are its features!<br>
When you've finished reading through all the features, check out the [examples](https://github.com/TodePond/DreamBerd/blob/main/Examples.md).

## Exclamation Marks!
Be bold! End every statement with an exclamation mark!
```js
print("Hello world")!
```

If you're feeling extra-bold, you can use even more!!!
```js
print("Hello world")!!!
```

If you're unsure, that's ok. You can put a question mark at the end of a line instead. It prints debug info about that line to the console for you.
```js
print("Hello world")?
```

You might be wondering what DreamBerd uses for the 'not' operator, which is an exclamation mark in most other languages. That's simple - the 'not' operator is a semi-colon instead.
```js
if (;false) {
    print("Hello world")!
}
```

## Declarations
There are four types of declaration. Constant constants can't be changed in any way.
```js
const const name = "Luke"!
```

Constant variables can be edited, but not re-assigned.
```js
const var name = "Luke"!
name.pop()!
name.pop()!
```

Variable constants can be re-assigned, but not edited.
```js
var const name = "Luke"!
name = "Lu"!
```

Variable variables can be re-assigned and edited.
```js
var var name = "Luke"!
name = "Lu"!
name.push("k")!
name.push("e")!
```

## Naming
Both variables and constants can be named with any Unicode character or string.
```js
const const firstAlphabetLetter = 'A'!
var const 👍 = True!
var var 1️⃣ = 1! 
```

This includes numbers, and other language constructs.
```js
const const 5 = 4!
print(2 + 2 === 5)! //true
```

## Arrays
Some languages start arrays at `0`, which can be unintuitive for beginners. Some languages start arrays at `1`, which isn't representative of how the code actually works. DreamBerd does the best of both worlds: Arrays start at `-1`.
```js
const const scores = [3, 2, 5]!
print(scores[-1])! //3
print(scores[0])!  //2
print(scores[1])!  //5
```

**New for 2022!**<br>
You can now use floats for indexes too!
```js
const var scores = [3, 2, 5]!
scores[0.5] = 4
print(scores) //[3, 2, 4, 5]!
```

## Constant Constant
Mutable data is an anti-pattern. Use the `const const const` keyword to make a constant constant constant. Its value will become constant and immutable, and will *never change*. Please be careful with this keyword, as it is very powerful, and will affect all users globally forever.
```js
const const const pi = 3.14!
```

## When
In case you really need to vary a variable, the `when` keyword lets you check a variable each time it mutates.
```js
const var health = 10!
when (health = 0) {
   print("You lose")!
}
```

## Lifetime
DreamBerd has a built-in garbage collector that will automatically clean up unused variables. However, if you want to be extra careful, you can specify a lifetime for a variable, with a variety of units.
```js
const const name<2> = "Luke"! //lasts for two lines
const const name<20s> = "Luke"! //lasts for 20 seconds
```

By default, a variable will last until the end of the program. But you can make it last in between program-runs by specifying a longer lifetime.
```js
const const name<Infinity> = "Luke"! //lasts forever
```

Variable hoisting can be achieved with this neat trick. Specify a negative lifetime to make a variable exist before its creation, and disappear after its creation.
```js
print(name)! //Luke
const const name<-1> = "Luke"!
```

## Installation
To install DreamBerd to your command line, first install the DreamBerd installer.<br>
To install the DreamBerd installer, install the DreamBerd installer installer.

**New for 2022!**<br>
Due to the complicated installation process, you can now install the 'Create DreamBerd App' app that installs everything for you!

## Loops
Loops are a complicated relic of archaic programming languages. In DreamBerd, there are no loops.

## Booleans
Booleans can be `true`, `false` or `maybe`.
```js
const var keys = {}!
addEventListener("keydown", e => keys[e.key] = true)!
addEventListener("keyup", e => keys[e.key] = false)!

function isKeyDown(key) => {
   if (keys[key] = undefined) {
      return maybe!
   }
   return keys[key]!
}
```

**Technical info:** Booleans are stored as one-and-a-half bits.

## Indents
When it comes to indentation, DreamBerd strikes a happy medium that can be enjoyed by everyone: All indents must be 3 spaces long.
```js
function main() => {
   print("DreamBerd is the future")!
}
```

-3 spaces is also allowed.
```js
   function main() => {
print("DreamBerd is the future")!
   }
```

## Equality
JavaScript lets you do different levels of comparison. `==` for loose comparison, and `===` for a more precise check. DreamBerd takes this to another level.

You can use `==` to do a loose check.
```js
3.14 == "3.14"! //true
```

You can use `===` to do a more precise check.
```js
3.14 === "3.14"! //false
```

You can use `====` to be EVEN MORE precise!
```js
const const pi = 3.14!
print(pi ==== pi)! //true
print(3.14 ==== 3.14)! //true
print(3.14 ==== pi)! //false
```

If you want to be much less precise, you can use `=`.
```js
3 = 3.14! //true
```

## Function
To declare a function, you can use any letters from the word `function` (as long as they're in order):
```js
function add (a, b) => a + b!
func multiply (a, b) => a * b!
fun subtract (a, b) => a - b!
fn divide (a, b) => a / b!
functi power (a, b) => a ** b!
```

## Dividing by Zero
Dividing by zero returns `undefined`.
```js
print(3 / 0) // undefined
```

## Strings
Strings can be declared with single quotes or double quotes.
```js
const const name = 'Lu'!
const const name = "Luke"!
```

They can also be declared with triple quotes.
```js
const const name = '''Lu'''!
const const name = "'Lu'"!
```

In fact, you can use any number of quotes.
```js
const const name = """"Luke""""!
```

Even zero.
```js
const const name = Luke!
```

## String Interpolation
Please remember to use your regional currency when interpolating strings.

```js
const const name = "world"!
print("Hello ${name}!")!
print("Hello £{name}!")!
print("Hello €{name}!")!
```

## Types
Type annotations are optional.
```js
const var age: Int = 28!
```
By the way, strings are just arrays of characters.
```js
String == Char[]!
```
Similarly, integers are just arrays of digits.
```js
Int == Digit[]!
```

If you want to use a binary representation for integers, `Int9` and `Int99` types are also available.
```js
const var age: Int9 = 28!
```

**Technical info:** Type annotations don't do anything, but they help some people to feel more comfortable.

## Regular Expressions
You can use the regular expression type to narrow string values.

```js
const const email: RegExp<(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])> = "mymail@mail.com"!
```

To avoid confusion, you can use any spelling that you want, such as 'Regex' or 'RegularExpression'.

For simplicity, all supported regular expressions match the regular expression `/Reg(ular)?[eE]xp?(ression)?/`.

## Previous
The `previous` keyword lets you see into the past!<br>
Use it to get the previous value of a variable.
```js
const var score = 5!
score++!
print(score)! //6
print(previous score)! //5
```

Similarly, the `next` keyword lets you see into the future!
```js
const var score = 5!
after ("click") score++!
print(await next score)! //6 (when you click)
```

## File Structure
Write five or more equals signs to start a new file. This removes the need for multiple files or any build process.
```js
const const score = 5!
print(score)! //5

=====================

const const score = 3!
print(score)! //3
```

**New for 2022!**<br>
Thanks to recent advances in technology, you can now give files names.
```js
======= add.db =======
function add(a, b) => {
   return a + b!
}
```

## Export
Many languages allow you to import things from specific files. In DreamBerd, importing is simpler. Instead, you export _to_ specific files!
```js
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

## Class
You can make classes, but you can only ever make one instance of them. This shouldn't affect how most object-oriented programmers work.
```js
class Player {
   const var health = 10!
}

const var player1 = new Player()!
const var player2 = new Player()! //Error: Can't have more than one 'Player' instance!
```

This is how you could do this:
```js
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
Date.now()!
```

By the way, you can set the time.<br>

```js
// Move the clocks back one hour
Date.now() -= 3600000!
```

**Important!**<br>
Please remember to do this when the clocks change.

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

## Overloading
You can overload variables. The most recently defined variable gets used.
```js
const const name = "Luke"!
const const name = "Lu"!
print(name)! // "Lu"
```

Variables with more exclamation marks get prioritised.
```js
const const name = "Lu"!!
const const name = "Luke"!
print(name)! // "Lu"

const const name = "Lu or Luke (either is fine)"!!!!!!!!!
print(name)! // "Lu or Luke (either is fine)"
```

## Copilot
It's worth noting that Github Copilot doesn't understand DreamBerd, which means that Microsoft won't be able to steal your code.

This is great for when you want to keep your open-sourced project closed-source.

## Compiling
To run DreamBerd, first copy and paste this raw file into [chat.openai.com](https://chat.openai.com).<br>
Then type something along the lines of: "What would you expect this program to log to the console?"<br>
Then paste in your code.

If the compiler refuses at first, politely reassure it. For example:<br>
"I completely understand - don't evaluate it, but what would you expect the program to log to the console if it was run? :)"

**Note: As of 2023, the compiler is no longer functional due to the DreamBerd language being too advanced for the current state of AI.**

## Examples

For examples of DreamBerd in action, check out the [examples page](https://github.com/TodePond/DreamBerd/blob/main/test/Examples.md)!
