def sifirEkle(gelen,basamak):
    donen = gelen
    while len(donen) < basamak:
        donen = "0"+donen
    return donen