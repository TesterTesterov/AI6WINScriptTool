# AI6WINScriptTool
## English
 Dual languaged (rus+eng) tool for disassembling and assembling scripts .mes from the visual novel's engine AI6WIN. Very incomplete list of games on this engine you can find [on vndb](https://vndb.org/v?q=&ch=&f=N18fwAI6WIN-). With it thou can fully edit all thecode, not just strings. Thou can add message breaks and change scenarios without restrictions!
 Mes script files can be used not just in AI6WIN, but also in Silky Engine. For assembling and disassembling mes script files of Silky Engine use [mesScriptAsseAndDisassembler](https://github.com/TesterTesterov/mesScriptAsseAndDisassembler).
 
 Also you may want to pack and unpack archives of AI6WIN. For it use [AI6WINArcTool](https://github.com/TesterTesterov/AI6WINArcTool).

Definations: "#0-" are "free bytes", "#1-" are commands (and "\[...]" are arguments below), "#2-" are labels.

## Russian
 Двуязычное (рус+англ) средство для разборки и сборки скриптов .mes движка визуальных новелл AI6WIN. С неполным списком игр на нём вы можете ознакомиться [на vndb](https://vndb.org/v?q=&ch=&f=N18fwAI6WIN-). С ним вы можете полностью редактирвоать код, а не только строки; по вашему повелению добавлять разрывы между сообщений и даже менять сценарии по своему замыслу!
  Скрипты с расширением "mes" используются не только в AI6WIN, но также и в Silky Engine. Чтобы дизассемблировать и ассемблировать скрипты движка Silky Engine используйте иное средство -- [mesScriptAsseAndDisassembler](https://github.com/TesterTesterov/mesScriptAsseAndDisassembler).
 
 Также вам может понадобиться распаковывать и паковать архивы движка AI6WIN. Для сего используйте средство [AI6WINArcTool](https://github.com/TesterTesterov/AI6WINArcTool).
  
 Определения: "#0-" есть "вольные байты", "#1-" есть команды (и под ними "\[...]" аргументы), "#2-" есть метки.
 
 # Usage / Использование
## English
![image](https://user-images.githubusercontent.com/66121918/147406445-b902efdf-b693-40ab-ab3b-ee123b02ae4f.png)
1. Choose the mode, file or directory. In first mode you will work with one .mes - .txt pair, in second -- with all files in a pair of directories.
2. Enter a name of the .mes file in the top entry (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
3. Enter a name of the .txt file (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
4. For dissassemble push the button "Disassemble script".
5. For assemble push the button "Assemble script".
6. Status will be displayed on the text area below.

## Русский
![image](https://user-images.githubusercontent.com/66121918/147406436-d0acbb0b-3744-47ee-bd68-008377343d6c.png)
1. Выберите режим: файл или директорию. В первом вы будете работать с парой .mes - .txt, во втором -- со всеми файлами в паре директорий.
2. Введите название файла .mes в верхней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
3. Введите название файла .txt в нижней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
4. Для разборки нажмите на кнопку "Дизассемблировать скрипт".
5. Для сборки нажмите на кнопку "Ассемблировать скрипт".
6. Статус сих операций будет отображаться на текстовом поле ниже.


# Line and Message Breaks Help / Помощь по организации переносов по строкам и сообщениям.
## English
Sometimes there could be a very big problem: text may not fully get in textbox. But with this tool thou don't need to cut some part of text, no. Thou can use message breaks. Methods are below.
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
Иногда можно столкнуться с одной большой-пребольшой проблемой: текст может не полностью влезать в текстовое окно. Однако, с сим средством вам не нужно обрезать его, отнюдь. Вы можеет организовывать переносы по сообщениям. Метод указан ниже.
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

## Russian
- [Рабыни гипноза в школе: А ведь недавно точно ненавидела](https://vndb.org/v1601).
