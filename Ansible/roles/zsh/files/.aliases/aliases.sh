#!/bin/sh

alias dip='python3 ~/.aliases/docker_ip.py'
alias dps='docker ps'
alias dpsa='docker ps -a'

deti() {
  docker exec -ti "$1" sh
}