from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Keyword, Name, Number, Punctuation


class AQALexer(RegexLexer):
    name = 'AQA'
    aliases = ['aqa']
    filenames = ['*.aqa']

    tokens = {
        'root': [
            # Whitespace and comments
            (r'\s+', Text),
            (r'/.*$', Comment.Single),

            # Keywords (Instructions)
            (r'\b(?i)(mov|add|sub|and|orr|not|cmp|b|beq|bnq|blt|bgt|halt|out|inp)\b', Keyword),

            # Registers
            (r'\b(?i)(r[0-9]|r[0-9][0-2])\b', Name.Variable),

            # Labels
            (r'^[A-Za-z_][A-Za-z0-9_]*:', Name.Label),

            # Numbers (decimal, hex)
            (r'\b0x[0-9A-Fa-f]+\b', Number.Hex),
            (r'\b\d+\b', Number.Integer),

            # Identifiers (variable names, function names)
            (r'[A-Za-z_][A-Za-z0-9_]*', Name),

            # Punctuation
            (r'[\[\](),]', Punctuation),
        ]
    }
