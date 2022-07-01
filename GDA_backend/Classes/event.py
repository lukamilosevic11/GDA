#  GDA Copyright (c) 2022.
#  University of Belgrade, Faculty of Mathematics
#  Luka Milosevic
#  lukamilosevic11@gmail.com
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.


class Observer:
    def __init__(self, frontendTracker):
        self.frontendTracker = frontendTracker

    def update(self, subject):
        self.frontendTracker.progress = int((subject.step/subject.total)*100)


class Subject:
    def __init__(self, lock):
        self.step = 0
        self._observers = []
        self.lock = lock
        self.total = 1

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def increase_step(self):
        with self.lock:
            self.step += 1
            self.notify()

    def set_total(self, total):
        self.total = total
