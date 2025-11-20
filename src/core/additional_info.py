# time calculator
# user action success probability.


import random

def roll_check(stat_value, difficulty):
    roll = random.randint(1, 20)
    total = roll + stat_value
    return {"roll": roll, "total": total, "success": total >= difficulty}
