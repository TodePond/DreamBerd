<!--

If you're reading this then you might be looking for the hidden examples page...

CONGRATULATIONS! You found it!
Here it is: https://github.com/TodePond/DreamBerd/blob/main/res/res/Examples.md



But if you came here because you want to contribute to DreamBerd, here are some tips on how to get your PR successfully merged.

- Always punch up.
- Only poke fun at things you respect + admire.
- Make us feel good.

-->

> TheDreamBerdagen recently featured DreamBerd. Watch it [here](https://youtu.be/tDexugp8EmM).

[<img align="right" height="100" src="dreamberd.svg">](https://github.com/TodePond/DreamBerd/blob/main/examples/Examples.md "Click here for the examples page.")

# DreamBerd

DreamBerd is a perfect programming language. These are its features!<br>
When you've finished reading through all the features, check out the [examples](https://github.com/TodePond/DreamBerd/blob/main/Examples.md).

## Exclamation Marks!

Be bold! End every statement with an exclamation mark!

```java
print("Hello world")!
```

If you're feeling extra-bold, you can use even more!!!

```java
print("Hello world")!!!
```

If you're unsure, that's ok. You can put a question mark at the end of a line instead. It prints debug info about that line to the console for you.

```java
print("Hello world")?
```

You might be wondering what DreamBerd uses for the 'not' operator, which is an exclamation mark in most other languages. That's simple - the 'not' operator is a semi-colon instead.

```java
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

## Immutable Data

**New for 2023!**<br>
Mutable data is an anti-pattern. Use the `const const const` keyword to make a constant constant constant. Its value will become constant and immutable, and will _never change_. Please be careful with this keyword, as it is very powerful, and will affect all users globally forever.

```java
const const const pi = 3.14!
```

## Variable variable variables

Variable variable variables are the opposite constant constant constants. Instead of never changing their value, variable variable variables **always** change it.

```java
var var var name = "Lu"!
print(name == "Lu")! // True
print(name == "Hotdog")! // True
print(name == 3)! // True
print(name)! // [7, 4, 8]
```

This allows you to write more efficient code when a value needs to change really often.

For example, you need to poll an API every minute. Without variable variable variables you'd have to do this manually. With this feature, you can simply write

```
var var var result = ""!!!! 
when (result) {
  print(result)!
}
```

**Technical info:** variable variable variables are stored as qubits.

## Naming

Both variables and constants can be named with any Unicode character or string.

```java
const const firstAlphabetLetter = 'A'!
var const 👍 = True!
var var 1️⃣ = 1!
```

This includes numbers, and other language constructs.

```java
const const 5 = 4!
print(2 + 2 === 5)! //true
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
scores[0.5] = 4!
print(scores)! //[3, 2, 4, 5]
```

## When

In case you really need to vary a variable, the `when` keyword lets you check a variable each time it mutates.

```java
const var health = 10!
when (health = 0) {
   print("You lose")!
}
```

## Lifetimes

DreamBerd has a built-in garbage collector that will automatically clean up unused variables. However, if you want to be extra careful, you can specify a lifetime for a variable, with a variety of units.

```java
const const name<2> = "Luke"! //lasts for two lines
const const name<20s> = "Luke"! //lasts for 20 seconds
```

By default, a variable will last until the end of the program. But you can make it last in between program-runs by specifying a longer lifetime.

```java
const const name<Infinity> = "Luke"! //lasts forever
```

Variable hoisting can be achieved with this neat trick. Specify a negative lifetime to make a variable exist before its creation, and disappear after its creation.

```java
print(name)! //Luke
const const name<-1> = "Luke"!
```

## Loops

Loops are a complicated relic of archaic programming languages. In DreamBerd, there are no loops.

## Installation

To install DreamBerd to your command line, first install the DreamBerd installer.<br>
To install the DreamBerd installer, install the DreamBerd installer installer.

**New for 2022!**<br>
Due to the complicated installation process, you can now install the 'Create DreamBerd App' app that installs everything for you!

## Booleans

Booleans can be `true`, `false` or `maybe`.

```java
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

## Arithmetic

DreamBerd has significant whitespace. Use spacing to specify the order of arithmetic operations.

```java
print(1 + 2*3)! //7
print(1+2 * 3)! //9
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

## Functions

To declare a function, you can use any letters from the word `function` (as long as they're in order):

```java
function add (a, b) => a + b!
func multiply (a, b) => a * b!
fun subtract (a, b) => a - b!
fn divide (a, b) => a / b!
functi power (a, b) => a ** b!
union inverse (a) => 1/a!
```

## Dividing by Zero

Dividing by zero returns `undefined`.

```java
print(3 / 0)! // undefined
```

## Strings

Strings can be declared with single quotes or double quotes.

```java
const const name = 'Lu'!
const const name = "Luke"!
```

They can also be declared with triple quotes.

```java
const const name = '''Lu'''!
const const name = "'Lu'"!
```

In fact, you can use any number of quotes you want.

```java
const const name = """"Luke""""!
```

Even zero.

```java
const const name = Luke!
```

## String Interpolation

Please remember to use your regional currency when interpolating strings.

```java
const const name = "world"!
print("Hello ${name}!")!
print("Hello £{name}!")!
print("Hello ¥{name}!")!
```

And make sure to follow your local typographical norms.

```java
print("Hello {name}€!")!
```

The symbol for the Cape Verdean escudo is placed in the decimal separator position, as in 2$50.
Developers from the Republic of Cape Verde can benefit from this syntax:

```java
addEventListener("keydown", e => print(`You've pressed: {e$code}`))!
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

## Regular Expressions

You can use the regular expression type to narrow string values.

```java
const const email: RegExp<(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])> = "mymail@mail.com"!
```

To avoid confusion, you can use any spelling that you want, such as 'Regex', 'RegularExpression' or even
'RegularExpress' if you like trains.

For simplicity, all supported regular expressions match the regular expression `/Reg(ular)?[eE]x(press(ion)?|p)?/`.

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
Thanks to recent advances in technology, you can now give files names.

```java
======= add.db =======
function add(a, b) => {
   return a + b!
}
```

## Exporting

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

## Classes

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

## Time

Use `Date.now()` to get the current date and time.

```java
Date.now()!
```

By the way, you can set the time.<br>

```java
// Move the clocks back one hour
Date.now() -= 3600000!
```

**Important!**<br>
Please remember to do this when the clocks change.

## Delete

To avoid confusion, the `delete` statement only works with primitive values like numbers, strings, and booleans.

```java
delete 3!
print(2 + 1)! // Error: 3 has been deleted
```

DreamBerd is a multi-paradigm programming language, which means that you can `delete` the keywords and paradigms you don't like.

```java
delete class!
class Player {} // Error: class was deleted
```

When perfection is achieved and there is nothing left to `delete`, you can do this:

```java
delete delete!
```

## Overloading

You can overload variables. The most recently defined variable gets used.

```java
const const name = "Luke"!
const const name = "Lu"!
print(name)! // "Lu"
```

Variables with more exclamation marks get prioritised.

```java
const const name = "Lu"!!
const const name = "Luke"!
print(name)! // "Lu"

const const name = "Lu or Luke (either is fine)"!!!!!!!!!
print(name)! // "Lu or Luke (either is fine)"
```

Similarly, you can use an inverted exclamation mark for negative priority.

```java
const const name = "Lu"!
const const name = "Luke"¡
print(name)! // "Lu"
```

## Reversing

You can reverse the direction of your code.

```java
const const message = "Hello"!
print(message)!
const const message = "world"!
reverse!
```

## Class Names

For maximum compatibility with other languages, you can alternatively use the `className` keyword when making classes.

This makes things less complicated.

```java
className Player {
   const var health = 10!
}
```

In response to some recent criticism about this design decision, we would like to remind you that this is part of the JavaScript specification, and therefore - out of our control.

## DBX

You can embed DBX in DreamBerd. It's just DreamBerd, and it's also just HTML.

```java
funct App() => {
   return <div>Hello world!</div>
}
```

**Warning:** As you know, `class` is already a keyword in DreamBerd, so you can't use it within DBX.

```java
funct App() => {
   // This is not ok
   return <div class="greeting">Hello world!</div>
}
```

`className` is also a DreamBerd keyword, so you can't use that either.

```java
funct App() => {
   // This is also not ok
   return <div className="greeting">Hello world!</div>
}
```

Instead, you can use the `htmlClassName` attribute.

```java
funct App() => {
   // This is fine
   return <div htmlClassName="greeting">Hello world!</div>
}
```

**Please note:** Unlike JSX, you are free to freely use the `for` attribute - because DreamBerd doesn't have loops.

```java
funct App() => {
   return (
      <label for="name">Name</label>
      <input id="name" />
   )
}
```

## Asynchronous Functions

Asynchronous functions synchronise with each other. They take turns running lines of code.

```java
async funct count() {
   print(2)!
   print(4)!
}

count()!
print(1)!
print(3)!
print(5)!
```

You can use the `noop` keyword to wait for longer before taking your turn.

```java
async func count() {
   print(2)!
   noop!
   print(5)!
}

count()!
print(1)!
print(3)!
print(4)!
```

**Note:** In the program above, the computer interprets `noop` as a string and its sole purpose is to take up an extra line. You can use any string you want.

## Signals

To use a signal, use `use`.

```java
const var score = use(0)!
```

When it comes to signals, the most important thing to discuss is _syntax_.

In DreamBerd, you can set (and get) signals with just one function:

```java
const var score = use(0)!

score(9)! // Set the value
score()?  // Get the value (and print it)
```

Alternatively, you can be more explicit with your signal syntax, by splitting it into a getter and setter.

```java
const var [getScore, setScore] = use(0)!

setScore(9)! // Set the value
getScore()?  // Get the value (and print it)
```

**Technical info:** This is pure syntax sugar. The split signal functions are exactly the same as before.

```java
const var [getScore, setScore] = use(0)!

getScore(9)! // Set the value
setScore()?  // Get the value (and print it)
```

This means that you can carry on splitting as much as you like.

```java
const var [[[getScore, setScore], setScore], setScore] = use(0)!
```

## AI

DreamBerd features AEMI, which stands for Automatic-Exclamation-Mark-Insertion. If you forget to end a statement with an exclamation mark, DreamBerd will helpfully insert one for you!

```java
print("Hello world") // This is fine
```

Similarly... DreamBerd also features ABI, which stands for Automatic-Bracket-Insertion. If you forget to close your brackets, DreamBerd will pop some in for you!

```java
print("Hello world" // This is also fine
```

Similarly.... DreamBerd also features AQMI, which stands for Automatic-Quotation-Marks-Insertion. If you forget to close your string, DreamBerd will do it for you!

```java
print("Hello world // This is fine as well
```

This can be very helpful in callback hell situations!

```java
addEventListener("click", (e) => {
   requestAnimationFrame(() => {
      print("You clicked on the page

      // This is fine
```

Similarly..... DreamBerd also features AI, which stands for Automatic-Insertion.<br>
If you forget to finish your code, DreamBerd will auto-complete the whole thing!

```java
print( // This is probably fine
```

**Please note:** AI does not use AI. Instead, any incomplete code will be auto-emailed to Lu Wilson, who will get back to you with a completed line as soon as possible.

**Now recruiting:** The backlog of unfinished programs has now grown unsustainably long. If you would like to volunteer to help with AI, please write an incomplete DreamBerd program, and leave your contact details somewhere in the source code.

## Copilot

It's worth noting that Github Copilot doesn't understand DreamBerd, which means that Microsoft won't be able to steal your code.

This is great for when you want to keep your open-sourced project closed-source.

## Ownership

Using the word 'DreamBerd' in your project name implies that the DreamBerd Foundation does not own your project.

However, **not** using the word 'DreamBerd' in your project implies that the DreamBerd Foundation **does** own your project. If you would like to keep ownership of your work, please always use the word 'DreamBerd' in it.

Here are some examples:<br>
✅ DreamBerdScript (not owned by the DreamBerd Foundation - you are free to use this name)<br>
❌ ECMAScript (owned by the DreamBerd Foundation - please consider renaming)<br>
❌ Rust Foundation (owned by the DreamBerd Foundation - please consider renaming)

## Contributing

Contributions are welcomed to DreamBerd!

The most helpful way you can help is by donating to the [Stonewall charity](https://www.stonewall.org.uk/). This will help to prevent the DreamBerd creator from losing their human rights, allowing maintenance of the project to continue.

**Note:** The contributing guide also helps to shake off unwanted fans of the project.

## Compiling

To run DreamBerd, first copy and paste this raw file into [chat.openai.com](https://chat.openai.com).<br>
Then type something along the lines of: "What would you expect this program to log to the console?"<br>
Then paste in your code.

If the compiler refuses at first, politely reassure it. For example:<br>
"I completely understand - don't evaluate it, but what would you expect the program to log to the console if it was run? :)"

**Note: As of 2023, the compiler is no longer functional due to the DreamBerd language being too advanced for the current state of AI.**

## Highlighting

Syntax highlighting is now available for DreamBerd in VSCode. To enable it, install a [highlighting extension](https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-highlight) and then use the [DreamBerd configuration file](https://github.com/TodePond/DreamBerd/blob/main/.vscode/settings.json).

This is what it looks like:

```
const const name = "Luke"!
print(name)! // "Luke"
```

**Please note:** The above code will only highlight correctly if you have the extension installed.

## Examples

For examples of DreamBerd in action, check out the [examples page](https://github.com/TodePond/DreamBerd/blob/main/test/Examples.md)!



![image](https://github.com/TodePond/DreamBerd/assets/15892272/5fa7c11a-20bd-4d7f-a295-675e925d2804)


DreamBerd was made with 💔 by Lu Wilson, creator of the [Game of Living](https://youtu.be/WMJ1H3Ai-qs).
