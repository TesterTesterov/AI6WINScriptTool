import os
import threading
import tkinter as tk
from tkinter.messagebox import showerror
from library.silky_mes_gui import SilkyMesGUI
from ai6win_mes import AI6WINScript


class AI6WINMesGUI(SilkyMesGUI):
    _strings_lib = {
        "eng": (
            "AI6WINScriptTool by Tester",  # 0
            "Single file",
            "Directory",
            "Enter a name of the .mes file:",
            "Enter a name of the directory with .mes files:",
            "Enter a title of the .txt file:",  # 5
            "Enter a name of the directory with .txt files:",
            "All files",
            "AI6WIN mes scripts",
            "Choice of mes script",
            "Choice of directory with mes scripts",  # 10
            "Text files",
            "Choice of directory with txt files",
            "Choice of text file",
            "Commands:",
            "Status:",  # 15
            "Help:",
            "Common help",
            "Usage help",
            "Breaks help",
            "Disassemble",  # 20
            "Assemble",
            "Warning",
            "File mes or a directory of them is not chosen.",
            "File txt or a directory of them is not chosen.",
            "Managing files...",  # 25
            "Error",
            "Disassembling failed. ",
            "Disassembling succeed. ",
            "Assembling failed. ",
            "Assembling succeed. ",  # 30
        ),
        "rus": (
            "AI6WINScriptTool от Tester-а",  # 0
            "По файлами",
            "По папкам",
            "Введите название файла .mes:",
            "Введите название директории с файлами .mes:",
            "Введите название файла .txt:",  # 5
            "Введите название директории с файлами .txt:",
            "Все файлы",
            "Скрипты mes AI6WIN",
            "Выбор скрипта mes",
            "Выбор директории со скриптами mes",  # 10
            "Текстовые файлы",
            "Выбор директории с файлами txt",
            "Выбор текстового файла",
            "Команды:",
            "Статус:",  # 15
            "Справка:",
            "Общая справка",
            "Справка о использовании",
            "Справка о переносах",
            "Дизассемблировать",  # 20
            "Ассемблировать",
            "Предупреждение",
            "Файл mes или их директория не выбраны",
            "Файл txt или их директория не выбраны",
            "Обрабатываем файлы...",  # 25
            "Ошибка",
            "Дизассемблирование не удалось. ",
            "Дизассемблирование удалось. ",
            "Ассемблирование не удалось. ",
            "Ассемблирование удалось. ",  # 30
        )
    }

    common_help = {
        'eng': """
Dual languaged (rus+eng) tool for disassembling and assembling scripts .mes from the visual novel's engine AI6WIN. Very incomplete list of games on this engine you can find on vndb. With it thou can fully edit all thecode, not just strings. Thou can add message breaks and change scenarios without restrictions! Mes script files can be used not just in AI6WIN, but also in Silky Engine. For assembling and disassembling mes script files of Silky Engine use mesScriptAsseAndDisassembler.
Also you may want to pack and unpack archives of AI6WIN. For it use AI6WINArcTool.
Definations: "#0-" are "free bytes", "#1-" are commands (and "[...]" are arguments below), "#2-" are labels.
    """,
        'rus': """
Двуязычное (рус+англ) средство для разборки и сборки скриптов .mes движка визуальных новелл AI6WIN. С неполным списком игр на нём вы можете ознакомиться на vndb. С ним вы можете полностью редактирвоать код, а не только строки; по вашему повелению добавлять разрывы между сообщений и даже менять сценарии по своему замыслу! Скрипты с расширением "mes" используются не только в AI6WIN, но также и в Silky Engine. Чтобы дизассемблировать и ассемблировать скрипты движка Silky Engine используйте иное средство -- mesScriptAsseAndDisassembler.
Также вам может понадобиться распаковывать и паковать архивы движка AI6WIN. Для сего используйте средство AI6WINArcTool.
Определения: "#0-" есть "вольные байты", "#1-" есть команды (и под ними "[...]" аргументы), "#2-" есть метки.
    """
    }
    breaks_help = {
        'eng': """
Sometimes there could be a very big problem: text may not fully get in textbox. But with this tool thou don't need to cut some part of text, no. Thou can use line and message breaks. Methods are below.
>>> For line breaks insert this below the current message ("SomeString" -> text on the new line).

#1-TO_NEW_STRING
[0]
#1-STR_UNCRYPT
["SomeString"]

>>> For message breaks insert this below the current message ("SomeString" -> text on the new message).

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
    """,
        'rus': """
Иногда можно столкнуться с одной большой-пребольшой проблемой: текст может не полностью влезать в текстовое окно. Однако, с сим средством вам не нужно обрезать его, отнюдь. Вы можеет организовывать переносы по строкам и сообщениям. Методы указаны ниже.
>>> Для переносов по строкам добавьте под текущее сообщение следующий код ("Какая_то_строка" -> текст на новой строке).

#1-TO_NEW_STRING
[0]
#1-STR_UNCRYPT
["Какая_то_строка"]

>>>Для переносов по сообщениям добавьте под текущее сообщение следующий код ("Какая_то_строка" -> текст на новой строке).

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
    """
    }

    def _disassemble_this_mes(self, mes_file: str, txt_file: str) -> None:
        """Disassemble this mes script."""
        try:
            self._thread_semaphore.acquire()
            script_mes = AI6WINScript(mes_file, txt_file)
            script_mes.disassemble()
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, mes_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][28])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
            self._print_lock.acquire()
            print("Disassembling of {0} succeed./Дизассемблирование {0} прошло успешно.".format(mes_file))
            self._print_lock.release()
        except Exception as ex:
            self._print_lock.acquire()
            print("Disassembling of {0} error./Дизассемблирование {0} не удалось.".format(mes_file))
            self._print_lock.release()
            showerror(title=self._strings_lib[self._language][26], message=str(ex))
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, mes_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][27])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
        finally:
            self._count_lock.acquire()
            self._unlocker_count -= 1
            self._count_lock.release()
            if self._unlocker_count == 0:
                self._unlock_activity()
            self._thread_semaphore.release()

    def _assemble(self) -> bool:
        """Assemble a mes script or a group of them from the text file or a group of them"""
        mes_file, txt_file, status = self._get_mes_and_txt()
        if not status:
            return False

        self._lock_activity()
        if self._input_mode.get() == 0:  # File mode.
            self._unlocker_count = 1
            new_thread = threading.Thread(daemon=False, target=self._assemble_this_mes,
                                          args=(mes_file, txt_file))
            new_thread.start()
        else:  # Dir mode.
            files_to_manage = []
            os.makedirs(txt_file, exist_ok=True)
            for root, dirs, files in os.walk(txt_file):
                for file_name in files:
                    new_file_array = []  # mes_file, txt_file

                    basic_path = os.sep.join(os.path.join(root, file_name).split(os.sep)[1:])
                    rel_mes_name = os.path.normpath(os.path.join(mes_file, os.path.splitext(basic_path)[0] + ".mes"))
                    rel_txt_name = os.path.normpath(os.path.join(txt_file, basic_path))

                    new_file_array.append(rel_mes_name)
                    new_file_array.append(rel_txt_name)
                    files_to_manage.append(new_file_array)

                    # Why did I not initiate file management right away, thou ask?

            self._unlocker_count = len(files_to_manage)  # ...That is the answer.
            for file_mes, file_txt in files_to_manage:
                new_thread = threading.Thread(daemon=False, target=self._assemble_this_mes,
                                              args=(file_mes, file_txt))
                new_thread.start()

        return True

    def _assemble_this_mes(self, mes_file: str, txt_file: str) -> None:
        """Assemble this mes script."""
        try:
            self._thread_semaphore.acquire()
            script_mes = AI6WINScript(mes_file, txt_file)
            script_mes.assemble()
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, mes_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][30])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
            self._print_lock.acquire()
            print("Assembling of {0} succeed./Ассемблирование {0} прошло успешно.".format(mes_file))
            self._print_lock.release()
        except Exception as ex:
            self._print_lock.acquire()
            print("Assembling of {0} error./Ассемблирование {0} не удалось.".format(mes_file))
            self._print_lock.release()
            showerror(title=self._strings_lib[self._language][26], message=str(ex))
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, mes_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][29])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
        finally:
            self._count_lock.acquire()
            self._unlocker_count -= 1
            self._count_lock.release()
            if self._unlocker_count == 0:
                self._unlock_activity()
            self._thread_semaphore.release()
