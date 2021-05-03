def findProduct(en):
    import pandas as pd
    df = pd.read_excel('P&G.xlsx')
    res = pd.DataFrame()
    with_brand = pd.DataFrame()
    for i in en:
        if i[1] == 'CONSUMER_GOOD' or i[1]=='OTHER':
            if len(i[0].split(" "))>1:
                item = i[0].split(" ")[-1].lower()
                brand = i[0].split(" ")[0]
                res = pd.concat([res, pd.DataFrame(df[df["Item"].str.lower() == item])], axis=0)
                with_brand = pd.concat([with_brand, res[res['Company']== brand]], axis=0)
            else:
                res = pd.concat([res, pd.DataFrame(df[df["Item"].str.lower() == i[0]])], axis=0)
    for i in en:
        if i[1] == 'ORGANIZATION':
                with_brand = pd.concat([with_brand, res[res['Company']== i[0]]], axis=0)
    return res, with_brand
