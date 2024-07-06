import os
from src.AST.Parser import *
from src.Semantics.semantic_analyzer import *
from src.Сompiler.code_generator import *
from src.VM.VirtualMachine import *

prog = '''
    function fibonacci(n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    }

    var i = 0;
    while (i < 10) {
        var result = fibonacci(i);
        logprint(result + 1);
        i = i + 1;
    }
'''
parser = Parser()
analyzer = Analyzer()
res = parser.parse(prog)
print(*res.tree, sep=os.linesep)

analyzer.analyze(res)
if len(analyzer.errors) > 0:
    for e in analyzer.errors:
        print("Ошибка: {}".format(e.message))
else:
    print("Ошибок не обнаружено.")
    generator = CodeGenerator(res)
    generator.print_bytecode()
    vm = VirtualMachine(generator.lines)