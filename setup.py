import sys
import cx_Freeze

base = None

if (sys.platform == 'win32'):
    base = "Win32GUI"


executables = [cx_Freeze.Executable("main.py",
                                    shortcut_name="AI6WINScriptTool",
                                    shortcut_dir="AI6WINScriptTool")]

cx_Freeze.setup(
        name="AI6WINScriptTool",
        version="1.0",
        description="Dual languaged (rus+eng) tool for packing and unpacking mes scripts of AI6WIN.\n"
                    "Двухязычное средство (рус+англ) для распаковки и запаковки скриптов mes AI6WIN.",
        options={"build_exe": {"packages": []}},
        executables=executables
)
