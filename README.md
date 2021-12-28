# AI6WINScriptTool
## English
 Dual languaged (rus+eng) tool for disassembling and assembling scripts .mes from the visual novel's engine AI6WIN. Very incomplete list of games on this engine you can find [on vndb](https://vndb.org/v?q=&ch=&f=N18fwAI6WIN-). With it thou can fully edit all the code, not just strings. Thou can add message breaks and change scenarios without restrictions!
 Mes script files can be used not just in AI6WIN, but also in AI5WIN and Silky Engine. For assembling and disassembling mes script files of AI5WIN use [AI5WINScriptTool](https://github.com/TesterTesterov/AI5WINScriptTool) and for mes of Silky Engine use [mesScriptAsseAndDisassembler](https://github.com/TesterTesterov/mesScriptAsseAndDisassembler).
 
 Also you may want to pack and unpack archives of AI6WIN. For it use [AI6WINArcTool](https://github.com/TesterTesterov/AI6WINArcTool).

Definations: "#0-" are "free bytes", "#1-" are commands (and "\[...]" are arguments below), "#2-" are labels.

## Русский
 Двуязычное (рус+англ) средство для дизассемблирования и ассемблирования скриптов .mes движка визуальных новелл AI6WIN. С неполным списком игр на нём вы можете ознакомиться [на vndb](https://vndb.org/v?q=&ch=&f=N18fwAI6WIN-). С ним вы можете полностью редактирвоать код, а не только строки; по вашему повелению добавлять разрывы между сообщений и даже менять сценарии по своему замыслу!
  Скрипты с расширением "mes" используются не только в AI6WIN, но также и в AI5WIN с Silky Engine. Чтобы дизассемблировать и ассемблировать скрипты движов AI5WIN и Silky Engine используйте иные следства -- [AI5WINScriptTool](https://github.com/TesterTesterov/AI5WINScriptTool) и [mesScriptAsseAndDisassembler](https://github.com/TesterTesterov/mesScriptAsseAndDisassembler) соответственно.
 
 Также вам может понадобиться распаковывать и паковать архивы движка AI6WIN. Для сего используйте средство [AI6WINArcTool](https://github.com/TesterTesterov/AI6WINArcTool).
  
 Определения: "#0-" есть "вольные байты", "#1-" есть команды (и под ними "\[...]" аргументы), "#2-" есть метки.
 
 # Usage / Использование
## English
![image](https://user-images.githubusercontent.com/66121918/147406445-b902efdf-b693-40ab-ab3b-ee123b02ae4f.png)
1. Choose the mode, file or directory. In first mode you will work with one .mes - .txt pair, in second -- with all files in a pair of directories.
2. Enter a name of the .mes file in the top entry (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
3. Enter a name of the .txt file (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
4. For dissassemble push the button "Disassemble".
5. For assemble push the button "Assemble".
6. Status will be displayed on the text area below.

## Русский
![image](https://user-images.githubusercontent.com/66121918/147406436-d0acbb0b-3744-47ee-bd68-008377343d6c.png)
1. Выберите режим: файл или директорию. В первом вы будете работать с парой .mes - .txt, во втором -- со всеми файлами в паре директорий.
2. Введите название файла .mes в верхней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
3. Введите название файла .txt в нижней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
4. Для дизассемблирования нажмите на кнопку "Дизассемблировать".
5. Для ассемблирования нажмите на кнопку "Ассемблировать".
6. Статус сих операций будет отображаться на текстовом поле ниже.


# Line and Message Breaks Help / Помощь по организации переносов по строкам и сообщениям.
## English
Sometimes there could be a very big problem: text may not fully get in textbox. But with this tool thou don't need to cut some part of text, no. Thou can use line and message breaks. Methods are below.
### For line breaks insert this below the current message ("SomeString" -> text on the new line).
```
#1-TO_NEW_STRING
[0]
#1-STR_UNCRYPT
["SomeString"]
```
### For message breaks insert this below the current message ("SomeString" -> text on the new message).
```
#1-32
[0, 3]
#1-32
[0, 23]
#1-18
[]
#1-32
[0, 4]
#1-32
[0, 0]
#1-32
[0, 31]
#1-18
[]
#1-MESSAGE
["*MESSAGE_NUMBER*"]
#1-STR_UNCRYPT
["SomeString"]
```

## Русский
Иногда можно столкнуться с одной большой-пребольшой проблемой: текст может не полностью влезать в текстовое окно. Однако, с сим средством вам не нужно обрезать его, отнюдь. Вы можеет организовывать переносы по строкам и сообщениям. Методы указаны ниже.
### Для переносов по строкам добавьте под текущее сообщение следующий код ("Какая_то_строка" -> текст на новой строке).
```
#1-TO_NEW_STRING
[0]
#1-STR_UNCRYPT
["Какая_то_строка"]
```
### Для переносов по сообщениям добавьте под текущее сообщение следующий код ("Какая_то_строка" -> текст на новой строке).
```
#1-32
[0, 3]
#1-32
[0, 23]
#1-18
[]
#1-32
[0, 4]
#1-32
[0, 0]
#1-32
[0, 31]
#1-18
[]
#1-MESSAGE
["*MESSAGE_NUMBER*"]
#1-STR_UNCRYPT
["Какая_то_строка"]
```


# Tested on / Протестировано на
## English
- [Gakuen Saimin Reido -Sakki made, Daikirai Datta Hazu na no ni-](https://vndb.org/v1601).
- [Words Worth - Windows 10 Edition](https://vndb.org/v315).

## Russian
- [Рабыни гипноза в школе: А ведь недавно точно ненавидела](https://vndb.org/v1601).
- [Значимость слов: Версия с поддержкой Windows 10](https://vndb.org/v315).
