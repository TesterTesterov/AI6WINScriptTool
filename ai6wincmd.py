import argparse


def diss(script_mes: str, file_txt: str, version: int = 1, encoding: str = 'cp932'):
    from ai6win_mes import AI6WINScript

    new_script = AI6WINScript(script_mes, file_txt, encoding=encoding, verbose=True, debug=False, version=version)
    new_script.disassemble()
    del new_script


def ass(script_mes: str, file_txt: str, version: int = 1, encoding: str = 'cp932'):
    from ai6win_mes import AI6WINScript

    new_script = AI6WINScript(script_mes, file_txt, encoding=encoding, verbose=True, debug=False, version=version)
    new_script.assemble()
    del new_script


parser = argparse.ArgumentParser(prog="AI6WINScriptTool", description="Assembler and disassembler of AI6WIN engine"
                                                                      "scripts")
parser.add_argument('action', choices=["d", "a"], help="Action")  # disassemble, assemble.
parser.add_argument('mes_file', help="Mes file")
parser.add_argument('txt_file', help="Txt file")
parser.add_argument('-v', '--version', dest="version",
                    choices=[0, 1], default=1, required=False, type=int, help="Mes version")
parser.add_argument('-e', '--encoding', dest="encoding", default='cp932', required=False, help="Strings encoding")

argdata = parser.parse_args()
action = argdata.action
mes_file = argdata.mes_file
txt_file = argdata.txt_file
version = argdata.version
encoding = argdata.encoding
if action == 'd':
    diss(mes_file, txt_file, version, encoding)
else:
    ass(mes_file, txt_file, version, encoding)
