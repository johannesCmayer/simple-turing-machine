from copy import deepcopy


class Instruction:
    def __init__(self, state, reading, write, move, new_state):
        self.state = state
        self.reading = reading
        self.write = write
        self.move = move
        self.new_state = new_state

    def is_halt(self):
        return self.state == 0

    def __str__(self):
        return f"{self.state}, {self.reading}, {self.write}, {self.move}, {self.new_state}"


class Program:
    def __init__(self, start_idx, start_state, start_memory, instructions):
        self.start_idx = start_idx 
        self.start_state =start_state 
        self.start_memory = start_memory
        self.instructions = instructions

        self.validate_instructions()
    
    def validate_instructions(self):
        ins = self.instructions
        new_states = set([x.new_state for x in ins]) 
        states = set([x.state for x in ins])
        assert len(new_states.difference(states)) == 0, \
            f"The machine can enter states ({new_states.difference(states)}) that have no intruction!"

        for current_state in states:
            for mem in set(self.start_memory).union(set([x.write for x in ins])):
                ins = [i for i in ins if i.state == current_state and i.reading == mem]
                assert len(ins) <= 1, f"Multiple instructions match state and reading ({current_state}, {mem}): {[str(i) for i in ins]}"

    def run(self):
        memory, instructions = deepcopy(self.start_memory), deepcopy(self.instructions)
        current_idx = self.start_idx
        current_state = self.start_state
        while True:
            assert current_idx < len(memory), f"Memory index is out of range (current: {current_idx}, mem_len: {len(memory)})"
            mem = memory[current_idx]
            if current_state == 0 or mem == 2:
                return memory
            ins = [i for i in instructions if i.state == current_state and i.reading == mem]
            assert len(ins) > 0, f"No instructions match state {current_state} and reading {mem}"
            ins = ins[0]
            memory[current_idx] = ins.write
            current_idx += ins.move
            current_state = ins.new_state


def run_program(program):
    output = program.run()
    print("Input:")
    print(invert_bits.start_memory)
    print("Output")
    print(output)


if __name__ == "__main__":
    invert_bits = Program(
        start_idx = 0,
        start_state = 1,
        start_memory = [1, 1, 0, 0, 0, 1, 1, 2],
        instructions = [
        #               s  r  w  m  ns
            Instruction(0, 0, 0, 0, 0),
            Instruction(1, 0, 1, 1, 1),
            Instruction(1, 1, 0, 1, 1),
        ]
    )

    run_program(invert_bits)

