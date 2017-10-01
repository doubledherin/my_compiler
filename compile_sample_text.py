from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from instruction_generator import InstructionGenerator
from instruction_interpreter import InstructionInterpreter

sample_text = """
var x, y, z : int;

function foo (p, q : int; n, m : int) {
    p = p + 5;
    q = q * 10;
    n = n - 4;
    m = m / 3;
}

function bar (r, s : int; t, u : int) {
    r = r + 5;
    s = s * 10;
    t = t - 4;
    u = u / 3;
}

print (3 + 3) * (3 - 3); # 0
"""

def compile_sample_text():
    print "\nSample text is: \n"
    rule =  "------------------\n"
    print rule
    print sample_text
    print rule
    print "Lexing ..."
    try:
        lexer = Lexer(sample_text)
        print "Lexing successful!"
    except:
        raise Exception('Error while lexing :(')
    print "Creating parser ..."
    try:
        parser = Parser(lexer)
        print "Parser creation successful!"
    except:
        raise Exception('Error while creating parser :(')
    print "Parsing ..."
    try:
        tree = parser.parse()
        print "Parsing successful!"
        print "Would you like to see the abstract syntax tree as JSON?"
        answer = raw_input("y/n")
        if answer == "y":
            print tree.toJSON()
    except:
        raise Exception('Error while generating abstract syntax tree :(')
    print "Creating semantic analyzer ..."
    try:
        semantic_analyzer = SemanticAnalyzer()
        print "Creation of semantic analyzer successful!"
    except:
        raise Exception('Error while creating semantic analyzer :(')
    print "Analyzing semantics ..."
    try:
        semantic_analyzer.visit(tree)
        print "Semantic analysis successful!"
    except:
        raise Exception('Error while analyzing semantics :(')
    print "Creating instruction generator ..."
    try:
        instruction_generator = InstructionGenerator()
        print "Creation of instruction generator successful!"
    except:
        raise Exception('Error while creating instruction generator :(')
    print "Generating instructions ..."
    try:
        instruction_generator.visit(tree)
        print "Instruction generation successful!"
    except:
        raise Exception('Error while generating instructions')
    print "Creating instruction interpreter..."
    try:
        instruction_interpreter = InstructionInterpreter()
        print "Creation of instruction interpreter successful!"
    except:
        raise Exception('Error while creating instruciton interpreter')
    print "Running instruction interpreter ..."
    try:
        print "Output is ..."
        instruction_interpreter.run_code(instruction_generator.code)
    except:
        raise Exception('Error while interpreting instructions')

if __name__ == '__main__':
    compile_sample_text()


    # while True:
    #     try:
    #         text = raw_input('wendy>')
    #     except EOFError:
    #         break
    #     if not text:
    #         continue
    #     lexer = Lexer(text)
    #     parser = Parser(lexer)
    #     interpreter = Interpreter(parser)
    #     result = interpreter.interpret()
    #     print result
