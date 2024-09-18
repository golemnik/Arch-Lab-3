if __name__ == "__main__":
    val0 = 1
    val1 = 2
    s = 0
    while val1 < 4_000_000:
        if 0 == val1 % 2:
            s += val1
        val = val0 + val1
        print("%d %d" % (val, s))
        val0 = val1
        val1 = val
    print("sum= %d" % s)
