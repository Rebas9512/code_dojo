class Car:
    def __init__(self, number, next_car=None):
        self.val = number
        self.next = next_car


car = Car(7, Car(4, Car(2)))
while car is not None:
    print(car.val)
    car = car.next
