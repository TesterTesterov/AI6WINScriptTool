import struct
import json
import os
from library.silky_mes import SilkyMesScript, SilkyMesScriptError


class AI6WINScript(SilkyMesScript):
    command_library = (
        (0x00, '', 'NULL'),
        (0x01, 'I', ''),
        (0x02, '', ''),
        (0x03, '', ''),
        (0x04, '', ''),
        (0x05, '', ''),
        (0x06, '', ''),

        (0x0A, 'S', 'STR_CRYPT'),
        (0x0B, 'S', 'STR_UNCRYPT'),
        (0x0C, '', ''),
        (0x0D, '', ''),
        (0x0E, '', ''),
        (0x0F, '', ''),

        (0x10, 'B', ''),
        (0x11, '', ''),
        (0x14, '>I', 'JUMP'),
        (0x15, '>I', 'MSG_OFSETTER'),
        (0x16, '>I', 'SPEC_OFSETTER'),
        (0x17, '', ''),
        (0x18, '', ''),
        (0x19, '>I', 'MESSAGE'),
        (0x1A, '>I', ''),
        (0x1B, '>I', ''),
        (0x1C, 'B', 'TO_NEW_STRING'),
        (0x1D, '', ''),

        (0x32, '>hh', ''),
        (0x33, 'S', 'STR_RAW'),
        (0x34, '', ''),
        (0x35, '', ''),
        (0x36, 'B', 'JUMP_2'),
        (0x37, '', ''),
        (0x38, '', ''),  # AI6WIN only?
        (0x3A, '', ''),
        (0x3B, '', ''),
        (0x39, '', ''),  # AI6WIN only?
        (0x3C, '', ''),
        (0x3D, '', ''),
        (0x3E, '', ''),
        (0x3F, '', ''),  # AI6WIN only?

        (0x40, '', ''),  # AI6WIN only?
        (0x41, '', ''),  # AI6WIN only?
        (0x42, '', ''),
        (0x43, '', ''),

        (0xFA, '', ''),
        (0xFB, '', ''),
        (0xFC, '', ''),
        (0xFD, '', ''),
        (0xFE, '', ''),
        (0xFF, '', ''),
    )

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
                for num, lib_entry in enumerate(self.command_library):  # Check if it is written by name.
                    if command_string == lib_entry[2]:
                        command_index = num
                        break
                if command_index == -1:  # Check if it is written by hex.
                    command_string = int(command_string, 16)
                    for num, lib_entry in enumerate(self.command_library):
                        if command_string == lib_entry[0]:
                            command_index = num
                            break
                if command_index == -1:  # There is no such command (text). But this should be impossible!
                    raise AI6WINScriptError("Error! There is no such command.\n{}".format(command_string))
                out_file.write(struct.pack('B', self.command_library[command_index][0]))

                line = in_file.readline()

                argument_list = json.loads(line)

                this_command = self.command_library[command_index][0]
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

                argument_bytes = self.set_args(argument_list, self.command_library[command_index][1], self.encoding)
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
                for num, lib_entry in enumerate(self.command_library):  # Check if it is written by name.
                    if command_string == lib_entry[2]:
                        command_index = num
                        break
                if command_index == -1:  # Check if it is written by hex.
                    command_string = int(command_string, 16)
                    for num, lib_entry in enumerate(self.command_library):
                        if command_string == lib_entry[0]:
                            command_index = num
                            break
                if command_index == -1:  # There is no such command (text). But this should be impossible!
                    raise AI6WINScriptError("Error! There is no such command.\n{}".format(command_string))

                if self.command_library[command_index][0] == 0x19:  # Since header save offsets to messages.
                    message_count += 1
                    first_offsets.append(pointer)

                pointer += 1

                # Okay, now is the time for getting arguments length!
                line = in_file.readline()
                argument_list = json.loads(line)
                if self.command_library[command_index][0] == 0x19:  # For this to not cause any errors.
                    argument_list[0] = 0
                argument_bytes = self.set_args(argument_list, self.command_library[command_index][1], self.encoding)
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
            for i in range(len(self.command_library)):
                if (current_byte == self.command_library[i][0]):
                    lib_index = i
                    break
            if lib_index != -1:
                arguments_list = self.get_args(in_file, self.command_library[lib_index][1], current_byte,
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


class AI6WINScriptError(SilkyMesScriptError):
    pass
