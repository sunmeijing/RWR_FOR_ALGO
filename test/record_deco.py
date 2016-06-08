import time
from algo import random_walk, distance
from spider import wikispider_ambiguity


def clean_record(fn):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            with open(fn, "w") as f:
                return func(*args, **kwargs)
        return wrapper
    return real_decorator


def record_time(fn):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            with open(fn, "a") as f:
                begin_time = time.time()
                T = func(*args, **kwargs)
                end_time = time.time()
                f.write(",time,"+str(begin_time)+","+str(end_time))
                return T
        return wrapper
    return real_decorator


def record_use_parameter(fn, width=wikispider_ambiguity.ENTITY_WIDTH, depth=wikispider_ambiguity.DEPTH, prob=random_walk.PROB, kl_l=distance.KL_L):
    # {time:[],data:[],description:[]}
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            with open(fn, "a") as f:
                f.write("width"+","+str(width)+",depth"+","+str(depth)+",prob" + "," + str(prob) + ",kl_l" + "," + str(kl_l))
                return func(width=width, depth=depth, prob=prob, kl_l=kl_l, *args, **kwargs)
        return wrapper
    return real_decorator


def record_plug_algo(fn, choice=None):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            with open(fn, "a") as f:
                f.write(",choice,"+choice+",")
                return func(choice=choice, *args, **kwargs)
        return wrapper

    return real_decorator


def record_judge_result(fn):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            with open(fn, "a") as f:
                accuracy, valid_tuple = func(*args, **kwargs)

                f.write("\r\naccuracy:"+str(accuracy)+"\r\n")
                for t in valid_tuple:
                    f.write(t[0]+","+t[1]+"\r\n")
                return accuracy, valid_tuple
        return wrapper
    return real_decorator