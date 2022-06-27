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
    def update(self, subject):
        # print(subject.step)
        pass


class Subject:
    def __init__(self, lock):
        self.step = 0
        self._observers = []
        self.lock = lock

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


# if __name__ == "__main__":
#     # The client code.
#
#     subject = ConcreteSubject()
#
#     observer_a = ConcreteObserverA()
#     subject.attach(observer_a)
#
#     observer_b = ConcreteObserverB()
#     subject.attach(observer_b)
#
#     subject.some_business_logic()
#     subject.some_business_logic()
#
#     subject.detach(observer_a)
#
#     subject.some_business_logic()
