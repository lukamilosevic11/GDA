#
# GDA Copyright (c) 2022.
# University of Belgrade, Faculty of Mathematics
# Luka Milosevic
# lukamilosevic11@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#

print_usage() {
  if [ $1 -eq 1 ]
  then
  cat<<EOF

  Wrong argument, see usage below!
EOF
  fi

  cat <<EOF

  Usage: $0 <options> [output mode]
    -h|-help            Shows this help text.
    -s|-start           Starts existing containers for a service.
                        Starts the stopped containers, can't create new ones.
                        Can be run only in detach mode. There is no output.
    -e|-exit            Exits/Stops running containers without removing them.
                        They can be started again with start command.
    -u|-up              Builds, (re)creates, and starts containers.
                        Run in detached mode or in the background. There is no output.
    -u|-up -o|-output   Shows output of execution for Typesense and GDA.
    -d|-down            Stops containers and by default, the only things removed are:
                          - Containers for services defined in the gda-compose file
                          - Networks defined in the networks section of the gda-compose file
                          - The default network, if one is used
                        Networks and volumes defined as external are never removed.
    -d|-down -r|-reset Stops containers and removes containers, networks, volumes, and images created by up command.
EOF
}

# Transform long options to short ones
case "$1" in
  -help)  set -- "$@" '-h'   ;;
  -start) set -- "$@" '-s'   ;;
  -exit)  set -- "$@" '-e'   ;;
  -up)    set -- "$@" '-u'   ;;
  -down)  set -- "$@" '-d'   ;;
  *)      set -- "$@" "$1" ;;
esac

OUTPUT_MODE=0;

if [ "$2" = "-o" ] || [ "$2" = "-output" ]
then
  OUTPUT_MODE=1;
fi

RESET_MODE=0;

if [ "$2" = "-r" ] || [ "$2" = "-reset" ]
then
  RESET_MODE=1;
fi

# Parse short options
getopts ":hseud" opt
  case "$opt" in
    h) print_usage 0; exit 0 ;;
    s) API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml -p gene-disease-annotation start ;;
    e) API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml -p gene-disease-annotation stop ;;
    u)
      if [ $OUTPUT_MODE -eq 1 ]
      then
        API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml -p gene-disease-annotation up
      else
        API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml -p gene-disease-annotation up -d
      fi ;;
    d)
      if [ $RESET_MODE -eq 1 ]
      then
        API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml -p gene-disease-annotation down --rmi all -v --remove-orphans
      else
        API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml -p gene-disease-annotation down
      fi ;;
    *) print_usage 1; exit 1 ;;
  esac
