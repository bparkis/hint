# hint

Hint is a bash menu system for people like me who forget the exact syntax for miscellaneous bash commands they haven't used in a while. The idea is, you navigate to the command you want in the menu and select it. The menu exits and you're back at the bash prompt, but the command is now in your bash history, so you can press the up arrow to get it. Then you can edit the command (if necessary) and run it. It's similar to copy-pasting a command from a text file or a web site, but much quicker and more direct.

Hint is a thin wrapper around simple-term-menu. It comes with menus providing a variety of bash commands I found useful at one time or another, but you can add your own or remove what you don't want.

To set it up:

1. Download the project to somewhere and run setup.py. It will set up the python environment and ask you if you want to set up your .bashrc for hint. This will add the following lines to the end of your .bashrc:
```
HINT_DIR=~/path/to/hint
source $HINT_DIR/hint.sh
# export HINT_MENUS_DIR=/path/to/hint/menus
```
You can say no and do this manually if you prefer.

2. `source ~/.bashrc` to activate hint in your current bash session.

3. Write menus like the example ones, and put them in `$HINT_MENUS_DIR`, or just rely on the example ones for now.

4. Type `hint` at the bash prompt to enter the home menu and see how it works. Or `hint some_menu` to open that specific menu file directly. The path is relative to `$HINT_MENUS_DIR`, and the .menu extension is optional here.

Some example menus are provided. But the idea is that you will fill your menus with the commands that you actually have a history of using, and delete what you don't need.

Good candidates for menu items would be commands that you use occasionally but are liable to forget, especially if they use complicated or obscure options. If you've just been searching on the web for a solution to some problem, it's a good idea to put all the commands for that solution in a menu, where you will be able to find it much more quickly next time without even having to leave bash. Locations of certain files are good candidates for menu items too.

If you're like me, you've built up text files over the years of useful commands. Putting these commands in menus lets you access them more directly. It's almost like having a good memory!

A menu file must have the extension .menu and be in the menus directory or a subdirectory. Each line of the menu file is another menu option. It should consist of a bash command, optionally followed by a pound sign `#` and a comment. You can use additional `#` signs on long comments so they will display as multiple lines in the menus. The comments must be on a single line in the .menu file, though. If you want to store non-bash-command information in your menu, you could have a line that's only a comment.

The menus can link to each other. Just put the filename of a menu, relative to the menus directory and including the .menu extension, on a line by itself. If you have navigated from a menu to a sub-menu, you can press ESC to go back to the previous menu, or to exit the program if you're at the initial menu.

You can press / to search for a term within the current menu. So, you can have quite a long menu and still easily navigate it, especially if you put tags in your comments.

That's about it. Hint isn't fancy, but it's functional.
