# ----11-02-2024 20:01:21----
# A system for remembering bash commands
# relies on and called from the hint() function in hints.sh

from simple_term_menu import TerminalMenu
import os
import argparse
import bashlex
import textwrap

def splitCodeComment(bashline):
    try:
        parts = bashlex.parse(bashline)
        cmdEndIx = parts[-1].pos[1]
        return (bashline[:cmdEndIx], bashline[cmdEndIx:])
    except:
        sp = bashline.split('#')
        return sp[0], '#' + '#'.join(sp[1:]) + " # (bashlex parsing error) "

script_dir = os.path.dirname(os.path.realpath(__file__))
# You can put the menusDir somewhere else if you like, with your other technical notes. Just export the HINT_MENUS_DIR bash variable
menusDir = None
if "HINT_MENUS_DIR" in os.environ:
    menusDir = os.path.expanduser(os.environ["HINT_MENUS_DIR"])
    if not os.path.isdir(menusDir):
        menusDir = None
        print("Ignoring invalid HINT_MENUS_DIR")
if menusDir == None:        
    menusDir = os.path.join(script_dir, "menus")
outputFile = os.path.join(script_dir, "out.txt")

def loadMenu(filename = "home.menu"):
    "Load a menu. Returns None in case the user aborted."
    with open(os.path.join(menusDir, filename)) as f:
        lines = f.read().split("\n")
    lines = [l for l in lines if l.strip() != ""]
    displayLines = []
    nocommentLines = []
    commentLines = []
    clipped = []
    indexMap = {} # map from displayLine to index
    for i,l in enumerate(lines):
        # the comments are often longer than fit as a menu item
        # so we'll display them as a preview, unless they are short
        nocomment, comment = splitCodeComment(l)
        commentLines.append(comment)
        nocommentLines.append(nocomment)
        if len(l) < 60:
            clipped.append(False)
        else:
            clipped.append(True)
        display = l
        indexMap[display] = i
        display = display.replace("|", "\\|")
        displayLines.append(display)

    def show_comment(display):
        i = indexMap[display]
        if not clipped[i]:
            return None
        wrappedCode = "\\\n  ".join(textwrap.wrap(nocommentLines[i]))
        
        return '\n'.join(['\n'.join(commentLines[i].split("#")[1:]), wrappedCode])
        
    while True:
        terminal_menu = TerminalMenu(displayLines, preview_command=show_comment)
        ix = terminal_menu.show()
        if ix == None:
            return None
        else:
            result = selectItem(lines[ix])
            if result != None:
                return result

def selectItem(item):
    "Load the new selection: a menu or a bash command."
    code, _ = splitCodeComment(item)
    if code[-5:] == ".menu":
        return loadMenu(code)
    else:
        print(item)
        print("Press the up arrow to retrieve the command from bash history.")
        with open(outputFile, "w") as f:
            f.write(code)
        return item
    
if __name__ == "__main__":
    with open(outputFile, "w") as f:
        f.write("") # clear it in case the user doesn't select anything
    helptext = \
        """    
        A system for organizing your bash commands so you don't have to
        remember them and can just select them from a menu. Once you
        select them, they will be set as the last history item. Press
        up-arrow to get them at the bash prompt, where you can edit them
        if necessary before running them.

        Place commands you want to use again later in $HINTS_MENU_DIR/*.menu
        files, one per line. You may use # after the command, on the same
        line, to describe what it does. Additional # in your comment will
        be displayed as newlines. If you list a .menu file within another
        .menu file, the listed menu can be accessed as a sub-menu."""
    helptext = textwrap.dedent(helptext)
    parser = argparse.ArgumentParser(description=helptext,formatter_class=argparse.RawTextHelpFormatter, prog="hint")
    parser.add_argument('menu', nargs='?', type=str, default="home.menu", help="The name of the menu you wish to start from, \noptionally omitting the .menu extension.\n Default: home.menu ")
    args = parser.parse_args()
    if args.menu[-5:] != ".menu":
        args.menu += ".menu"
    if not os.path.exists(os.path.join(menusDir, args.menu)):
        print("Menu not found:", args.menu)
        print("Defaulting to home.menu")
        args.menu = "home.menu"
    loadMenu(args.menu)
