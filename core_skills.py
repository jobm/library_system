import random
rand_list = random.shuffle(list(range(1, 21)))

ist_comprehension_below_10 = [num for num in rand_list if num < 10]

list_comprehension_below_10 = list(filter(lambda n: n < 10, rand_list))
