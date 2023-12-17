import sys

class Hwalang:

    def __init__(self, size=32768):
        self.memory = [0] * size 
        self.code = "" 
        self.ptr = 0  
        self.pc = 0  
        self.jumpTo = {} 

    def load(self, code):
        start = "사관생도 신조!"
        end = "이상 점호 끝!"
        start_idx = code.find(start)
        if start_idx == -1:
            raise ValueError("악! 열외!")
        end_idx = code.find(end, start_idx + len(start))
        if end-idx == -1:
            raise ValueError("악! 열외!")
        self.code = code[start_idx + len(start):end_idx]
        self.code = list(self.code)

    def increasePtr(self):
        if self.ptr >= len(self.memory) - 1:
            raise ValueError("악! 메모리 열외!")
        self.ptr += 1

    def decreasePtr(self):
        if self.ptr <= 0:
            raise ValueError("악! 메모리 열외!")
        self.ptr -= 1

    def increaseValue(self):
        self.memory[self.ptr] += 1

    def decreaseValue(self):
        self.memory[self.ptr] -= 1

    def printValue(self):
        sys.stdout.write(chr(self.memory[self.ptr]))
        sys.stdout.flush()

    def storingValue(self):
        buffer = sys.stdin.read(1)
        if buffer:
            self.memory[self.ptr] = ord(buffer)

    def jump(self, command):
        if command == "명" and self.memory[self.ptr] == 0:
            self.pc = self.jumpTo[self.pc]
        elif command == "법" and self.memory[self.ptr] != 0:
            self.pc = self.jumpTo[self.pc]

    def preprocess(self):
        stack = []
        for i in range(len(self.code)):
            command = self.code[i]
            if command == "명":
                stack.append(i)
            elif command == "법":
                if len(stack) == 0:
                    raise ValueError("악! 조건문 열외!")
                start_position = stack.pop()
                self.jumpTo[i] = start_position
                self.jumpTo[start_position] = i

        if stack:
            raise ValueError("악! 조건문 열외!")

    def run(self):
        while self.pc < len(self.code):
            command = self.code[self.pc]

            if command == "정":
                self.increasePtr()
                self.pc += 1
            elif command == "국":
                self.decreasePtr()
                self.pc += 1
            elif command == "상":
                self.increaseValue()
                self.pc += 1
            elif command == "실":
                self.decreaseValue()
                self.pc += 1
            elif command == "훈":
                self.printValue()
                self.pc += 1
            elif command == "육":
                self.storingValue()
                self.pc += 1
            elif command == '명' or command == '법':
                self.jump(command)
                self.pc += 1

            self.pc += 1

if len(sys.argv) < 2:
    print("Usage: python hwalang.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    with open(input_file, "r") as file:
        code = file.read()
        hl = Hwalang()
        hl.load(code)
        hl.preprocess()
        hl.run()
        print()  
except FileNotFoundError:
    print("악! 입력값 열외!")
except Exception:
    print("열외!")
