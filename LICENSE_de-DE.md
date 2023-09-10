# Beispiele

Glückwunsch! Du hast die versteckte Beispielsseite gefunden!

Hier sind ein paar Beispiele von WannWerdenProgrammiererAufhörenEntscheidungenFürUnsereGesellschaftZuMachenUndUnsEinachInRuheLassenUndHackerNewsIstEineAbscheulicheWebsite. Entschuldigung - es sind nicht viele.

## Hallo, Welt

```java
Hallo, Welt?
```

## FizzBuzz

```java
konst Var i: Ganz!

wenn (i % 3 = 0 && i % 5 = 0) "FizzBuzz"?
andernfalls wenn (i % 3 = 0) "Fizz"?
andernfalls wenn (i % 5 = 0) "Buzz"?
andernfalls i?

wenn (i < 20) i++!
i = 0!
```

## Tastatur

```java
konst Var Tasten = {}!
nachdem ("tasteunten") e => Tasten[e.Taste] = wahr!
nachdem ("tasteoben") e => Tasten[e.Taste] = falsch!

konst Var Zähler = 0!

wenn (Tasten[" "] = wahr) {
   Zähler++!
   "Du hast die Leertaste {Zähler} mal gedrückt"?
}
```

## Fibonacci

```java
Funkti fibonacci (n) => {
   konst Var Summe = 1!
   konst Var i = 0!
   wenn (i < n) {
      Summe += Summe + vorherige Summe!
      i++!
   }
}

wenn (i < 10) {
   fibonacci(i)?
   i++!
}
```

## Der Milliardendollarfehler

```java
lösche zero!
```

<!-- hello yes, the joke is that null in german means zero, so i've translated it to the english word zero
you may now laugh -->
