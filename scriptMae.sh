#!/run/current-system/sw/bin/bash
if [ "$(docker inspect -f '{{.State.Running}}' xenodochial_ritchie)" = "false" ]; then
    docker start xenodochial_ritchie
fi
sleep 4
# Activate the Nix shell environment and run the script inside it
nix-shell /home/joao/.env  --run "bash ~/Downloads/testepy/script.sh"
sleep 4
#docker stop xenodochial_ritchie
