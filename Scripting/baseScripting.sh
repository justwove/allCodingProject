#/bin/bash

function addition() {
    echo "$1 + $2 = $(($1+$2))" 
}

addition 1 2

function reste() {
    if [[ $2 != 0 ]]; then
        echo "$1 % $2 = $(($1%$2))" 
    fi
}

reste 5 10

function lasomme() {
    listeNombre=()
}