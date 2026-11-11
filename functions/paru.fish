function paru --wraps paru
    if _pacspin_wanted $argv
        python3 $__pacspin_script paru $argv
    else
        command paru $argv
    end
end
