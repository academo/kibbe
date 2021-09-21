#compdef kibbe

_kibbe_completion() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    (( ! $+commands[kibbe] )) && return 1

    response=("${(@f)$(env COMP_WORDS="${words[*]}" COMP_CWORD=$((CURRENT-1)) _KIBBE_COMPLETE=zsh_complete kibbe)}")

    for type key descr in ${response}; do
        if [[ "$type" == "plain" ]]; then
            if [[ "$descr" == "_" ]]; then
                completions+=("$key")
            else
                completions_with_descriptions+=("$key":"$descr")
            fi
        elif [[ "$type" == "dir" ]]; then
            _path_files -/
        elif [[ "$type" == "file" ]]; then
            _path_files -f
        fi
    done

    if [ -n "$completions_with_descriptions" ]; then
        _describe -V unsorted completions_with_descriptions -U
    fi

    if [ -n "$completions" ]; then
        compadd -U -V unsorted -a completions
    fi
}

compdef _kibbe_completion kibbe;
