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

    """,
        'rus': """
    
    """
    }
    breaks_help = {
        'eng': """

    """,
        'rus': """

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
