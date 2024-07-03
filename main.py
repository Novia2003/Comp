import os
from src.AST.Parser import *
from src.Semantics.semantic_analyzer import *
from src.Сompiler.code_generator import *
from src.VM.VirtualMachine import *

prog = '''
    var i = 5;
    do {
        if(i >= 7)
            logprint(i);
        i++;
    } while(i < 10)
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