from ai6win_mes_gui import AI6WINMesGUI

debug = False


def test(mode: str):
    # diss, ass, diss_for_hack, spec_cmp...
    from ai6win_mes import AI6WINScript

    base_name = "01asa_s02_01_03"
    script_mes = "{}.mes".format(base_name)
    file_txt = "{}.txt".format(base_name)

    if mode == "diss":
        new_script = AI6WINScript(script_mes, file_txt, verbose=True, debug=False, version=1)
        new_script.disassemble()
        del new_script
    elif mode == "ass":
        new_script = AI6WINScript(script_mes, file_txt, verbose=True, debug=False)
        new_script.assemble()
        del new_script
    elif mode == "diss_for_hack":
        new_script = AI6WINScript(script_mes, file_txt, verbose=True, debug=True, hackerman_mode=True)
        new_script.disassemble()
        del new_script


def main():
    gui = AI6WINMesGUI()
    return True


if __name__ == '__main__':
    if debug:
        test("diss")
    else:
        main()
