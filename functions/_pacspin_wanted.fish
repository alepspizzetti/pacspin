function _pacspin_wanted
    isatty stdout; or return 1
    test -r "$__pacspin_script"; or return 1
    command -q python3; or return 1
    string match -qr -- '^-[SRU]' $argv[1]
end
