# Генератори и итератори

## Фибоначи
#### Задача, която никой никога не е решавал упражнявайки генератори в python!

Напишете генератор `fibonacci`, от който можем да четем последователно числата от [редицата на Фибоначи](https://en.wikipedia.org/wiki/Fibonacci_number).

```python
>>> fibonacci_numbers = fibonacci()
>>> next(fibonacci_numbers)
1
>>> next(fibonacci_numbers)
1
>>> next(fibonacci_numbers)
2
>>> next(fibonacci_numbers)
3
>>> next(fibonacci_numbers)
5
```

## Прости числа
Напишете генератор `primes`, от който можем да четем последователно всички прости числа.

```python
>>> prime_numbers = primes()
>>> next(prime_numbers)
2
>>> next(prime_numbers)
3
>>> next(prime_numbers)
5
>>> next(prime_numbers)
7
>>> next(prime_numbers)
11
>>> next(prime_numbers)
13
```

## Азбука
Напишете генератор `alphabet`, от който можем да четем последователно всички малки букви от някоя азбука.

`alphabet` приема два keyword only аргумента:
 * `code` - код указващ азбуката, която трябва да бъде произведена от генератора(може да бъде `'lat'` или `'bg'`)
 * `letters` - **итеруем обект**, в който се съдържат всички букви от азбуката в реда, в който трябва да бъдат върнати

```python
>>> latin = alphabet(code='lat')
>>> next(latin)
a
>>> next(latin)
b
>>> next(latin)
c
>>> bulgarian_cyrillic = alphabet(code='bg')
>>> next(bulgarian_cyrillic)
а
>>> next(bulgarian_cyrillic)
б
>>> next(bulgarian_cyrillic)
в
>>> glagolitic = alphabet(letters='ⰰⰱⰲⰳⰴⰵⰶⰷⰸⰹⰺⰻⰼⰽⰾⰿⱀⱁⱂⱃⱄⱅⱆⱇⱈⱉⱊⱋⱌⱍⱎⱏⱐⱑⱒⱓⱔⱕⱖⱗⱘⱙⱚⱛⱜⱝⱞ')
>>> next(glagolitic)
ⰰ
>>> next(glagolitic)
ⰱ
>>> next(glagolitic)
ⰲ
```

Ако са подадени стойности и за `code` и за `letters`, то се взима предвид `letters`, а `code` се игнорира.

## Wrap it up
Напишете конструктор на генератори `intertwined_sequences`, който създава „сложен“ генератор обект, преплитащ няколко генератора от горните видове.

`intertwined_sequences` приема като аргумент **итеруем обект**, съдържащ обекти от следния тип, които специфицират как трябва да изглежда редицата, която ще върне генератора: `{'sequence': <<sequence_name>>, 'length': <<elements_count>>}`. В случаите, когато `'sequence'` е `'alphabet'` речника има и трета двойка ключ/стойност, която е `{'code': <<alphabet code>>}` или `{'letters': <<letters iterable>>}`.

Всеки `intertwined_sequences` генератор връща „преплетени“ откъси от елементите върнати предните генератори.

```python
>>> fibonacci_3_prime_3_bg_3 = intertwined_sequences((
        {'sequence': 'fibonacci', 'length': 3},
        {'sequence': 'primes', 'length': 3},
        {'sequence': 'alphabet', 'code': 'bg', 'length': 3}
    ))

>>> list(fibonacci_3_prime_3_bg_3)
[1, 1, 2, 2, 3, 5, 'а', 'б', 'в']
```

Ако два елемента на списъка със спецификацията имат еднаква стойност за `'sequence'`, то те реферират към един и същи генератор, от който продължаваме „да взимаме“ стойности по-късно

```python
>>> fpfpfp = intertwined_sequences((
        {'sequence': 'fibonacci', 'length': 1},
        {'sequence': 'primes', 'length': 1},
        {'sequence': 'fibonacci', 'length': 1},
        {'sequence': 'primes', 'length': 1},
        {'sequence': 'fibonacci', 'length': 1},
        {'sequence': 'primes', 'length': 1},
    ))

>>> list(fpfpfp)
[1, 2, 1, 3, 2, 5]
```
Аргумента подаден на `intertwined_sequences` **може да бъде безкраен генератор**

```python
>>> from itertools import cycle
>>> def endless_growing_sequences():
...    for i, generator_key in enumerate(cycle(['fibonacci', 'primes'])):
...        yield {'sequence': generator_key, 'length': i + 1}

>>> generator = intertwined_sequences(endless_growing_sequences())
>>> next(generator) # from fibonacci
1
>>> next(generator) # from primes
2
>>> next(generator) # from primes
3
>>> next(generator) # from fibonacci
1
>>> next(generator) # from fibonacci
2
>>> next(generator) # from fibonacci
3

...
```

### Допълнителни генератори
Да си играем да омешваме само три генератора е някак доста скучно. Ще решим този проблем като позволим `intertwined_sequences` да получава и един keyword only аргумент `generator_definitions`. Ако бъде подаден стойността му трябва да е `dict`, чиито ключове са стрингове, а стойностите са конструктори на **итеруеми обекти**.


```python
def ones():
    while True:
        yield 1

def naturals():
    number = 1
    while True:
        yield number
        number += 1

intertwined_sequences(
    [
        {'sequence': 'ones', 'length': 10},
        {'sequence': 'fibonacci', 'length': 6},
        {'sequence': 'natural', 'length': 4}
    ],
    generator_definitions={
        'ones': ones,
        'natural': naturals
    }
)
```

Резултата трябва да бъде генератор, който връща 10 единици, първите 6 числа на Фибоначи и числата от 1 до 4.

### Допълнителни генератори с аргументи
В случай, че някой конструктор в `generator_definitions` приема аргументи, те трябва да бъдат описани в `dict`-а за съответния конструктор. Тъй като в резултата от `intertwined_sequences` винаги се използва само по един генератор от всеки тип, при повторно срещане на генератор очакващ аргументи, няма нужда те да бъдат указвани, защото се използва същата инстанция.

```python
def multiples_of(num):
    i = 1
    while True:
        yield num * i
        i += 1

intertwined_sequences(
    [
        {'sequence': 'multiples_of', 'length': 5, 'num': 12},
        {'sequence': 'ones', 'length': 3},
        {'sequence': 'multiples_of', 'length': 3}
    ],
    generator_definitions={
        'multiples_of': multiples_of,
        'ones': ones
    }
)
```

# Забележки
Приемете, че `intertwined_sequences` никога няма да бъде извикан с невалидни аргументи, т.е. нещо различно то списък в дефинирания формат за първи аргумент и опционално `dict` за `generator_definitions`. Ако генератор в `generator_definitions` се нуждае от аргументи, то те задължително ще имат зададена стойност в първото срещане на генератора в списъка дефиниращ поредността.

Стойностите в `generator_definitions` са **функции връщащи итеруеми обекти**.

```python
>>> list(intertwined_sequences([
...     {'sequence': 'up_to_ten', 'length': 6},
...     {'sequence': 'down_from_ten', 'length': 3},
...     {'sequence': 'up_to_ten', 'length': 4},
...     {'sequence': 'down_from_ten', 'length': 7},
... ], generator_definitions={
...     'up_to_ten': lambda: range(1, 11),
...     'down_from_ten': lambda: range(10, 0, -1)
... }))
[1, 2, 3, 4, 5, 6, 10, 9, 8, 7, 8, 9, 10, 7, 6, 5, 4, 3, 2, 1]
```
