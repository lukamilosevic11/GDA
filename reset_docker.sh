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

API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml down
docker rmi gda:1.0
docker build -t gda:1.0 . --no-cache
API_KEY="$(uuidgen)" docker-compose -f gda-compose.yml up
