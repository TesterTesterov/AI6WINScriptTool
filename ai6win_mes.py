import struct
import json
import os
from library.silky_mes import SilkyMesScript, SilkyMesScriptError


class AI6WINScript(SilkyMesScript):
    default_version = 1
    supported_versions = (
        (0, "Aishimai 4 & earliest games"),
        (1, "Most games"),
    )

    command_library = (
        (
            (0x00, '', 'YIELD'),
            (0x01, '', 'RETURN'),
            (0x02, '', 'LGDLOB1_I8'),
            (0x03, '', 'LGDLOB2_I16'),
            (0x04, '', 'LGDLOB3_VAR'),
            (0x05, '', 'LGDLOB4_VAR'),
            (0x06, '', 'LDLOC_VAR'),
            (0x07, '', 'LGDLOB5_I8'),
            (0x08, '', 'LGDLOB5_I16'),
            (0x09, '', 'LGDLOB5_I32'),
            (0x0A, 'S', 'STR_PRIMARY'),
            (0x0B, 'S', 'STR_SUPPLEMENT'),
            (0x0C, '', 'STGLOB1_I8'),
            (0x0D, '', 'STGLOB2_I16'),
            (0x0E, '', 'STGLOB3_VAR'),
            (0x0F, '', 'STGLOB4_VAR'),

            (0x10, '', 'STLOC_VAR'),
            (0x11, '', 'STGLOB5_I8'),
            (0x12, '', 'STGLOB6_I16'),
            (0x13, '', 'STGLOB7_I32'),
            (0x14, '>I', 'JUMP_IF_ZERO'),
            (0x15, '>I', 'JUMP'),
            (0x16, '>I', 'LIBREG'),
            (0x17, '', 'LIBCALL'),
            (0x18, '', 'SYSCALL'),
            (0x19, '>I', 'MESSAGE'),
            (0x1A, '>I', 'CHOICE'),
            (0x1B, 'B', 'ESCAPE'),
            (0x1D, '', ''),

            (0x32, '>i', 'PUSH_INT32'),
            (0x33, 'S', 'PUSH_STR'),
            (0x34, '', 'ADD'),
            (0x35, '', 'SUB'),
            (0x36, '', 'MUL'),
            (0x37, '', 'DIV'),
            (0x38, '', 'MOD'),
            (0x39, '', 'RAND'),
            (0x3A, '', 'LOGICAL_AND'),
            (0x3B, '', 'LOGICAL_OR'),
            (0x3C, '', 'BINARY_AND'),
            (0x3D, '', 'BINARY_OR'),
            (0x3E, '', 'LT'),
            (0x3F, '', 'GT'),

            (0x40, '', 'LE'),
            (0x41, '', 'GE'),
            (0x42, '', 'EQ'),
            (0x43, '', 'NEQ'),

            (0xFA, '', ''),
            (0xFB, '', ''),
            (0xFC, '', ''),
            (0xFD, '', ''),
            (0xFE, '', ''),
            (0xFF, '', ''),
        ),
        (
            (0x00, '', 'YIELD'),
            (0x01, '', 'RETURN'),
            (0x02, '', 'LGDLOB1_I8'),
            (0x03, '', 'LGDLOB2_I16'),
            (0x04, '', 'LGDLOB3_VAR'),
            (0x05, '', 'LGDLOB4_VAR'),
            (0x06, '', 'LDLOC_VAR'),
            (0x07, '', 'LGDLOB5_I8'),
            (0x08, '', 'LGDLOB5_I16'),
            (0x09, '', 'LGDLOB5_I32'),
            (0x0A, 'S', 'STR_PRIMARY'),
            (0x0B, 'S', 'STR_SUPPLEMENT'),
            (0x0C, '', 'STGLOB1_I8'),
            (0x0D, '', 'STGLOB2_I16'),
            (0x0E, '', 'STGLOB3_VAR'),
            (0x0F, '', 'STGLOB4_VAR'),

            (0x10, 'B', 'STLOC_VAR'),
            (0x11, '', 'STGLOB5_I8'),
            (0x12, '', 'STGLOB6_I16'),
            (0x13, '', 'STGLOB7_I32'),
            (0x14, '>I', 'JUMP_IF_ZERO'),
            (0x15, '>I', 'JUMP'),
            (0x16, '>I', 'LIBREG'),
            (0x17, '', 'LIBCALL'),
            (0x18, '', 'SYSCALL'),
            (0x19, '>I', 'MESSAGE'),
            (0x1A, '>I', 'CHOICE'),
            (0x1B, 'B', 'ESCAPE'),
            (0x1D, '', ''),

            (0x32, '>i', 'PUSH_INT32'),
            (0x33, 'S', 'PUSH_STR'),
            (0x34, '', 'ADD'),
            (0x35, '', 'SUB'),
            (0x36, 'B', 'MUL'),
            (0x37, '', 'DIV'),
            (0x38, '', 'MOD'),
            (0x39, '', 'RAND'),
            (0x3A, '', 'LOGICAL_AND'),
            (0x3B, '', 'LOGICAL_OR'),
            (0x3C, '', 'BINARY_AND'),
            (0x3D, '', 'BINARY_OR'),
            (0x3E, '', 'LT'),
            (0x3F, '', 'GT'),

            (0x40, '', 'LE'),
            (0x41, '', 'GE'),
            (0x42, '', 'EQ'),
            (0x43, '', 'NEQ'),

            (0xFA, '', ''),
            (0xFB, '', ''),
            (0xFC, '', ''),
            (0xFD, '', ''),
            (0xFE, '', ''),
            (0xFF, '', ''),
        )
    )

    offsets_library = (
        (0x14, 0),
        (0x15, 0),
        (0x16, 0),
        (0x1A, 0),
    )

    def __init__(self, mes_name: str, txt_name: str, encoding: str = "", debug: bool = False, verbose: bool = False,
                 hackerman_mode: bool = False, version=1):
        """Prms:
mes_name -- name (and path) of mes script.
txt_name -- name (and path) of txt file.
encoding (not required) -- name of encoding.
debug -- push debug data in the script.
verbose -- print data about the class operations.
hackerman_mode -- for true hackers; helps hacking unsupported mes scripts."""

        super().__init__(mes_name, txt_name, encoding, debug, verbose, hackerman_mode)
        self.version = version

    # User methods.

    def disassemble(self) -> None:
        """Disassemble AI6WIN mes script."""
        self._offsets = []
        self._prm, self._first_offsets = self._diss_header()
        self._diss_other_offsets()
        if self._verbose:
            print("Parameters:", self._prm[0:1])
            print("First offsets:", len(self._first_offsets), self._first_offsets)
            print("True offsets:", len(self._offsets), self._offsets)
        self._disassemble_commands()

    def assemble(self) -> None:
        """Assemble Silky Engine mes script."""

        self._prm, self._first_offsets, self._offsets = self._assemble_offsets_and_parameters()

        if self._verbose:
            print("Parameters:", self._prm[0:1])
            print("First offsets:", len(self._first_offsets), self._first_offsets)
            print("True offsets:", len(self._offsets), self._offsets)
        self._assemble_script_file()

    # Technical methods for assembling.

    def _assemble_script_file(self) -> None:
        """Assemble AI6WIN mes script."""
        in_file = open(self._txt_name, 'r', encoding=self.encoding)
        try:
            os.rename(self._mes_name, self._mes_name + '.bak')
        except OSError:
            pass
        out_file = open(self._mes_name, 'wb')

        message_count = 0
        search_offset = [i[0] for i in self._offsets]

        out_file.write(struct.pack('I', self._prm[0]))
        for first_offset in self._first_offsets:
            out_file.write(struct.pack('I', first_offset))

        while True:
            line = in_file.readline()
            if line == '':  # EOF.
                break
            if len(line) == 1:  # To evade some nasty errors.
                continue
            if (line == '\n') or (line[0] == '$'):
                continue
            if line[1] == '0':
                out_file.write(bytes.fromhex(line[2:-1]))
            elif line[1] == '1':
                command_string = line[3:-1]
                command_index = -1
                for num, lib_entry in enumerate(self.command_library[self.version]):  # Check if it is written by name.
                    if command_string == lib_entry[2]:
                        command_index = num
                        break
                if command_index == -1:  # Check if it is written by hex.
                    command_string = int(command_string, 16)
                    for num, lib_entry in enumerate(self.command_library[self.version]):
                        if command_string == lib_entry[0]:
                            command_index = num
                            break
                if command_index == -1:  # There is no such command (text). But this should be impossible!
                    raise AI6WINScriptError("Error! There is no such command.\n{}".format(command_string))
                out_file.write(struct.pack('B', self.command_library[self.version][command_index][0]))

                line = in_file.readline()

                argument_list = json.loads(line)

                this_command = self.command_library[self.version][command_index][0]
                offset_set = -1
                if this_command == 0x19:
                    argument_list[0] = message_count
                    message_count += 1
                else:
                    for offset_entry in self.offsets_library:
                        if this_command == offset_entry[0]:
                            offset_set = offset_entry[1]
                            break

                if offset_set != -1:
                    indexer = search_offset.index(argument_list[offset_set])
                    argument_list[offset_set] = self._offsets[indexer][1]

                argument_bytes = self.set_args(argument_list, self.command_library[self.version][command_index][1], self.encoding)
                out_file.write(argument_bytes)

        in_file.close()
        out_file.close()

    def _assemble_offsets_and_parameters(self) -> tuple:
        """Assemble offsets and parameters of AI6WIN mes archive."""
        in_file = open(self._txt_name, 'r', encoding=self.encoding)

        first_offsets = []
        offsets = []
        prm = [0, 0]  # First shall be changed. Second is to work with functions inherited from silky_mes.

        pointer = 0
        message_count = 0

        while True:
            line = in_file.readline()
            if line == '':  # EOF.
                break
            if len(line) == 1:  # To evade some nasty errors.
                continue
            if (line == '\n') or (line[0] == '$'):  # Line without text or comment should not be parsed as script.
                continue

            # Actually code strings logic.

            if line[1] == '0':  # "Free bytes".
                pointer += len(line[2:-1].split(' '))
            elif line[1] == '1':  # Command.
                command_string = line[3:-1]
                command_index = -1
                for num, lib_entry in enumerate(self.command_library[self.version]):  # Check if it is written by name.
                    if command_string == lib_entry[2]:
                        command_index = num
                        break
                if command_index == -1:  # Check if it is written by hex.
                    command_string = int(command_string, 16)
                    for num, lib_entry in enumerate(self.command_library[self.version]):
                        if command_string == lib_entry[0]:
                            command_index = num
                            break
                if command_index == -1:  # There is no such command (text). But this should be impossible!
                    raise AI6WINScriptError("Error! There is no such command.\n{}".format(command_string))

                if self.command_library[self.version][command_index][0] == 0x19:  # Since header save offsets to messages.
                    message_count += 1
                    first_offsets.append(pointer)

                pointer += 1

                # Okay, now is the time for getting arguments length!
                line = in_file.readline()
                argument_list = json.loads(line)
                if self.command_library[self.version][command_index][0] == 0x19:  # For this to not cause any errors.
                    argument_list[0] = 0
                argument_bytes = self.set_args(argument_list, self.command_library[self.version][command_index][1], self.encoding)
                pointer += len(argument_bytes)

            elif line[1] == '2':  # If label (of true offset).
                offset_array = []

                offset_number = int(line[3:-1])
                offset_array.append(offset_number)
                offset_array.append(pointer)

                offsets.append(offset_array)
        in_file.close()

        prm[0] = message_count

        return prm, first_offsets, offsets

    # Technical methods for disassembling.

    def _disassemble_commands(self) -> None:
        """Disassemble Silky Engine mes script commands."""
        commands = []
        args = []
        # [Opcode, struct, name].
        pointer = self.get_true_offset(0)
        stringer = ''
        these_indices = []

        out_file = open(self._txt_name, 'w', encoding=self.encoding)
        in_file = open(self._mes_name, 'rb')
        in_file.seek(pointer, 0)

        sorted_offset = sorted(list(enumerate(self._offsets)), key=lambda x: x[1])
        # Sorted by offsets, but with index saving.
        search_offset = [i[1] for i in sorted_offset]
        initial_sorted_offset = sorted_offset.copy()
        initial_search_offset = search_offset.copy()
        # I know, you may say it's pointless, but that's for the sake of optimization.

        second_offsets = [self.get_true_offset(i) for i in self._second_offsets]

        while True:
            pointer = in_file.tell()  # To get current position before the command.

            # Offsets functionality.
            # I did try my best to optimize it. It may be looked as bad, but...
            # I have managed to drastically decrease the number of iterations.
            # From some hundreds to about 1-2.
            these_indices.clear()
            speedy_crutch = -1
            for pos, offset in sorted_offset:
                speedy_crutch += 1
                if pointer == offset:
                    these_indices.append(speedy_crutch)
                    if self._debug:
                        out_file.write("#2-{} {}\n".format(pos, pointer))
                    else:
                        out_file.write("#2-{}\n".format(pos))
                    break
                elif pointer > offset:
                    break
            for used in these_indices:
                sorted_offset.pop(used)
                search_offset.pop(used)
            for offset in second_offsets:  # Should be fine since it is rare and not lengthy.
                if pointer == offset:
                    if self._debug:
                        out_file.write("#3 {}\n".format(pointer))
                    else:
                        out_file.write("#3\n")
                    break

            # Commands functionality.

            current_byte = in_file.read(1)
            if current_byte == b'':
                break
            current_byte = current_byte[0]
            args.append([])
            commands.append(current_byte)
            analyzer = str(hex(current_byte))[2:]
            if (len(analyzer) == 1):
                analyzer = '0' + analyzer

            lib_index = -1
            for i in range(len(self.command_library[self.version])):
                if current_byte == self.command_library[self.version][i][0]:
                    lib_index = i
                    break
            if lib_index != -1:
                if stringer != '':
                    stringer = stringer.lstrip(' ')
                    stringer = '#0-{}\n'.format(stringer)
                    out_file.write(stringer)
                    stringer = ''

                out_file.write("#1-")
                if self.command_library[self.version][lib_index][2] == '':
                    out_file.write(analyzer)
                else:
                    if self.command_library[self.version][lib_index][2] == 'STR_CRYPT':
                        out_file.write('STR_UNCRYPT')
                    else:
                        out_file.write(self.command_library[self.version][lib_index][2])
                if self._debug:
                    out_file.write(' {}\n'.format(pointer))
                else:
                    out_file.write('\n')

                arguments_list = self.get_args(in_file, self.command_library[self.version][lib_index][1], current_byte, self.encoding)

                what_index = -1
                for entry_pos, offsets_entry in enumerate(self.offsets_library):
                    if current_byte == offsets_entry[0]:
                        what_index = entry_pos

                if what_index != -1:
                    first_indexer = self.offsets_library[what_index][1]
                    evil_offset = self.get_true_offset(arguments_list[first_indexer])
                    indexer = initial_search_offset.index(evil_offset)
                    arguments_list[first_indexer] = initial_sorted_offset[indexer][0]

                if self.command_library[self.version][lib_index][0] == 0x19:
                    arguments_list[0] = "*MESSAGE_NUMBER*"
                json.dump(arguments_list, out_file, ensure_ascii=False)
                out_file.write('\n')

            else:
                stringer += ' ' + analyzer
                pointer += 1
        if stringer != '':  # Print remaining free bytes.
            stringer = stringer.lstrip(' ')
            stringer = '#0-' + stringer
            out_file.write(stringer)

        out_file.close()

    def _diss_other_offsets(self) -> None:
        """Disassemble other offsets from the Silky Engine script."""
        pointer = self.get_true_offset(0)
        in_file = open(self._mes_name, 'rb')
        in_file.seek(pointer, 0)

        if self._hackerman_mode:
            out_file = open("HACK.txt", 'w', encoding=self.encoding)

        while True:
            pointer = in_file.tell()
            current_byte = in_file.read(1)
            if current_byte == b'':
                break
            current_byte = current_byte[0]  # Get int from byte in the fastest way possible.
            lib_index = -1
            for i in range(len(self.command_library[self.version])):
                if (current_byte == self.command_library[self.version][i][0]):
                    lib_index = i
                    break
            if lib_index != -1:
                arguments_list = self.get_args(in_file, self.command_library[self.version][lib_index][1], current_byte,
                                               self.encoding)

                if self._hackerman_mode:
                    out_file.write("#1-{}    {}\n".format(hex(current_byte), pointer))
                    out_file.write(str(arguments_list))
                    out_file.write("\n")

                what_index = -1
                for entry_pos, offsets_entry in enumerate(self.offsets_library):
                    if current_byte == offsets_entry[0]:
                        what_index = entry_pos
                if what_index != -1:
                    not_here = True
                    good_offset = self.get_true_offset(arguments_list[self.offsets_library[what_index][1]])
                    for i in range(len(self._offsets)):
                        if good_offset == self._offsets[i]:
                            not_here = False
                    if not_here:
                        self._offsets.append(good_offset)
            else:
                if self._hackerman_mode:
                    out_file.write("#0-{}    {}\n".format(hex(current_byte), pointer))

        in_file.close()
        if self._hackerman_mode:
            out_file.close()

    def _diss_header(self) -> tuple:
        """Disassemble Silky Engine mes header."""
        first_offsets = []
        with open(self._mes_name, 'rb') as mes_file:
            prm = list(struct.unpack('I', mes_file.read(4)))
            for i in range(prm[0]):
                first_offsets.append(struct.unpack('I', mes_file.read(4))[0])

        return prm, first_offsets

    # Offsets methods.

    def get_true_offset(self, raw_offset: int) -> int:
        """Get true offset (as it is factically in the file)."""
        return raw_offset + self._prm[0] * 4 + 4

    def set_true_offset(self, raw_offset):
        """Set true offset (as it is factically in the arguments)."""
        return raw_offset - self._prm[0] * 4 - 4

    # Disassembling methods.

    @staticmethod
    def get_args(in_file, args: str, current_byte: int, current_encoding: str) -> list:
        """Extract args from file."""
        arguments_list = []
        appendix = ""
        for argument in args:  # self.command_library[lib_index][1]
            if argument in AI6WINScript.technical_instances:
                appendix = argument
            elif argument in AI6WINScript.get_I.instances:
                arguments_list.append(AI6WINScript.get_I(in_file, appendix + argument))
            elif argument in AI6WINScript.get_H.instances:
                arguments_list.append(AI6WINScript.get_H(in_file, appendix + argument))
            elif argument in AI6WINScript.get_B.instances:
                arguments_list.append(AI6WINScript.get_B(in_file, appendix + argument))
            elif argument in AI6WINScript.get_S.instances:
                arguments_list.append(AI6WINScript.get_S(in_file, current_encoding))
        return arguments_list

    @staticmethod
    def get_S(in_file, this_encoding: str) -> tuple:
        """Read string from file and it."""
        string = b''
        byte = in_file.read(1)
        while byte != b'\x00':
            string += byte
            byte = in_file.read(1)
        return string.decode(encoding=this_encoding)


class AI6WINScriptError(SilkyMesScriptError):
    pass
