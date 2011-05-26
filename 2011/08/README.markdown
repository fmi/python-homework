# Класика и джаз

Представете си, че имаме каталог с музиката, която слушаме. Искаме да му задаваме въпроси от рода на:

* Дай ми всички песни на този изпълнител.
* Дай ми всички меланхолични джаз песни.
* Дай ми всички песни, които имат буквата “е”.
* Дай ми всички песни, в които има саксофон.

Всяка песен в нашия каталог има следните неща:

* name – Име (`"My Favourite Things"`)
* artist – Изпълнител или композитор (`"John Coltrane"`)
* genre – Жанр с опционален поджанр (`"Jazz"`)
* subgenre – Поджанр (опционален; `"Bebop"`)
* tags – Етикети (множество от низове `{'saxophone', 'popular', 'jazz', 'bebop', 'cover'}`)

Песните са записани в текстов файл със следния формат:

<pre class="plain">My Favourite Things;    John Coltrane;      Jazz, Bebop;        popular, cover
Greensleves;            John Coltrane;      Jazz, Bebop;        popular, cover
Alabama;                John Coltrane;      Jazz, Avantgarde;   melancholic
Acknowledgement;        John Coltrane;      Jazz, Avantgarde;
Afro Blue;              John Coltrane;      Jazz;               melancholic
'Round Midnight;        John Coltrane;      Jazz;
My Funny Valentine;     Miles Davis;        Jazz;               popular
Tutu;                   Miles Davis;        Jazz, Fusion;
Miles Runs The Voodo Down; Miles Davis;     Jazz, Fusion;
Boplicity;              Miles Davis;        Jazz, Bebop;
Autumn Leaves;          Bill Evans;         Jazz;               popular
Waltz for Debbie;       Bill Evans;         Jazz;
'Round Midnight;        Thelonious Monk;    Jazz, Bebop;
Ruby, My Dear;          Thelonious Monk;    Jazz;               saxophone
Fur Elise;              L.v. Beethoven;     Classical;          popular
Moonlight Sonata;       L.v. Beethoven;     Classical;          popular
Pathetique;             L.v. Beethoven;     Classical;
Toccata e Fuga;         J.S. Bach;          Classical, Baroque; popular
Goldberg Variations;    J.S. Bach;          Classical, Baroque;
Eine Kleine Nachtmusik; W.A. Mozart;        Classical;          popular, violin
</pre>

* Стойностите са разделени с точка и запетая (;)
* Може да има повторения както в имена на песни, така и на артисти
* Жанрът и поджанрът са в едно поле, като вторият е опционален. Ако го има, разделени са със запетая.
* Последното поле е списък от етикети, разделени със запетаи. Може да е празно.
* Освен от изрично изброените, една песен може да получава етикети от две други места – артист и жанрове.

Знаем, че всички песни на Колтрейн имат саксофон, а пък Бах пише полифонична музика за пиано. Затова, освен този файл, имаме и такъв речник:

    artist_tags = {
      "John Coltrane": {'saxophone'},
      "J.S. Bach": {'piano', 'polyphony'},
    }

Горното казва, че всички песни на Колтрейн трябва да имат етикет `saxophone`, а всички на Бах – етикети `piano` и `polyphony`.

Жанрът и поджанрът трябва също да дават етикети. Ако една песен е “Jazz, Bebop”, тя трябва да получи етикетите `jazz` и `bebop` (изцяло малки букви). Ако е само “Jazz”, получава само един етикет – `jazz`.

## Идеята

Първо трябва да създадете обекти, които представят песен. Няма значение от какъв клас са, стига да имат следните методи:

    # My Favourite Things;    John Coltrane;      Jazz, Bebop;        popular
    song.name     # "My Favourite Things"
    song.artist   # "John Coltrane"
    song.genre    # "Jazz"
    song.subgenre # "Bebop"
    song.tags     # {'popular', 'jazz', 'bebop', 'saxophone'}
    
    # Eine Kleine Nachtmusik; W.A. Mozart;        Classical;          popular
    song.name     # "Eine Kleine Nachtmusik"
    song.artist   # "W.A. Mozart"
    song.genre    # "Classical"
    song.subgenre # None
    song.tags     # {'classical', 'popular'}

Трябва да дефинирате клас, представящ музикалната колекция:

    collection = Collection(file_contents_as_string, artist_tags)

`file_contents_as_string` е текстовият файл, прочетен в низ.

Колекциите трябва да дефинират метод `find`:

    class Collection:
        def find(self, result, **what):
            pass
        
Няколко примера как трябва да работи find:

    # Намира всички песни с етикет jazz:
    collection.find('songs', tags='jazz')
    
    # Намира всички песни, които имат двата етикета jazz и piano:
    collection.find('songs', tags={'jazz', 'piano'})
    
    # Намира всички песни, които имат етикет jazz и нямат етикет piano:
    collection.find('songs', tags={'jazz', 'piano!'})
    
    # Намира всички популярни песни на Джон Колтрейн:
    collection.find('songs', tags='popular', artist="John Coltrane")
    
    # Връща имена на песни, които започват с думичката "My":
    collection.find('songs', name=re.compile(r'^My\b'))
    
    # Връща имената на всички артисти, които имат поне една песен с етикет jazz:
    collection.find('artists', tags='jazz')
    
    # Намира всички класически песни с по-дълги имена:
    collection.find('songs', filter=(lambda song: len(song.name) > 15), tags='classical')
    
## Спецификацията
Да се създаде клас `Collection`, със:

* Конструктор, вземащ два аргумента
  * Първият е текстов низ, съдържащ каталог с песни, във показания по-горе формат.
  * Вторият е речник, съпоставящ име на артист (низ) с етикети (множенство от низове), които всички негови песни трябва да имат.
* Метод `find(self, result, **what)`. `what` дефинира кои песни да се търсят, докато `result` – под каква форма да се върне информацията за тях.
* `what['tags']` – Съдържа символ или списък от символи. Ограничава резултатите до песни, притежаващи всички етикети. Ако някой етикет завършва на удивителна (!), ограничава песните до тези, които нямат този етикет.
* `what['name']` – Низ или регулярен израз. Ако е низ, ограничава до песни, чието име съвпада с низа. Ако е регулярен израз, ограничава до песни, за които има съвпадение с регулярния израз. `{'name': 'My'}` ограничава до песни, които се казват “My”. `{'name': re.compile('My') }` ограничава до песни, съдържащи подниза `"My"`.
* `what['artist']` – Аналогично на предното, но за име на изпълнител.
* `what['filter']` – Ламбда или списък от ламбди. Всяка приема един аргумент, който е песен (с изброените горе методи) и връща булева стойност. find трябва да ограничи резултатите до песни, за които всички ламбди са върнали истина.
* Обърнете внимание, че критериите са конюнктивни. Търсят се песни, които отговарят на всички.
* Ако result е низът `'songs'`, методът връща списък от песни, отговарящи на зададените критерии.
* Ако result е някой от символите `'name'`, `'artist'`, `'genre'` или `'subgenre'` , `find` връща списък от низове, които съдържат съответно имената, изпълнителите, жанровете или поджанровете на песните. В този списък не трябва да има повторения.
* Може би е очевидно, но ако няма резултати, връщате празен списък. Ако има един резултат, връщате списък с един елемент.
* Редът на върнатите обекти няма значение.
* Ако `find` се извика с празен речник за `what`, връща всички песни (всички артисти, всички жанрове и т.н.).
* Няма никакво значение какво точно ще бъдат песните, стига да имат посочените пет атрибута.