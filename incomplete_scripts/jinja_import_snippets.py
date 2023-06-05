# {{ ... }}

# {{ 1:specified_cursor_order }}

# $1, $2, $3, etc.: These are placeholders for tab stops in the snippet. When the user inserts the snippet, they can press the Tab key to move between the tab stops and fill in the required values.

# ${1:default_value}: This is a placeholder with a default value. When the user inserts the snippet, the default value will be pre-filled in the placeholder, and the user can edit it if necessary.

# ${TM_FILENAME_BASE}: This is a variable that expands to the base name of the current file (i.e., the file name without the extension).

# ${TM_SELECTED_TEXT}: This is a variable that expands to the currently selected text in the editor.

# ${TM_CURRENT_LINE}: This is a variable that expands to the current line in the editor.

# ${TM_CURRENT_WORD}: This is a variable that expands to the current word under the cursor in the editor.

# ${TM_LINE_NUMBER}: This is a variable that expands to the current line number in the editor.

# ${TM_DIRECTORY}: This is a variable that expands to the directory of the current file.

# ${TM_FILEPATH}: This is a variable that expands to the full path of the current file.

# {# comment not rendered in output #}

# > [!NOTE] Warning
# > possible issue with jinja variable interpolation needing double curly braces not single