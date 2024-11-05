hint()
{
    history -s "hint $@"
    $HINT_DIR/.env/bin/python3 $HINT_DIR/hint.py $@
    out="$(<$HINT_DIR/out.txt)"
    if [ -n "$out" ] ; then
        history -s "$out"
    fi
}
