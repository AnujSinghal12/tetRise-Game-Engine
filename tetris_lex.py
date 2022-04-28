from shutil import ignore_patterns
from sly import Lexer

class TetRiseLexer(Lexer):
    tokens = {
        UNIT, ARRAY, IDENTIFIER, NUMBER, STRING, ADDITION, SUBTRACTION, MULTIPLICATION, DIVISION, AND, OR, EQUAL,
        NOTEQUAL, LESS, GREATER, LEFT_PAR, LEFT_SQ_PAR, RIGHT_PAR, RIGHT_SQ_PAR, COLON,
        IDENTIFIER, GAME, BOARD_SIZE, GRAVITY, ROTATION, POINTS, BLOCK, SHAPE, SIZE, SCORE, CONFIG,
        LEFT, RIGHT, PAUSE, ROTATE, IF, ELSE, FOR, ASSIGN, INDENT
    }

    ignore = ' '
    # Other patterns to ignore
    ignore_comment = r'\#.*'
    ignore_newline = r'\n'

    literals = {'(', ')', ',', ':', '!', '.'}

    # Define each token as a regular expression.
    INDENT = r'\t'
    ARRAY = r'\[(\(([0,1]\,)*[0,1]\)\,)*(\(([0,1]\,)*[0,1]\))\]'
    IF = r'IF'
    ELSE = r'ELSE'
    FOR = r'FOR'
    ASSIGN = r'='
    LEFT_PAR = r'\('
    RIGHT_PAR = r'\)'
    LEFT_SQ_PAR = r'\['
    RIGHT_SQ_PAR = r'\]'
    COLON = r'\:'
    ADDITION = r'\+'
    SUBTRACTION = r'\-'
    MULTIPLICATION = r'\*'
    DIVISION = r'/'
    OR = r'\|\|'
    AND = r'\&\&'
    EQUAL = r'(===|==)'
    NOTEQUAL = r'(!==|!=)'
    GREATER = r'(>=|>)'
    LESS = r'(<=|<)'
    STRING = r'\".*?\"'
    
    @_(r"(0|[1-9][0-9]*)")
    def NUMBER(self, num):
        """Number token type."""
        num.value = int(num.value)
        return num

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, string):
        """Strings are represented using double quotes."""
        string.value = str(string.value)
        return string

    # Keywords
    # Identifier comes after STRING defined above.
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['Game'] = GAME
    IDENTIFIER['BoardSize'] = BOARD_SIZE
    IDENTIFIER['Gravity'] = GRAVITY
    IDENTIFIER['Rotation'] = ROTATION
    IDENTIFIER['Points'] = POINTS
    IDENTIFIER['Block'] = BLOCK
    IDENTIFIER['Size'] = SIZE
    IDENTIFIER['Shape'] = SHAPE
    IDENTIFIER['Score'] = SCORE
    IDENTIFIER['Config'] = CONFIG
    IDENTIFIER['Left'] = LEFT
    IDENTIFIER['Right'] = RIGHT
    IDENTIFIER['Pause'] = PAUSE
    IDENTIFIER['Rotate'] = ROTATE

    def error(self, t):
        """Custom error message to handle bad characters."""
        print(f"Line {self.lineno}: Bad character {t.value[0]!r}")
        self.index += 1

    # To track line number.
    # @_(r'\n+')
    # def ignore_newline(self, t):
    #     self.lineno += t.value.count('\n')


def main():
    lexer = TetRiseLexer()
    while True:
        text = input(">>> ")
        tokens = lexer.tokenize(text)  # Creates a generator of tokens
        print(list(tokens))


if __name__ == "__main__":
    main()
