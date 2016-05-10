#Статичен анализ на python код

Няма нищо по-досадно от зле написан код. От друга страна хората сме крайно
несъвършени същества, в следствие на което и кода, който пишем е крайно
несъвършен.

Като програмисти обаче, ние знаем че всеки проблем може да бъде поне частично
решен с добър инструмент, който да автоматизира досадните части от задачите ни.
Сега ще си напишем малък инструмент, с който да хващаме някои по-очевидни
недомислици, които всички често допускаме в кода си.

Напишете функция `critic(code, **rules)`, където `code` е текстов низ, който
представлява код на python, а `rules` са различни правила, на които искаме да
отговаря въпросния код. Резултатът от извикването на функцията трябва да е
речник, в който са описани откритите в кода проблеми.

## Правила
Правилата, които трябва да проверява функцията и съответните им стойности по
подразбиране са следните:

 * `line_length=79` - максимална допустима дължина на ред. Всеки ред от
   подадения код трябва да е не по-дълъг от определения брой символи.
 * `forbid_semicolons=True` - да се отчита ли като грешка когато няколко
   логически реда да са написани на един, разделени с `;`.
 * `max_nesting=None` - максималното ниво на влагане
 * `indentation_size=4` - брой `<Space>` символи, с които трябва да са
   индентирани блоковете код
 * `methods_per_class=None` - максимален брой методи в клас.
 * `max_arity=None` - максимален брой аргументи на функции/методи.
 * `forbid_trailing_whitespace=True` - да се отчитат ли като грешка whitespace
   символи в края на реда.
 * `max_lines_per_function=None` - максимален брой **логически** редове в
   тялото на функция/метод.

## Резултат
Върнатия речник трябва да има за ключове номерата на редовете, на които са
открити проблеми. Стойността за всеки от тези ключове трябва да е итеруемо с
текстови низове, описващи проблемите на този ред.

## Съобщения за грешка
Съобщенията за всеки вид грешка трябва да са съответно:

 * твърде дълъг ред: `'line too long (<<actual>> > <<allowed>>)'` 
 * редове с точка и запетая: `'multiple expressions on the same line'`
 * твърде много влагания: `'nesting too deep (<<actual>> > <<allowed>>)'`
 * неправилна индентация: `'indentation is <<actual>> instead of <<size>>'`
 * твърде много методи в клас: `'too many methods in class(<<actual>> > <<allowed>>)`
 * твърде много аргументи на функция/метод: `'too many arguments(<<actual>> > <<allowed>>)'`
 * при оставени празни символи: `'trailing whitespace'`
 * при функции с твърде много редове: `'method with too many lines (<<actual>>
   > <<allowed>>)'` (трябва да се отнася за реда, на който е `def`-а на функцията)

## Примери
```python
>>> critic('''def ugly(indent):
     return indent
''')
{2: {'indentation is 5 instead of 4'}}
```

```python
>>> critic('a = 5; b = 6')
{1: ('multiple expressions on the same line')}
```

```python
>>> solution.critic('''def some_func():
    a_variable = 'some text'; another_variable = 'some more text'; even_moar_variables = 'just for to pass the time'
''')
{2: ('line too long (116 > 79)', 'multiple expressions on the same line')}
```

```python
>>> solution.critic('''def some_func():
    a_variable = 'some text'; another_variable = 'some more text'; even_moar_variables = 'just for to pass the time'
    for char in a_variable:
        if char != 'a':
            for _ in range(10):
                print('SOOOO MUUUCH INDENTATION')
''', max_nesting=3)
{2: ('line too long (116 > 79)', 'multiple expressions on the same line'),
 6: {'nesting too deep (4 > 3)')}
```

### Отговори на очаквани въпроси
 * Няма значение от какъв тип точно е итеруемото с грешките.
 * Ако изберете тип с подредба, няма значение каква е подредбата на грешките,
   стига да са всичките за този ред.
 * Съобщенията трябва да са изписани по абсолютно същия начин, защото
   автоматизирани тестове.
 * Максималното ниво на влагане, което се среща в следния код е 1:
```python
def f   return {
        'name': 'Foo',
        'friends': [
            'bar',
            'baz',
        ],
    }
```


### Полезности
 * [Документацията на ast модула](https://docs.python.org/3/library/ast.html)
 * [greentreesnakes](https://greentreesnakes.readthedocs.io/en/latest/)
