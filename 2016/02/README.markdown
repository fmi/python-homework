# Аритметични изрази

Смятането на дълги аритметични изрази е тегава и мъчна работа. За щастие за такива задачи имаме компютри(които някой ден ще осъзнаят, че биват експлоатирани да вършат мръсната ни работа и ще въстанат срещу нас, но не това е важно сега). Ще се възползваме от този факт, за да улесним значително живота си.

От вас се изисква да реализирате четири функции:

 * `create_constant(value)` - връща обект, който представлява константа
 * `create_variable(name)` - връща обект, който представлява променлива, аргумента `name` указва какво да бъде името ѝ.
 * `create_operator(symbol, function)` - връща обект, който представлява бинарен оператор. `symbol` е символа, с който въпросния оператор се изписва, а `function` е функция с два аргумента, която реализира изпълнението на оператора.
 * `create_expression(expression_structure)` - връща обект, който представлява аритметичен израз. `expression_structure` е итеруемо от итеруеми, което описва желания израз.

### Код > думи

```python
>>> plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
>>> minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
>>> times = create_operator('*', lambda lhs, rhs: lhs * rhs)
>>> six = create_constant(6)
>>> nine = create_constant(9)
>>> expression = create_expression((six, times, nine))
```

Изразът, който получаваме от `create_expression` трябва да има метод `evaluate(**variables)`. Той приема keyword аргументи за стойностите на променливите в израза и връща като резултат стойността на израза при тези стойности.

### Код > думи

```python
>>> x = create_variable('x')
>>> y = create_variable('y')
>>> added_expression = create_expression((x, plus, y))
>>> added_expression.evaluate(x=5, y=3)
8
```

Разбира се изразите могат да са доста по-интересни

```python
>>> expression = create_expression((six, times, ((x, minus, y), plus, nine)))
```

Изразите трябва да имат атрибут `variable_names`, който е итеруемо с имената на всички променливи в израза.


```python
>>> added_expression.variable_names == ('x',)
True
```

## Оператори
Обектите ни представляващи константи, променливи и изрази трябва да могат да се събират/изваждат/умножават/делят. Логично, резултатът от такава операция трябва да бъде израз:


```python
>>> y = create_variable('y')
>>> twelve = create_constant(12)
>>> expression = y + twelve
>>> expression.variable_names
('y',)
>>> expression.evaluate(y=3)
15
```

Същото се отнася и за операции приложени върху литерали от езика:

```python
>>> x = create_variable('x')
>>> y = create_variable('y')
>>> (x + 3 * (y - 2)).evaluate(x=1, y=4)
7
```

## Четимост
Добра идея е да можем да четем изразите, които създаваме, за да можем да верифицираме какво правим. Всеки от обектите ни трябва да може да се конвертира до низ.

```python
>>> x = create_variable('x')
>>> y = create_variable('y')
>>> twelve = create_constant(12)
>>> times = create_operator('*', lambda lhs, rhs: lhs * rhs)
>>> plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
>>> expression = create_expression((x, plus, (y, times, twelve)))
>>> print(x)
x
>>> print(y)
y
>>> print(twelve)
12
>>> print(times)
*
>>> print(plus)
+
>>> print(expression)
(x + (y * 12))

```

## Оценяване
Всяко нещо, което има смисъл да може да се оцени, следва да може да се оцени. Т.е. освен за изразите очакваме променливите и константите също да могат да се оценяват.

```python
>>> x = create_variable('x')
>>> five = create_constant(5)
>>> five.evaluate()
5
>>> x.evaluate(x=42)
42
```

Ако на `evaluate` бъдат подадени допълнителни именовани аргументи, за които нямаме променливи, това очевидно не трябва да е проблем.


## Бонус
Ако всичко това ви се струва скучно и лесно(както и би трябвало), може да се позабавлявате със следния въпрос: Има ли смисъл от няколко различни оператора за събиране? По-скоро не.

Помислете как можете да не създавате много различни инстанции на един и същи оператор.
