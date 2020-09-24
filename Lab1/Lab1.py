T = int(input())
for t in range(0, T):
    s = input.split(' ')
    n = int(s[0])
    m = int(s[1])
    ans = 0
    tmp = 1
    x = n // m

    if n == x * m:
        print(x)
        continue

    while tmp * 2 <= x:
        tmp = tmp * 2
    while n // m >= 2:
        x = n // m
        while tmp > x:
            tmp = tmp // 2

        ans = ans + tmp
        n = n - tmp * m

    if n // m == 1:
        if n % 2 == 0:
            ans = ans + 2
        else:
            ans = ans + 3
    elif n > 0:
        ans = ans + 1

    print(ans)
