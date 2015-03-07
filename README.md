# Python Output Format

A simple plugin for Sublime Text inspired by [Pretty JSON](https://packagecontrol.io/packages/Pretty JSON) for formatting printed output from Python programs into a more easily readable format.

The plugin simply adds one action, cleverly named "Python Output Format", which either takes the text you have selected, or, if nothing is selected, the entire active document, and attempts to format it in a way that is more easy to read.

It will for instance turn this blob:

    {'details': 'https://github.com/Tenzer/PythonOutputFormat', 'releases': [{'sublime_text': '*', 'tags': True}], 'name': 'Python Output Format'}```

into this:

    {
        'details': 'https://github.com/Tenzer/PythonOutputFormat',
        'releases': [
            {
                'sublime_text': '*',
                'tags': True 
            }
        ],
        'name': 'Python Output Format'
    }


# Installation

The package is available via [Package Control](https://sublime.wbond.net/) under the name "Python Output Format".
