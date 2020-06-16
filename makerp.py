def makecnt(rp):
    rp = str(rp)
    if len(rp)<=3:
        return int(rp)
    else:
        rem = rp[:-3]
        hun = rp[-3:]
        ls = list()
        if len(rem)%2==0:
            for i in range(0, len(rem), 2):
                ls.append(rem[i:i+2])
        else:
            ls.append(rem[0])
            for i in range(1, len(rem), 2):
                ls.append(rem[i:i+2])
        return ','.join(ls)+','+hun