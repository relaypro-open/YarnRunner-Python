import csv
from .yarn_spinner_pb2 import Program as YarnProgram, Instruction


class YarnRunner(object):
    def __init__(self, compiled_yarn_f, names_csv_f, autostart=True) -> None:
        self._compiled_yarn = YarnProgram()
        self._compiled_yarn.ParseFromString(compiled_yarn_f.read())
        self._names_csv = csv.DictReader(names_csv_f)
        self.__construct_string_lookup_table()

        self.visits = {key: 0 for key in self._compiled_yarn.nodes.keys()}
        self._command_handlers = {}
        self._line_buffer = []
        self._option_buffer = []
        self._vm_data_stack = ["Start"]
        self._vm_instruction_stack = [Instruction(
            opcode=Instruction.OpCode.RUN_NODE)]
        self.paused = True
        self.finished = False

        if autostart:
            self.resume()

    def __construct_string_lookup_table(self):
        self.string_lookup_table = dict()

        for entry in self._names_csv:
            self.string_lookup_table[entry["id"]] = entry

    def resume(self):
        # confirm there's a string to jump to
        if len(self._vm_data_stack) < 1 or type(self._vm_data_stack[0]) != str:
            raise Exception(
                "Attempted to resume play from selecting an option, but no option has been selected.")

        self.paused = False
        self.__process_instruction()

    def __lookup_string(self, string_key):
        if string_key not in self.string_lookup_table:
            raise Exception(
                f"{string_key} is not a key in the string lookup table.")
        else:
            return self.string_lookup_table[string_key]["text"]

    def debug_vm(self):
        print(f"VM paused: {self.paused}")
        print("The current VM instruction stack is:")
        for (idx, instruction) in enumerate(self._vm_instruction_stack):
            print(f"    {idx}: {Instruction.OpCode.Name(instruction.opcode)}")
        print("The current VM data stack is:")
        print(self._vm_data_stack)

    def debug_program_proto(self):
        print("The protobuf representation of the current program is:")
        print(self._compiled_yarn)

    ##### Public functions to surface via API below here #####

    def get_line(self):
        return self._line_buffer.pop(0)

    def print_line(self):
        print(self.get_line())

    def has_line(self):
        return len(self._line_buffer) > 0

    def get_lines(self):
        lines = self._line_buffer
        self._line_buffer = []
        return lines

    def print_all_lines(self):
        lines = self.get_lines()
        for line in lines:
            print(line)

    def get_choices(self):
        return self._option_buffer

    def choose(self, index):
        choice = self._option_buffer[index]
        self._option_buffer = []
        self._vm_data_stack.insert(0, choice["choice"])
        self.resume()

    def add_command_handler(self, command, fn):
        self._command_handlers[command] = fn

    ##### OpCode Implementations below here #####

    def __go_to_node(self, node_key):
        if node_key not in self._compiled_yarn.nodes.keys():
            raise Exception(
                f"{node_key} is not a valid node in this Yarn story.")

        self.visits[node_key] += 1
        self._vm_instruction_stack.extend(
            self._compiled_yarn.nodes[node_key].instructions)
        self.__process_instruction()

    def __run_line(self, instruction):
        string_key = instruction.operands[0].string_value

        self._line_buffer.append(self.__lookup_string(string_key))

    def __run_command(self, instruction):
        command, *args = instruction.operands[0].string_value.split(" ")
        if command not in self._command_handlers.keys():
            raise Exception(
                f"Command '{command}' does not have a registered command handler.")
        else:
            # TODO: maybe do some argument parsing later
            self._command_handlers[command](*args)

    def __add_option(self, instruction):
        title_string_key = instruction.operands[0].string_value
        choice_path = instruction.operands[1].string_value

        self._option_buffer.append({
            'index': len(self._option_buffer),
            'text': self.__lookup_string(title_string_key),
            'choice': choice_path
        })

    def __show_options(self, _instruction):
        self.paused = True

    def stop(self, _instruction):
        self.finished = True

    def __run_node(self, _instruction):
        # confirm there's a string to jump to
        if len(self._vm_data_stack) < 1 or type(self._vm_data_stack[0]) != str:
            raise Exception(
                "The RUN_NODE opcode requires a string to be on the top of the stack. A string is not currently present.")

        node_key = self._vm_data_stack.pop(0)
        self.__go_to_node(node_key)

    def __process_instruction(self):
        if len(self._vm_instruction_stack) < 1:
            raise Exception(
                "The VM instruction stack is empty. No more instructions can be processed.")

        instruction = self._vm_instruction_stack.pop(0)

        def noop(instruction):
            if (len(instruction.operands) > 0):
                print(instruction.operands)
            raise Exception(
                f"OpCode {Instruction.OpCode.Name(instruction.opcode)} is not yet implemented")

        opcode_functions = {
            Instruction.OpCode.JUMP_TO: noop,
            Instruction.OpCode.JUMP: noop,
            Instruction.OpCode.RUN_LINE: self.__run_line,
            Instruction.OpCode.RUN_COMMAND: self.__run_command,
            Instruction.OpCode.ADD_OPTION: self.__add_option,
            Instruction.OpCode.SHOW_OPTIONS: self.__show_options,
            Instruction.OpCode.PUSH_STRING: noop,
            Instruction.OpCode.PUSH_FLOAT: noop,
            Instruction.OpCode.PUSH_BOOL: noop,
            Instruction.OpCode.PUSH_NULL: noop,
            Instruction.OpCode.JUMP_IF_FALSE: noop,
            Instruction.OpCode.POP: noop,
            Instruction.OpCode.CALL_FUNC: noop,
            Instruction.OpCode.PUSH_VARIABLE: noop,
            Instruction.OpCode.STORE_VARIABLE: noop,
            Instruction.OpCode.STOP: self.stop,
            Instruction.OpCode.RUN_NODE: self.__run_node,
        }

        opcode_functions[instruction.opcode](instruction)

        if not self.paused and not self.finished:
            self.__process_instruction()
