#In-memory файлова система

За целите на това домашно ще се престорим на нещо като файлова система.

## FileSystem
Всяка файлова система ще дава като интерфейс чрез който да може да се създават, трият и местят файлове, директории и твърди и символни връзки.

Ще използваме Unix нотацията за пътища, т.е. всяка файлова система има за корен '/', а пътищата се изписват в следния вид:

    /path/to/some/file

Създайте клас `FileSystem`, който да реализира въпросния интерфейс.

При конструирането си обект от този клас трябва да очаква единствен аргумент указващ размера на файловата система в байтове.

```python
sda1 = FileSystem(250 * (1024 ** 3)) # initialize a 250GB file system
```

Първоначално конструираната файлова система няма никакви файлове и директории в себе си освен празната root директория(`/`).
Трябва да можем да достъпваме следните атрибути на `FileSystem` обектите:

  * `size` - общия размер на системата, зададен при конструирането
  * `available_size` - останало свободно пространство на системата

`FileSystem` обектите трябва да имат следните методи:

  * `get_node(path)` - връща обект(файл или директория) намиращ се на определения път. Ако няма такъв хвърля `NodeDoesNotExistError`.
  * `create(path, directory=False, content='')` - създава файл или директория на дадения път. Ако създаваме файл, то `content` указва какво ще се съдържа в него, за директории стойността на `content` няма смисъл.
    * Ако пътя до директорията, в която трябва да създадем новия обект не съществува, трябва да се хвърли `DestinationNodeDoesNotExistError`.
    * При опит за създаване на файл или директория, който би довел до изчерпване на наличното пространство трябва да се хвърля `NotEnoughSpaceError` и самото създаване да не се случва.
    * Ако на пътя вече съществува файл или директория трябва да се хвърли `DestinationNodeExistsError`
  * `remove(path, directory=False, force=True)` - изтрива това, към което сочи въпросния път.
    * Ако `path` сочи към директория, то `directory` трябва да е изрично указан като `True`, в противен случай да се хвърля изключение от тип `NonExplicitDirectoryDeletionError`.
    * Ако `directory` е `True`, но директорията не е празна, то и `force` трябва да е `True`, за да се случи изтриването. В противен случай да се предизвика `NonEmptyDirectoryDeletionError`.
    * Ако това, което се опитваме да изтрием не съществува трябва да се хвърли `NodeDoesNotExistError`.
  * `move(source, destination)` - премества намиращото се на `source` в директорията намираща се на място `destination`.
    * Ако `source` не съществува в нашата файлова система трябва да се хвърли `SourceNodeDoesNotExistError`.
    * Ако `destination` не съществува, трябва да се хвърли `DestinationNodeDoesNotExistError`.
    * Ако `destination` съществува, но не е директория да се хвърли `DestinationNotADirectoryError`.
    * Ако `destination` е директория, но в нея вече има файл или директория с името на този, който местим трябва да се хвърли `DestinationNodeExistsError`.
  * `link(source, destination, symbolic=True)` - създава връзка с пълен път `destination`, сочеща към намиращото се на `source`.
    * `symbolic` указва дали връзката трябва да е символна или твърда(по-подробно за това по-долу).
    * Ако `source` не съществува в нашата файлова система и `symbolic` е `True` трябва да се хвърли `NodeDoesNotExistError`.
    * Не можем да създаваме твърди връзки към директории, ако `source` сочи към директория, а `symbolic` е `False` да се хвърля `DirectoryHardLinkError`.
    * Ако се опитваме да създадем твърда връзка към файл, който не съществува трябва да се хвърли `SourceNodeDoesNotExistError`.
  * `mount(file_system, path)` - монтира друга файлова система на зададения пълен път(по-подробно и и за това по-долу).
    * Ако `path` сочи към непразна директория да се хвърли `MountPointNotEmptyError`.
    * Ако не е директория, а файл да се хвърли `MountPointNotADirectoryError`.
    * Ако изобщо не съществува - `MountPointDoesNotExistError`.
    * Трите вида грешки трябва да могат да наследяват `FileSystemMountError`.
  * `unmount(path)` - премахва монтирана файлова система.
    * Ако пътя не съществува да се хвърли `NodeDoesNotExistError`.
    * Ако на дадения път няма монтирана файлова система да се хвърля `NotAMountpointError`
      който също наследява `FileSystemMountError`.

### Пространство
`available_size` трябва да отразява оставащото място на файловата система. В нашия случай за простота всеки файл заема толкова байта колкото е дължината на `content`-а му плюс 1(за „системна информация“), а всяка директория(включително '/') заема по 1 байт.

### Изключения
Всички изключения, които вашите решения могат да хвърлят трябва да са дефинирани класове във вашия код.

* `SourceNodeDoesNotExistError` и `DestinationNodeDoesNotExistError` трябва да наследяват от `NodeDoesNotExistError`
* `MountPointDoesNotExistError`, `MountPointNotADirectoryError` и `MountPointNotEmptyError` трябва да наследяват `FileSystemMountError`
* Всички изключения, които хвърля вашия код трябва да наследяват `FileSystemError`.

```python
>>> fs = FileSystem(22)
>>> fs.size
22
>>> fs.available_size
21
>>> fs.create('/data', content='Nineteen characters')
>>> fs.available_size
1
>>> try:
...     fs.create('/home/gosho')
... except DestinationNodeDoesNotExistError:
...     print('Not even a valid place to create')
... except NotEnoughSpaceError:
...     print('Getting greedy here')
...
Not even a valid place to create
>>> try:
...     fs.create('/home')
... except DestinationNodeDoesNotExistError:
...     print('Not even a valid place to create')
... except NotEnoughSpaceError:
...     print('Getting greedy here')
...
>>> try:
...     fs.create('/home/gosho')
... except DestinationNodeDoesNotExistError:
...     print('Not even a valid place to create')
... except NotEnoughSpaceError:
...     print('Getting greedy here')
...
Getting greedy here
```

