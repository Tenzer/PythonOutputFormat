"""Sublime Text plugin to format the output of Python programs nicely."""

import re
import tokenize
from io import BytesIO

import sublime
import sublime_plugin


class PythonOutputFormatCommand(sublime_plugin.TextCommand):

    """The Sublime Text plugin class."""

    indentation_level = 0
    newline = (tokenize.NL, '\n')
    indentation = '    '
    extra_spaces_regex = re.compile(r' (,?)$', re.MULTILINE)

    def set_indentation(self):
        """Set internal variable based on the indentation settings of the document."""
        if self.view.settings().get('translate_tabs_to_spaces'):
            self.indentation = ' ' * self.view.settings().get('tab_size')
        else:
            self.indentation = '\t'

    def indent(self):
        """Return the indentation needed at the current level."""
        return (tokenize.INDENT, self.indentation * self.indentation_level)

    def fix_extra_spaces(self, text):
        """Remove extra trailing spaces inserted by the tokenize module."""
        return self.extra_spaces_regex.sub(r'\1', text)

    def fix_ending_newlines(self, text):
        """Remove any excess newlines and make sure we always end with one newline."""
        return text.rstrip() + '\n'

    def run(self, edit):
        """Main function which is called when the plugin is activated."""
        self.set_indentation()

        for region in self.view.sel():
            if region.empty():
                region = sublime.Region(0, self.view.size())

            region_data = self.view.substr(region).encode('utf-8')
            result = []

            try:
                for token in tokenize.tokenize(BytesIO(region_data).readline):
                    if token.type == tokenize.OP:
                        if token.exact_type in [tokenize.LBRACE, tokenize.LSQB]:
                            result.append(self.indent())
                            result.append((token.exact_type, token.string))
                            result.append(self.newline)
                            self.indentation_level += 1
                        elif token.exact_type in [tokenize.RBRACE, tokenize.RSQB]:
                            if result[-1] != self.newline:
                                result.append(self.newline)
                            self.indentation_level -= 1
                            result.append(self.indent())
                            result.append((token.exact_type, token.string))
                        elif token.exact_type == tokenize.COLON:
                            result.append((token.exact_type, token.string))
                            result.append((tokenize.STRING, ' '))
                        elif token.exact_type == tokenize.COMMA:
                            result.append((token.exact_type, token.string))
                            result.append(self.newline)
                        else:
                            result.append((token.exact_type, token.string))
                    elif token.type != tokenize.NL:
                        result.append(self.indent())
                        result.append((token.exact_type, token.string))
            except tokenize.TokenError as error:
                sublime.status_message(str(error))
                return

            result_string = tokenize.untokenize(result).decode('utf-8')
            result_string = self.fix_extra_spaces(result_string)
            result_string = self.fix_ending_newlines(result_string)

            self.view.replace(edit, region, result_string)

        if self.view.settings().get('syntax') == 'Packages/Text/Plain text.tmLanguage':
            self.view.set_syntax_file('Packages/Python/Python.tmLanguage')
