import sublime, sublime_plugin
import tokenize
from io import BytesIO


class PythonOutputFormatCommand(sublime_plugin.TextCommand):
    indentation_level = 0

    def indent(self):
        return (tokenize.INDENT, ' ' * 4 * self.indentation_level)

    def run(self, edit):
        NEWLINE = (tokenize.NL, '\n')
        result = []
        entire_document = sublime.Region(0, self.view.size())
        data_input = tokenize.tokenize(BytesIO(self.view.substr(entire_document).encode('utf-8')).readline)

        for token in data_input:
            if token.type == tokenize.OP:
                if token.exact_type in [tokenize.LBRACE, tokenize.LSQB]:
                    result.append(self.indent())
                    result.append((token.exact_type, token.string))
                    result.append(NEWLINE)
                    self.indentation_level += 1
                elif token.exact_type in [tokenize.RBRACE, tokenize.RSQB]:
                    if result[-1] != NEWLINE:
                        result.append(NEWLINE)
                    self.indentation_level -= 1
                    result.append(self.indent())
                    result.append((token.exact_type, token.string))
                elif token.exact_type == tokenize.COLON:
                    result.append((token.exact_type, token.string))
                    result.append((tokenize.STRING, ' '))
                elif token.exact_type == tokenize.COMMA:
                    result.append((token.exact_type, token.string))
                    result.append(NEWLINE)
                else:
                    result.append((token.exact_type, token.string))
            elif token.type != tokenize.NL:
                result.append(self.indent())
                result.append((token.exact_type, token.string))

        result.append(NEWLINE)
        self.view.replace(edit, entire_document, tokenize.untokenize(result).decode('utf-8'))
