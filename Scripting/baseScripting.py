#/bin/python3.9

def addition(n: int, p:int):
    return n + p

def reste(n: int, p:int):
    if p == 0: print('Opération non possible'), exit(1)
    return n % p 
    
def lasomme():
    listeNombres = [int(input('Indiqué un chiffre: ')) for _ in range(20)]
    return sum(listeNombres)

def lascdsomme():
    somme = 0
    listeNombres = []
    while somme < 1000:
        userInput = int(input('Indiqué un chiffre: '))                 #Somme divisé par le nombre de valeur
        somme += userInput
        listeNombres.append(int(userInput))
    return listeNombres, somme // len(listeNombres)

def sameInterval(firstList: list, secondList: list):
    for i in range(int(firstList[0]), int(firstList[1])):
        for j in range(int(secondList[0]), int(secondList[1])):
            if i == j: return True

def scndSameInterval(firstList: list, secondList: list):
    if int(firstList[1]) > int(secondList[0]) and int(firstList[0]) < int(secondList[1]): return True

def find21(firstList: list, secondList: list):
    firstList = sorted(firstList, reverse=True)
    secondList = sorted(secondList, reverse=True)
    for firstIndex in range(len(firstList)):
        for secondIndex in range(len(secondList)):
            if firstList[firstIndex] > secondList[secondIndex] and firstList[firstIndex] < 21: 
                secondList = sorted(secondList)
                for i in secondList:
                    if (firstList[firstIndex] + i) == 21:
                        print(firstList[firstIndex], i)
            elif secondList[secondIndex] > firstList[firstIndex] and secondList[secondIndex] < 21: 
                firstList = sorted(firstList)
                for i in firstList:
                    if (secondList[secondIndex] + i) == 21:
                        print(secondList[secondIndex], i)


# firstNumber = int(input('Indiqué un premier chiffre: '))
# secondNumber = int(input('Indiqué un second chiffre: '))

# print(f'{firstNumber} + {secondNumber} = {addition(firstNumber, secondNumber)}')
# print(f'{firstNumber} % {secondNumber} = {reste(firstNumber, secondNumber)}')
# print('Veuillez donnez 20 nombres qui seront additionner.')
# print(f'La sommes des 20 nombres est : {lasomme()}')

# print("Veuillez donnez plusieurs nombres jusqu'a ce que la somme des nombres soit 1000.")
# nbrNombres, moyenne = lascdsomme()
# print(f'Nous sommes arrivez à 1000 avec {len(nbrNombres)} nombres avec une moyenne de {moyenne}')

# print('Veuillez donnez 2 intervale différentes. Si les les intervale ont le même nombres on retourne Vrai')
# firstInterval = input('Entrer la première intervale séparé par un espace: ').split()
# secondInterval = input('Entrer la seconde intervale séparé par un espace: ').split()
# print(f'Les intervales {firstInterval} {secondInterval} ont un ou plusieurs nombres identique' 
#     if scndSameInterval(firstInterval, secondInterval) is True 
#     else f"Les intervales {firstInterval} {secondInterval} n'ont pas de nombre identique")
find21([10,7,4,12,8], [15,9,4,12,2])