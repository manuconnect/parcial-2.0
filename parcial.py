#Ejercicio 1
def elementos_repetidos (lista):
    return len(lista) != len(set(lista))

lista1 = [1, 2, 3]
if elementos_repetidos(lista1):
    print("Hay elementos repetidos")
else:
    print("No hay elementos repetidos")

#Ejercicio 2
def cadena ():
    lista = ["a", "no", "numero", "hola"]
    lista2 = []
    

    for i in lista:
       if len(i) >= 2:
        lista2.append(i)
       else:
            print("Este no cumple")
    return lista2
print(cadena())

#Ejercicio 3
def elemento():
    v = [1,7,2]
    w = [1,6,7]

    lista2 = []

    for i in v:
       if i not in w:
          lista2.append(i)
    for i in w:
       if i not in v:
          lista2.append(i)
    return lista2

print("El elemento que no se repite es",elemento())
    

    



#Ejercicio 4
def promedio():
    arreglo = [1,2,3,4,5]
    promedio = sum(arreglo)/len(arreglo)
    return promedio
print("El promedio es",promedio())

#Ejercicio 5

def calmediana (arreglo):
    arreglo_ordenado = sorted(arreglo)
    n = len(arreglo)
    mitad = n//2
    if n % 2 == 0:
        mediana =(arreglo_ordenado[mitad-1] + arreglo_ordenado [mitad])/2
    else:
        mediana = arreglo_ordenado[mitad]
    return mediana

lista = [1,4,5,7,6]
mediana1 = calmediana(lista)
print("La mediana es",mediana1)