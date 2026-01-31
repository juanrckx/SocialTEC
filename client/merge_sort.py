"""
Implementación del algoritmo Merge Sort para ordenar listas de amigos.
Cumple con el requisito del proyecto para ordenar la lista de amigos.
"""


def merge_sort(arr, key=None, reverse=False):
    """
    Implementación recursiva de Merge Sort.

    Args:
        arr: Lista a ordenar
        key: Función para extraer la clave de ordenamiento (opcional)
        reverse: Si es True, ordena en orden descendente

    Returns:
        list: Lista ordenada
    """
    if len(arr) <= 1:
        return arr

    # Dividir la lista en dos mitades
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Ordenar recursivamente
    left_sorted = merge_sort(left_half, key, reverse)
    right_sorted = merge_sort(right_half, key, reverse)

    # Combinar las mitades ordenadas
    return merge(left_sorted, right_sorted, key, reverse)


def merge(left, right, key=None, reverse=False):
    """
    Combina dos listas ordenadas en una sola lista ordenada.

    Args:
        left: Lista izquierda ordenada
        right: Lista derecha ordenada
        key: Función para extraer la clave de ordenamiento (opcional)
        reverse: Si es True, ordena en orden descendente

    Returns:
        list: Lista combinada y ordenada
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key(left[i]) if key else left[i]
        right_val = key(right[j]) if key else right[j]

        if reverse:
            # Orden descendente
            if left_val >= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            # Orden ascendente (por defecto)
            if left_val <= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    # Agregar los elementos restantes
    result.extend(left[i:])
    result.extend(right[j:])

    return result


def sort_friends_by_name(friends_list, reverse=False):
    """
    Ordena una lista de amigos por nombre usando Merge Sort.

    Args:
        friends_list: Lista de diccionarios con información de amigos
        reverse: Si es True, ordena en orden Z-A

    Returns:
        list: Lista ordenada por nombre
    """
    if not friends_list:
        return []

    # Ordenar por el campo 'name' (ignorando mayúsculas/minúsculas)
    return merge_sort(friends_list, key=lambda x: x.get('name', '').lower(), reverse=reverse)


def sort_friends_by_username(friends_list, reverse=False):
    """
    Ordena una lista de amigos por nombre de usuario usando Merge Sort.

    Args:
        friends_list: Lista de diccionarios con información de amigos
        reverse: Si es True, ordena en orden descendente

    Returns:
        list: Lista ordenada por nombre de usuario
    """
    if not friends_list:
        return []

    return merge_sort(friends_list, key=lambda x: x.get('username', '').lower(), reverse=reverse)


def sort_friends_by_friend_count(friends_list, reverse=True):
    """
    Ordena una lista de amigos por número de amigos (popularidad).

    Args:
        friends_list: Lista de diccionarios con información de amigos
        reverse: Si es True, ordena de mayor a menor (por defecto)

    Returns:
        list: Lista ordenada por número de amigos
    """
    if not friends_list:
        return []

    return merge_sort(friends_list, key=lambda x: len(x.get('friends', [])), reverse=reverse)


def sort_strings(strings_list, reverse=False):
    """
    Ordena una lista de strings usando Merge Sort.

    Args:
        strings_list: Lista de strings
        reverse: Si es True, ordena en orden Z-A

    Returns:
        list: Lista ordenada alfabéticamente
    """
    return merge_sort(strings_list, reverse=reverse)


# Función de demostración para mostrar cómo funciona el algoritmo
def demonstrate_merge_sort():
    """Demuestra el funcionamiento del Merge Sort con ejemplos"""

    # Ejemplo 1: Ordenar números
    numbers = [38, 27, 43, 3, 9, 82, 10]
    sorted_numbers = merge_sort(numbers)
    print(f"Números originales: {numbers}")
    print(f"Números ordenados: {sorted_numbers}")
    print()

    # Ejemplo 2: Ordenar strings
    names = ["María", "Juan", "Ana", "Carlos", "Beatriz"]
    sorted_names = sort_strings(names)
    print(f"Nombres originales: {names}")
    print(f"Nombres ordenados: {sorted_names}")
    print()

    # Ejemplo 3: Ordenar amigos por nombre
    friends = [
        {"name": "Carlos Ruiz", "username": "carlos_ruiz", "friends": 15},
        {"name": "Ana López", "username": "ana_lopez", "friends": 23},
        {"name": "María García", "username": "maria_garcia", "friends": 18},
        {"name": "Juan Pérez", "username": "juan_perez", "friends": 12},
    ]

    sorted_by_name = sort_friends_by_name(friends)
    sorted_by_friends = sort_friends_by_friend_count(friends)

    print("Amigos ordenados por nombre:")
    for friend in sorted_by_name:
        print(f"  - {friend['name']} (@{friend['username']})")

    print("\nAmigos ordenados por popularidad (más amigos primero):")
    for friend in sorted_by_friends:
        print(f"  - {friend['name']}: {friend['friends']} amigos")

    return sorted_numbers, sorted_names, sorted_by_name, sorted_by_friends


if __name__ == "__main__":
    # Ejecutar demostración si se ejecuta directamente
    demonstrate_merge_sort()