function pacman --wraps pacman
    if _pacspin_wanted $argv
        python3 $__pacspin_script pacman $argv
    else
        command pacman $argv
    end
end
