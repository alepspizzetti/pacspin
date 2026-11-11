function sudo --wraps sudo
    if contains -- "$argv[1]" pacman paru; and _pacspin_wanted $argv[2..-1]
        command sudo python3 $__pacspin_script $argv
    else
        command sudo $argv
    end
end
