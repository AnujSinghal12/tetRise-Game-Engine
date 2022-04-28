import fileinput
from sly import Parser
from tetris_lex import TetRiseLexer


class TetRiseParser(Parser):
    tokens = TetRiseLexer.tokens

    # File for outputting parser logs for debugging.
    debugfile = 'parser_debug.out'

    # Multiplication has a higher precedence than addition/subtraction.
    precedence = (
        ('left', ADDITION, SUBTRACTION),
        ('left', MULTIPLICATION, DIVISION),
        # ('left', "."),  # To handle float types, we need to evaluate "." first.
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        # A statement can be empty in which case nothing is done.
        pass

    @_('FOR variable_assign condition expr statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.variable_assign, p.expr), p.statement)

    @_('INDENT BOARD_SIZE expr expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.BOARD_SIZE, p.expr0, p.expr1))

    @_('INDENT SIZE expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.SIZE, p.expr))

    @_('INDENT GRAVITY expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.GRAVITY, p.expr))

    @_('INDENT ROTATION expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.ROTATION, p.expr))

    @_('INDENT POINTS expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.POINTS, p.expr))

    @_('INDENT SHAPE ARRAY')    
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.SHAPE, p.ARRAY))

    @_('BLOCK ')
    def statement(self, p):
        return ('block_declaration', p.BLOCK,)
    
    @_('GAME')
    def statement(self, p):
        return ('game_declaration', p.GAME,)

    @_('SCORE expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.SCORE, p.expr))

    @_('CONFIG LEFT expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.CONFIG, p.LEFT, p.expr))

    @_('CONFIG RIGHT expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.CONFIG, p.RIGHT, p.expr))  

    @_('CONFIG PAUSE expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.CONFIG, p.PAUSE, p.expr))

    @_('CONFIG ROTATE expr')
    def statement(self, p):
        return ('assign_keyword', ('assign_keyword_setup', p.CONFIG, p.ROTATE, p.expr))  

    @_('IF condition statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('expr EQUAL expr')
    def condition(self, p):
        return ('condition_equal', p.expr0, p.expr1)

    @_('expr LESS expr')
    def condition(self, p):
        return ('condition_less', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def condition(self, p):
        return ('condition_greater', p.expr0, p.expr1)

    @_('variable_assign')
    def statement(self, p):
        return p.variable_assign

    @_('IDENTIFIER ASSIGN NUMBER')
    def variable_assign(self, p):
        return ('variable_assign', p.IDENTIFIER, p.number)

    @_('IDENTIFIER ASSIGN expr')
    def variable_assign(self, p):
        return ('variable_assign', p.IDENTIFIER, p.expr)

    @_('IDENTIFIER ASSIGN STRING')
    def variable_assign(self, p):
        return ('variable_assign', p.IDENTIFIER, p.STRING)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr ADDITION expr')
    def expr(self, p):
        return ('addition', p.expr0, p.expr1)

    @_('expr SUBTRACTION expr')
    def expr(self, p):
        return ('subtraction', p.expr0, p.expr1)

    @_('expr MULTIPLICATION expr')
    def expr(self, p):
        return ('multiplication', p.expr0, p.expr1)

    @_('expr DIVISION expr')
    def expr(self, p):
        return ('division', p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('IDENTIFIER')
    def expr(self, p):
        return ('var', p.IDENTIFIER)

    @_('STRING')
    def expr(self, p):
        return ('num', p.STRING)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('ARRAY')
    def expr(self, p):
        return ('array', p.ARRAY)


if __name__ == '__main__':
    lexer = TetRiseLexer()
    parser = TetRiseParser()
    env = {}
    with open('tetRiseCode.txt') as f:
       data = f.read()
    data = data.replace("    ", "\t")
    print(data)
    data2 = "Block\n\tGravity 100"
    data = data+'\n'
    everyline = ""
    for char in data:
        if ord(char) == 10:
            tree = parser.parse(lexer.tokenize(everyline))
            print(tree)
            everyline = ""

        everyline = everyline+char
        if ord(char) == 10:
            everyline=""