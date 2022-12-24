_lnman_complete_sites(){
  COMPREPLY=( $(compgen -W "$(lnman list --as-list)" -- "$cur") )
}

_lnman_complete_sites_slash(){
  COMPREPLY=( $(compgen -W "$(lnman list --as-list)" -S "/" -- "$cur") )
  if declare -F _init_completion >/dev/null 2>&1; then
    [[ $COMPREPLY == */ ]] && compopt -o nospace # not work on mac
  fi
}

_lnman_complete_tree(){
  if [[ "$cur" == */* ]]; then
    local realcur=${cur##*/}
    local prefix=${cur%/*}
    COMPREPLY=( $(compgen -W "$(lnman list "${prefix}" --as-list)" -P "${prefix}/" -- "$realcur") )
  else
    _lnman_complete_sites_slash
  fi
}


_lnman(){
  local cur prev words cword split
  if declare -F _init_completion >/dev/null 2>&1; then
    _init_completion -n / || return
  else
    COMPREPLY=()
    _get_comp_words_by_ref -n / cur prev words cword || return
  fi

  case $cword in
    1)
      COMPREPLY=( $(compgen -W 'file init deinit list sites show lsdir create install remove register unregister version completion' -- "$cur") )
      ;;
    *)
      case ${words[1]} in

        init)
          if [[ ${cword} == 3 ]]; then
            _filedir
          fi
          ;;

        deinit)
          _lnman_complete_tree
          ;;

        list)
          _lnman_complete_sites
          ;;

        show)
          _lnman_complete_tree
          ;;

        lsdir)
          _lnman_complete_sites
          ;;

        create)
          _filedir
          ;;

        install)
          if [[ ${cword} == 2 ]]; then
            _lnman_complete_sites_slash
          else
            _filedir
          fi
          ;;

        remove)
          _lnman_complete_tree
          ;;

        register)
          if [[ "$cur" == */* ]]; then
            local realcur=${cur##*/}
            local prefix=${cur%/*}
            COMPREPLY=( $(compgen -W "$(lnman lsdir "${prefix}" --as-list)" -P "${prefix}/" -- "$realcur") )
          else
            _lnman_complete_sites_slash
          fi
          ;;

        unregister)
          _lnman_complete_tree
          ;;

        esac
      ;;
  esac
}

complete -F _lnman lnman
