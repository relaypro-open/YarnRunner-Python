import csv
import re
from warnings import warn
from .yarn_spinner_pb2 import Program as YarnProgram, Instruction
from .vm_std_lib import functions as std_lib_functions


class YarnRunner(object):
    def __init__(self, compiled_yarn_f, names_csv_f, autostart=True, enable_tracing=False) -> None:
        self._compiled_yarn = YarnProgram()
        self._compiled_yarn.ParseFromString(compiled_yarn_f.read())
        self._names_csv = csv.DictReader(names_csv_f)
        self.__construct_string_lookup_table()
        self._enable_tracing = enable_tracing

        self.visits = {key: 0 for key in self._compiled_yarn.nodes.keys()}
        self.variables = {}
        self.current_node = None
        self._command_handlers = {}
        self._line_buffer = []
        self._option_buffer = []
        self._vm_data_stack = ["Start"]
        self._vm_instruction_stack = [Instruction(
            opcode=Instruction.OpCode.RUN_NODE)]
        self._program_counter = 0
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

    def __find_label(self, label_key):
        labels = self._compiled_yarn.nodes[self.current_node].labels
        if label_key in labels:
            return labels[label_key]
        else:
            raise Exception(
                f"The current node `{self.current_node}` does not have a label named `{label_key}")

    def __find_expressions(self, operand):
        # TODO: implement this functionality
        if int(operand.float_value) != 0:
            raise Exception(
                f"Yarn stories with interpolated inline expressions are not yet supported.")

    def __debug_log(self, msg, **kwargs):
        if self._enable_tracing:
            print(msg, **kwargs)

    def debug_vm(self):
        print(f"VM paused: {self.paused}")
        print(f"VM finished: {self.finished}")
        self.debug_vm_instruction_stack()
        print("The current VM data stack is:")
        print(self._vm_data_stack)
        self.debug_variables()

    def debug_variables(self):
        print("The current variables stored are:")
        print(self.variables)

    def debug_vm_instruction_stack(self):
        print(f"The current node is: {self.current_node}")
        print("The current VM instruction stack is:")
        for (idx, instruction) in enumerate(self._vm_instruction_stack):
            arrow = "-->" if idx == self._program_counter else "   "
            print(
                f"{arrow} {idx}: {Instruction.OpCode.Name(instruction.opcode)}(", end='')
            print(*list(map(lambda o: o.string_value or o.float_value,
                  instruction.operands)), sep=", ", end=")\n")
        print("The current labels are:")
        print(self._compiled_yarn.nodes[self.current_node].labels)

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

    def __jump_to(self, instruction):
        self.__debug_log(
            f"__jump_to: Jump from {self._program_counter} ", end='')
        self._program_counter = self.__find_label(
            instruction.operands[0].string_value)
        self.__debug_log(f"to {self._program_counter}")

    def __jump(self, _instruction):
        if len(self._vm_data_stack) < 1 or type(self._vm_data_stack[0]) != str:
            raise Exception(
                "The JUMP opcode requires a string to be on the top of the stack. A string is not currently present.")

        self._program_counter = self.__find_label(
            self._vm_data_stack[0]
        )

    def __go_to_node(self, node_key):
        # print(f"Go from {self.current_node} to node {node_key}")
        if node_key not in self._compiled_yarn.nodes.keys():
            raise Exception(
                f"{node_key} is not a valid node in this Yarn story.")

        self.current_node = node_key
        self.visits[node_key] += 1
        self.__debug_log(
            f"__go_to_node: visits[{node_key}] = {self.visits[node_key]}")
        self._vm_instruction_stack = (
            self._compiled_yarn.nodes[node_key].instructions)
        self._program_counter = 0
        self.__process_instruction()

    def __run_line(self, instruction):
        string_key = instruction.operands[0].string_value

        # if this instruction has a second operand, it's the number of expressions
        # on the line that need to be evaluated.
        if len(instruction.operands) > 1:
            line_substitutions = self.__find_expressions(
                instruction.operands[1])
            # TODO: implement substitutions

        self._line_buffer.append(self.__lookup_string(string_key))

    def __run_command(self, instruction):
        command, * \
            args = instruction.operands[0].string_value.strip().split(" ")

        if command not in self._command_handlers.keys():
            warn(
                f"Command '{command}' does not have a registered command handler.")
        else:
            # if this instruction has a second operand, it's the number of expressions
            # on the line that need to be evaluated.
            if len(instruction.operands) > 1:
                line_substitutions = self.__find_expressions(
                    instruction.operands[1])
                # TODO: implement substitutions

            # TODO: maybe do some argument type parsing later
            self._command_handlers[command](*args)

    def __add_option(self, instruction):
        title_string_key = instruction.operands[0].string_value
        choice_path = instruction.operands[1].string_value

        # if this instruction has a second operand, it's the number of expressions
        # on the line that need to be evaluated.
        if len(instruction.operands) > 2:
            line_substitutions = self.__find_expressions(
                instruction.operands[2])
            # TODO: implement substitutions

        self._option_buffer.append({
            'index': len(self._option_buffer),
            'text': self.__lookup_string(title_string_key),
            'choice': choice_path
        })

    def __show_options(self, _instruction):
        self.paused = True

    def __push_string(self, instruction):
        self._vm_data_stack.insert(0, instruction.operands[0].string_value)

    def __push_float(self, instruction):
        self._vm_data_stack.insert(0, instruction.operands[0].float_value)

    def __push_bool(self, instruction):
        self._vm_data_stack.insert(0, instruction.operands[0].bool_value)

    def __push_null(self, _instruction):
        self._vm_data_stack.insert(0, None)

    def __jump_if_false(self, instruction):
        if self._vm_data_stack[0] == False:
            self.__jump_to(instruction)

    def __pop(self, _instruction):
        self._vm_data_stack.pop(0)

    def __call_func(self, instruction):
        function_name = instruction.operands[0].string_value
        if function_name not in std_lib_functions:
            raise Exception(
                f"The internal function `{function_name}` is not implemented in this Yarn runtime.")

        expected_params, fn = std_lib_functions[function_name]
        actual_params = int(self._vm_data_stack.pop(0))

        if expected_params != actual_params:
            raise Exception(
                f"The internal function `{function_name} expects {expected_params} parameters but received {actual_params} parameters")

        params = []
        while expected_params > 0:
            params.insert(0, self._vm_data_stack.pop(0))
            expected_params -= 1

        # invoke the function
        ret = fn(params)

        # Store the return value on the stack
        self._vm_data_stack.insert(0, ret)

    def __push_variable(self, instruction):
        variable_name = instruction.operands[0].string_value

        match = re.search(r"\$visits_([a-zA-Z\_0-9]+)", variable_name)
        if match:
            node_name = match.group(1)
            visits_lookup = {node_key.replace(".", "_"): v for (
                node_key, v) in self.visits.items()}

            if node_name not in visits_lookup:
                visits = 0
            else:
                visits = visits_lookup[node_name]
            self._vm_data_stack.insert(0, visits)
            return

        if variable_name not in self.variables:
            raise Exception(f"Variable {variable_name} has not been set.")

        self._vm_data_stack.insert(
            0, self.variables[variable_name])

    def __store_variable(self, instruction):
        self.variables[instruction.operands[0].string_value] = self._vm_data_stack[0]

    def __stop(self, _instruction):
        self.finished = True

    def __run_node(self, instruction):
        # FIXME: this is not to spec, but it's how the yarn compiler generates this opcode
        # if this opcode has a string operand, use that instead
        if (len(instruction.operands) > 0):
            node_key = instruction.operands[0].string_value
        # confirm there's a string to jump to
        else:
            if len(self._vm_data_stack) < 1 or type(self._vm_data_stack[0]) != str:
                raise Exception(
                    "The RUN_NODE opcode requires a string to be on the top of the stack. A string is not currently present.")
            else:
                node_key = self._vm_data_stack.pop(0)

        self.__go_to_node(node_key)

    def __process_instruction(self):
        if len(self._vm_instruction_stack) < 1:
            raise Exception(
                "The VM instruction stack is empty. No more instructions can be processed.")

        if self._program_counter > len(self._vm_instruction_stack) - 1:
            raise Exception(
                "The program counter has reached the end of the instruction stack without encountering a STOP opcode.")

        instruction = self._vm_instruction_stack[self._program_counter]

        opcode_functions = {
            Instruction.OpCode.JUMP_TO: self.__jump_to,
            Instruction.OpCode.JUMP: self.__jump,
            Instruction.OpCode.RUN_LINE: self.__run_line,
            Instruction.OpCode.RUN_COMMAND: self.__run_command,
            Instruction.OpCode.ADD_OPTION: self.__add_option,
            Instruction.OpCode.SHOW_OPTIONS: self.__show_options,
            Instruction.OpCode.PUSH_STRING: self.__push_string,
            Instruction.OpCode.PUSH_FLOAT: self.__push_float,
            Instruction.OpCode.PUSH_BOOL: self.__push_bool,
            Instruction.OpCode.PUSH_NULL: self.__push_null,
            Instruction.OpCode.JUMP_IF_FALSE: self.__jump_if_false,
            Instruction.OpCode.POP: self.__pop,
            Instruction.OpCode.CALL_FUNC: self.__call_func,
            Instruction.OpCode.PUSH_VARIABLE: self.__push_variable,
            Instruction.OpCode.STORE_VARIABLE: self.__store_variable,
            Instruction.OpCode.STOP: self.__stop,
            Instruction.OpCode.RUN_NODE: self.__run_node,
        }

        self._program_counter += 1

        if instruction.opcode not in opcode_functions:
            if (len(instruction.operands) > 0):
                print(instruction.operands)
            raise Exception(
                f"OpCode {Instruction.OpCode.Name(instruction.opcode)} is not yet implemented")

        opcode_functions[instruction.opcode](instruction)

        if not self.paused and not self.finished:
            self.__process_instruction()
