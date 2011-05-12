# Multi Dispatch

Ако в C++ имате йерархия и извикате някакъв метод в нея, C++ определя кой точно ще бъде извикан по време на компилация. Това зависи от типа на reference-а, а не от типа обекта. Ако искате метода да се определя по време на изпълнение, трябва да го маркирате с `virtual`. Това се нарича *dynamic dispatch*, понеже "dispatch-а" (кой метод да се извика) се определя "dynamic-но" (по време на изпълнение). Начира се още *single dispatch*, избора зависи само от обекта, на който сте извикали метода. *Multi dispatch* е когато избора зависи и от аргументите. Това може да се реализира с *visitor pattern*.

Или ако пишете на Python, с декоратор.

## Задание

Дефинирайте декоратор `multimethod`:

    class Asteroid: pass
    class Spaceship: pass
    class CollisionDetector:
        @multimethod
        def collide(self, a: Spaceship, b: Spaceship):
            print("Two spaceships")
    
        @collide.multimethod
        def collide(self, a: Spaceship, b: Asteroid):
            print("A spaceship and an asteroid")
    
        @collide.multimethod
        def collide(self, a: Asteroid, b: Spaceship):
            self.collide(b, a)
    
        @collide.multimethod
        def collide(self, a: Asteroid, b: Asteroid):
            print("Two asteroids")
    
    a = Asteroid()
    s = Spaceship()
    
    detector = CollisionDetector()
    
    detector.collide(a, a) # Two asteroids
    detector.collide(s, a) # A spaceship and an asteroid
    detector.collide(s, s) # Two spaceships

## Правилата

* Първия метод се декорира с `@multimethod`
* Остналите методи се декорират с `@foo.multimethod`, където `foo` е името на метода. Точно както `property`
* Всички методи трябва да имат едно и също име. В противен случай пораждайте `NameError`
* Параметрите на методите могат да се анотират с типове
* Ако един параметър не е анотиран, то приемайте, че е анотиран с `object`
* Мултиметод може да се извика ако всичките му аргументи са инстанции на типовете в анотацията (`isinstance`)
* Ако има няколко мултиметода, които могат да бъдат извикани за дадени аргументи, винаги се извиква първия дефиниран
* Ако нито един метод не е подходящ за дадени аргументи, пораждайте `LookupError`
* `self`, `*args` и `**kwargs` нито се анотират, нито се вземат предвид в определянето на метода

## Друг пример

    class Spam:
        @multimethods
        def eggs(self, a: int, b: int):
            print("1")
    
        @eggs.multimethods
        def eggs(self, a, b: int):
            print("2")
    
        @eggs.multimethods
        def eggs(self, a: str, b):
            print("3")
    
        @eggs.multimethods
        def eggs(self, a: object, b: object):
            print("4")
    
        @eggs.multimethods
        def eggs(self, a: float, b: float):
            print("5")
    
    spam = Spam()
    spam.eggs(420, 420) # 1
    spam.eggs('x', 420) # 2
    spam.eggs('x', 'x') # 3
    spam.eggs(1.0, 'x') # 4
    spem.eggs(1.0, 1.0) # 1
