## 1 - Utiliser des constantes 
Je préconiserais d'utiliser à la place de chaînes de caractère répétés partout dans le code, des constantes.

Exemple:
`if self.armor_type == 'chobham':`

On peut définir à la place une constante:
`CHOBHAM = 'chobham'`

Cela à plusieurs avantages:
- Eviter les fautes de frappes qui peuvent casser le code.
    - l'IDE pointera que la variable n'existe pas
    - le linter mettra également cela en évidence dans le pre-commit avant le lancement des tests
    - l'auto-complétion permettra d'aller plus vite et éviter les erreurs
- Ça sera nettement plus facile de renommer la variable si besoin !


## 2 - Utiliser des dataclass/enums
Par rapport à ma review précédente, dans ce cas précis je préconiserais même de créer une enum/dataclass

- Cela permettra de définir un typage relativement précis sur ce qu'on attend (exemple: `armor_type: ArmorType`)
- Ça évite de devoir faire des validations pour vérifier que le type d'armure existe, on peut juste vérifier le type d'instance (`isinstance(armor_type, ArmorType)`)
- En terme de lisibilité / documentation, on peut rapidement voir quels sont les types d'armures disponibles
- Ça permet de résoudre #1, c'est à dire de définir des constantes réutilisables dans le code



## 3. Amélioration de la fonction `def vulnerable`

Sur ces lignes de code:
```
if self.armor_type == 'chobham':
    real_armor += 100
elif self.armor_type == 'composite':
    real_armor += 50
elif self.armor_type == 'ceramic':
    real_armor += 50
```

Plutôt que de définir les valeurs dans la fonction et de créer autant de conditions, on peut créer des constantes dans un dictionnaire ou dans la dataclass facilement accessibles.

Exemple:

```
ARMOR_TYPE_VALUES = {
    CHOBHAM: 100,
    COMPOSITE: 50,
    CERAMIC: 50
}

real_armor = self.armor + ARMOR_TYPE_VALUES[self.armor_type]
```

ou bien

```
class ArmorType(IntEnum):
    CHOBHAM = 100
    COMPOSITE = 50
    CERAMIC = 50

armor_type = ArmorType.CHOBHAM
real_armor = self.armor + armor_type.value
```

Cela permet de gagner en lisibilité, d'éviter les erreurs et de pouvoir être facilement ré-utilisé ailleurs si besoin. 


## 4. Retourner directement l'évaluation de la condition 

Dans ce cas précis:
```
if real_armor <= tank.penetration: return True
return False
```

On peut directement retourner:

`return real_armor <= tank.penetration`


## 5. Utilisation de variable potentiellement non définie

Attention à la ligne `tmp = self.name.lower()` dans `__repr__`, car `self.name` n'est pas défini dans le `__init__`, ce qui peut conduire à une erreur si on n'appelle pas la fonction `set_name` au préalable.


## 6. Utiliser des logs plutôt que des print

`print` pour debug local ponctuel, `logging` pour du code destiné à tourner / être observé.


## 7. Éviter d'exécuter du code en dehors des classes et des fonctions

Une sécurité qui ne fait pas de mal si jamais certaines définitions sont utilisées ailleurs, serait de faire ceci :

```
def main():
    m1_1 = Tank(600, 670, 'chobham')
    m1_2 = Tank(620, 670, 'chobham')
    ...

if __name__ == "__main__":
    main()
```

Cela évite les mauvaises surprises si jamais un autre script veut ré-utiliser la classe Tank par exemple :

`from tank import Tank`

Notre nouvelle condition `__name__ == "__main__"`  permettra d'éviter d'exécuter le code écrit dans `main` !


## 8. Plusieurs erreurs ici :

```
for i in range(5):
    tanks.append(Tank(400, 400, 'steel'))
index = 0
for tank in tanks:
    tank.set_name('Tank' + str(index) + "_Small")
    index += 1
test = []
index = 0
while index < len(tanks):
    test.append(tanks[i].vulnerable(m1_1))
```
1. Une seule itération suffit pour exécuter le code, ici on fait 3 itérations.
2. `steel` n'existe pas, et l'exécution du code trigger une exception
3. On peut utiliser la fonction python `enumerate` pour éviter de s'emcombrer à incrémenter manuellement une variable `index`
4. Nous avons une boucle infinie dans le `while`, car index n'est jamais incrémenté. La boucle `while` n'est d'ailleurs pas nécessaire car on pourrait directement itérer sur la liste de `tanks`
5. Dans le `while`, il y a une erreur car on utilise `i` au lieu de `index`


## 9. La variable `self.tank = "Tank"` n'est pas utilisée


## 10. Essayer d'utiliser des exceptions plus spécifique que `Exception` (e.g: `ValueError`, `TypeError`, `AssertionError`...)


## 11. Éviter de définir les variables mutables comme valeur par défaut (e.g: `def test_tank_safe(shooter, test_vehicles=[]):`)

C'est seulement possible si on est sûr de ne jamais manipuler la variable `test_vehicles` (readonly), mais ça reste dangereux car ça peut créer des gros problèmes parfois difficiles à debug !

Je préconiserais à la place de mettre une variable non mutable (comme `None`), et de faire une validation/clean en début de fonction (e.g: `test_vehicles = test_vehicles or []`)


## 12. Incohérence sémantique sur `at_least_one_safe`

La liste `test` contient une liste de booléen où le véhicule est considéré comme vulnérable si `True`, mais `at_least_one_safe` est définie comme `True` si `t` est vrai.


## 13. La fonction `swap_armor` n'a pas besoin de retourner d'objets

Ici on chance directement l'instance passé en argument, et on ne retourne pas de clone. Il n'y a donc pas de necessité de retourner l'objet pour écraser l'ancienne instance.


## 14. Utiliser des sets de données variés dans les tests

```
for tank in tanks:
    tank.set_name('Tank' + str(index) + "_Small")
    index += 1
test = []
index = 0
while index < len(tanks):
    test.append(tanks[i].vulnerable(m1_1))
...
```

On évalue plusieurs fois le même type de tank et donc les mêmes conditions. Peut-être créer un dataset avec plusieurs cas différents ?

## 15. Attention aux variables écrasées

```
    def __repr__(self):
        tmp = self.name.lower()
        tmp = self.name.replace(' ', '-')
        return tmp
```

Dans ce cas là, `tmp` est écrasé immédiatement par `tmp = self.name.replace(' ', '-')`

Aussi, `__repr__` devrait renvoyer une réprésentation comme `Tank(name='...', armor=...)`, pour pouvoir facilement visualiser les attributs de l'objet
Il faudrait plutôt utiliser `__str__` dans ce cas précis !