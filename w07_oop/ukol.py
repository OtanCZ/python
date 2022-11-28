#  Upravte třídu Point tak, aby podporovala následující operace,
# kde p, q a r jsou objekty typu Point a n je číslo
# p =  q + r
# p += q
# p = q - r
# p -= q
# p =q * n
# p *= n
# p = q / n
# p /= n
# p = q // n
# p //= n

# Upravte třídu Image (v souboru Image.py) tak, aby poskytovala metodu resize
# (width, height). Je-li nová šířka menší, než aktuální hodnota, je nutné
# všechny barvy mimo nové hranice vymazat. Máli jeden z parametrů hodnotu None,
# použije se stávající výška, resp. šířka. Na konci nezapomeňte vygenerovat
# množinu self.__colors. Metoda vrátí logickou hodnotu signalizující, zda změny
# byly, či nebyly provedeny.