## Файлове и директории
Всички методи на `FileSystem` под една или друга форма работят или с файлове или с директории. За целта трябва да имате обекти представляващи файлове и директории.

Няма значение как се казват тези класове и дали са достъпни извън решенията ви, стига `get_node` да връща техни инстанции.

Всеки обект върнат от `get_node` трябва да има атрибут `is_directory`, който да е `True` когато обектът е директория и `False`, ако не е.

### Файлове
Обектите за файлове трябва да дават достъп до съдържанието си, като `str` обект достъпен през `content` атрибута им. Ето така бихме могли да прочетем първия ред на файл:

```python
>>> passwd_file = file_system.get_node('/etc/passwd')
>>> passwd_file.content.split('\n')[0]
'root:x:0:0:root:/root:/usr/bin/zsh'
```


Всеки файл има следните методи:
  * `append(text)` - добавя `text` към  текущия `content` на файла
  * `truncate(text)` - премахва изтрива текущото съдържание на файла и го подменя с `text`
  * `size` - атрибут, казващ размера на файла(дължината на `content` стринга + 1)


### Директории
Всяка директория трябва да предоставя списък с всички съдържими в нея директории и файлове чрез следните атрибути:
  * `directories` - списък с всички поддиректории
  * `files` - списък с всички файлове намиращи се в директорията
  * `nodes` - списък с всички обекти от горните два списъка

### Примери
```python
>>> file_system = FileSystem(50)
>>> file_system.create('/home', directory=True)
>>> home_directory = file_system.get_node('/home')
>>> file_system.create('/home/evstati', directory=True)
>>> evstati_home_directory = file_system.get_node('/home/evstati')
>>> evstati_home_directory in home_directory.directories
True
>>> file_system.create('/home/evstati/.vimrc', content='syntax on')
>>> evstati_vimrc = file_system.get_node('/home/evstati/.vimrc')
>>> evstati_vimrc in evstati_home_directory
True
>>> evstati_vimrc in home_directory
False
>>> evstati_vimrc in evstati_home_directory.nodes
True
>>> evstati.content
'syntax on'
```

```python
>>> suchki = file_system.get_node('/home/evstati/suchki.mp3')
>>> file_system.create('/home/music')
>>> file_system.move('/home/suchki.mp3', '/home/music')
>>> suchki is file_system.get_node('/home/music/suchki.mp3')
True
>>> file_system.get_node('/home/evstati/suchki.mp3')
```


## Връзки
Поддържаме два типа връзки: символни и твърди.

### символни
Меките връзки са специален вид файлове, които нямат собствен `content`, имат `link_path` атрибут, който сочи или към друг файл или към директория.
  * Ако символна връзка сочи към файл, то можем да достъпим нейния `content` атрибут и като резултат трябва да получим съдържанието на файла, към който сочи.
  * Ако символна връзка сочи към директория, то можем да достъпваме `files`, `directories` и `nodes` атрибутите, чрез който да получим директно съответния атрибут на директорията, към която сочи връзката.

Символна връзка може да сочи към несъществуващ път. В такъв случай обаче всеки опит за достъпване на `content`, `files`, `directories` или `nodes` трябва да хвърля `LinkPathError`.

### твърди
Твърдата връзка на практика е самостоятелен обект файл. Създаването на твърда връзка създава нов файл на съответния зададен път, като неговия `content` е същия(**не копие на**) `content`-а на „оригиналния“ файл. Фактически след създаването на твърда връзка никой от двата файла не е източник/оригинален/пръв/по-важен/специален по някакъв начин. Двата файлови обекта са напълно независими един от друг, като просто `content` атрибутите им сочат към един и същи обект. Изтриването на единия файл по никакъв начин не се отразява на другия файл, той продължава да съществува и да сочи към същия `content`. `content`-а на двата файла трябва винаги да бъде еднакъв. Можем да имаме неограничен брой файлови обекти създадени по този начин, сочещи към един и същи `content`.

```python
>>> file_system.create('/tmp/data_file', 'such data, much big')
>>> data_file = file_system.get_node('/tmp/data_file')
>>> file_system.link('/tmp/data_file', '/home/evstati/data_file', symbolic=False)
>>> second_handle = file_system.get_node( '/home/evstati/data_file')
>>> data_file is second_handle
False
>>> data_file.content is second_handle.content
True
>>> data.file.append(', very enterprise')
>>> second_handle.content
'such data, much, big, very enterprise'
>>> file_system.remove('/tmp/data_file')
>>> del data_file
>>> second_handle.content
'such data, much, big, very enterprise'
```

Ако два файла сочат към един и същи `content`, то заетото пространство на файловата система очевидно не трябва да е същото като в случая, в който двата файла са просто копия на едно и също нещо. Заетото пространство трябва да бъде дължината на `content`-а плюс броя на файл обектите, които сочат към него.


```python
>>> fs.available_size
32
>>> fs.create('/such_file', content='Twentyone characters.')
>>> fs.available_size
10
>>> fs.link('/such_file', '/much_file')
>>> fs.available_size
9
```


## Монтиране
Една файлова система може да бъде монтирана на произволен път в друга файлова система, стига този път да сочи към празна директория. Това ще рече, че след монтирането ѝ достъпването на тази директория ще е същото като достъпването на '/' директорията на монтираната файлова система.

```python
>>> file_system.create('/mnt/other', directory=True)
>>> file_system.mount(other_file_system, '/mnt/other')
>>> other_file_system.get_node('/') is file_system.get_node('/mnt/other')
True
```
