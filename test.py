taomlar = {'osh':20000,
         "sho'rva":15000,
         'qotirma':25000,
         'somsa':6000,
         'non':3000,
         'choy':2000,
         'salat':5000
         }
buyurtmalar = []
n = 1

while True:
    taom = input(f"{n}-taomga nima buyurtma berasiz>>>").lower()
    user = buyurtmalar.append(taom)

    if taom == 'somsa':
        nechta = int(input("Nechta somsa yozaylik?>>>"))
        user = buyurtmalar.append(taom)
        s_narx = taomlar['somsa']
        narx = s_narx*6000
        n+=1
        continue
    elif taom == 'osh' or taom == 'salat' or taom == 'qotirma' or taom == 'non' or taom == 'choy' or taom == "sho'rva":
        n+=1
        continue

    elif taom == "exit":
        break

    print(taom)