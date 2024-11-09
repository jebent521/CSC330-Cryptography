class Racer:
    def __init__(self, f, s) -> None:
        self.f = f
        self.state = s
        self.lastValue = None
    
    def step(self):
        self.lastValue = self.state
        self.state = self.f(self.state)
        return self

def floyd(f, s):
    '''Floyd's cycle detection algorithm'''
    i = 0
    tortoise = Racer(f, s)
    hare = Racer(f, s)
    # print('i\tT\tH')
    # print(i, tortoise.state, hare.state, sep='\t')
    while tortoise.state != hare.state or i == 0:
        i += 1
        tortoise.step()     # move tortoise 1 step
        hare.step().step()  # move hare 2 steps
        # print(i, tortoise.state, hare.state, sep='\t')
    j = 0
    secondTortoise = Racer(f, s)    # start second tortoise
    # print('\nj\tT\tH')
    # print(j, tortoise.state, secondTortoise.state, sep='\t')
    while tortoise.state != secondTortoise.state:
        j += 1
        tortoise.step()     # each moves one step until they collide
        secondTortoise.step()
        # print(j, tortoise.state, secondTortoise.state, sep='\t')
    
    return tortoise.lastValue, secondTortoise.lastValue, tortoise.state, j, i


collission = floyd(lambda n: int(str(n * 53)[0:2]), 81)
print('Collision found!')
print(f'f({collission[0]}) = f({collission[1]}) = {collission[2]}');
print('Tail length:', collission[3])
print('Cycle length:', collission[4])
