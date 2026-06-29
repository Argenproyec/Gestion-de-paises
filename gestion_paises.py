"""
=============================================================
  TPI - Gestión de Datos de Países
  Universidad Tecnológica Nacional (UTN)
  Tecnicatura Universitaria en Programación a Distancia (TUPaD)
  Materia: Programación 1
  Alumno: Troncoso Leonardo Gabriel
=============================================================
Descripción:
  Sistema de gestión de información sobre países.
  Permite agregar, actualizar, buscar, filtrar, ordenar
  y obtener estadísticas de países leídos desde un CSV.

Estructuras usadas: listas, diccionarios, funciones,
condicionales, bucles, manejo de archivos CSV y errores.
=============================================================
"""

import csv
import os

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
ARCHIVO_CSV = "paises.csv"
CABECERA_CSV = ["nombre", "poblacion", "superficie", "continente"]


# ═══════════════════════════════════════════════════════════
# MÓDULO 1 – LECTURA / ESCRITURA DE ARCHIVOS CSV
# ═══════════════════════════════════════════════════════════

def cargar_paises(ruta):
    # Lee el archivo CSV y devuelve una lista de diccionarios.
    # Cada diccionario representa un país con sus campos.
    # Valida el formato de cada fila antes de agregarla.
    # Retorna: lista de diccionarios (puede estar vacía si hay error).
    
    paises = []

    if not os.path.exists(ruta):
        print(f"[AVISO] No se encontró '{ruta}'. Se iniciará con lista vacía.")
        return paises

    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Verificar que el CSV tiene las columnas esperadas
            if not all(col in lector.fieldnames for col in CABECERA_CSV):
                print("[ERROR] El CSV no tiene el formato esperado.")
                print(f"  Columnas requeridas: {CABECERA_CSV}")
                return paises

            for numero_fila, fila in enumerate(lector, start=2):
                pais = _validar_fila_csv(fila, numero_fila)
                if pais is not None:
                    paises.append(pais)

    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo: {e}")

    return paises


def _validar_fila_csv(fila, numero_fila):
    """
    Valida una fila del CSV y devuelve un diccionario válido o None.
    Comprueba que no haya campos vacíos y que los números sean correctos.
    """
    # Verificar campos vacíos
    for campo in CABECERA_CSV:
        if not fila.get(campo, "").strip():
            print(f"[AVISO] Fila {numero_fila}: campo '{campo}' vacío. Se omite.")
            return None

    # Convertir y validar tipos numéricos
    try:
        poblacion = int(fila["poblacion"].strip())
        superficie = int(fila["superficie"].strip())
    except ValueError:
        print(f"[AVISO] Fila {numero_fila}: población/superficie no son enteros. Se omite.")
        return None

    if poblacion <= 0 or superficie <= 0:
        print(f"[AVISO] Fila {numero_fila}: población y superficie deben ser positivos. Se omite.")
        return None

    return {
        "nombre": fila["nombre"].strip(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": fila["continente"].strip()
    }


def guardar_paises(paises, ruta):
    """
    Escribe la lista de países en el archivo CSV.
    Sobreescribe el contenido anterior.
    """
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CABECERA_CSV)
            escritor.writeheader()
            escritor.writerows(paises)
        print("[OK] Datos guardados correctamente en el archivo CSV.")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo: {e}")


# ═══════════════════════════════════════════════════════════
# MÓDULO 2 – AGREGAR Y ACTUALIZAR PAÍSES
# ═══════════════════════════════════════════════════════════

def agregar_pais(paises):
    """
    Solicita los datos de un nuevo país al usuario y lo agrega.
    No permite campos vacíos ni población/superficie no positivos.
    Evita duplicados por nombre (insensible a mayúsculas).
    """
    print("\n─── AGREGAR PAÍS ───")

    nombre = _pedir_texto("Nombre del país")
    if nombre is None:
        return

    # Verificar duplicado
    if _buscar_indice(paises, nombre) != -1:
        print(f"[AVISO] Ya existe un país con el nombre '{nombre}'.")
        return

    continente = _pedir_texto("Continente")
    if continente is None:
        return

    poblacion = _pedir_entero_positivo("Población")
    if poblacion is None:
        return

    superficie = _pedir_entero_positivo("Superficie (km²)")
    if superficie is None:
        return

    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo_pais)
    print(f"[OK] País '{nombre}' agregado exitosamente.")


def actualizar_pais(paises):
    """
    Permite actualizar la población y/o superficie de un país existente.
    Busca el país por nombre (coincidencia exacta, sin importar mayúsculas).
    """
    print("\n─── ACTUALIZAR PAÍS ───")

    if not paises:
        print("[AVISO] No hay países cargados.")
        return

    nombre = _pedir_texto("Nombre del país a actualizar")
    if nombre is None:
        return

    indice = _buscar_indice(paises, nombre)
    if indice == -1:
        print(f"[ERROR] No se encontró ningún país con el nombre '{nombre}'.")
        return

    pais = paises[indice]
    print(f"\nPaís encontrado: {_formato_pais(pais)}")
    print("Ingrese el nuevo valor (o presione Enter para no cambiar).")

    # Actualizar población
    entrada = input("  Nueva población (Enter para omitir): ").strip()
    if entrada:
        nueva_pob = _convertir_entero_positivo(entrada, "Población")
        if nueva_pob is not None:
            paises[indice]["poblacion"] = nueva_pob
            print(f"  Población actualizada: {nueva_pob:,}")

    # Actualizar superficie
    entrada = input("  Nueva superficie en km² (Enter para omitir): ").strip()
    if entrada:
        nueva_sup = _convertir_entero_positivo(entrada, "Superficie")
        if nueva_sup is not None:
            paises[indice]["superficie"] = nueva_sup
            print(f"  Superficie actualizada: {nueva_sup:,} km²")

    print(f"[OK] País '{paises[indice]['nombre']}' actualizado.")


# ═══════════════════════════════════════════════════════════
# MÓDULO 3 – BÚSQUEDA
# ═══════════════════════════════════════════════════════════

def buscar_pais(paises):
    """
    Busca países cuyo nombre contenga el texto ingresado.
    La búsqueda es parcial e insensible a mayúsculas/minúsculas.
    """
    print("\n─── BUSCAR PAÍS ───")

    if not paises:
        print("[AVISO] No hay países cargados.")
        return

    termino = input("Ingrese el nombre o parte del nombre a buscar: ").strip()
    if not termino:
        print("[ERROR] El término de búsqueda no puede estar vacío.")
        return

    # Búsqueda parcial: compara en minúsculas
    resultados = [p for p in paises if termino.lower() in p["nombre"].lower()]

    if not resultados:
        print(f"[INFO] No se encontraron países que coincidan con '{termino}'.")
    else:
        print(f"\nSe encontraron {len(resultados)} resultado(s):")
        _mostrar_lista(resultados)


# ═══════════════════════════════════════════════════════════
# MÓDULO 4 – FILTROS
# ═══════════════════════════════════════════════════════════

def filtrar_paises(paises):
    """
    Menú de filtros: por continente, rango de población o rango de superficie.
    """
    print("\n─── FILTRAR PAÍSES ───")

    if not paises:
        print("[AVISO] No hay países cargados.")
        return

    print("¿Cómo desea filtrar?")
    print("  1. Por continente")
    print("  2. Por rango de población")
    print("  3. Por rango de superficie")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        _filtrar_por_continente(paises)
    elif opcion == "2":
        _filtrar_por_rango(paises, campo="poblacion", unidad="habitantes")
    elif opcion == "3":
        _filtrar_por_rango(paises, campo="superficie", unidad="km²")
    else:
        print("[ERROR] Opción no válida.")


def _filtrar_por_continente(paises):
    """Filtra países que pertenezcan al continente ingresado."""
    # Mostrar continentes disponibles
    continentes = sorted(set(p["continente"] for p in paises))
    print("\nContinentes disponibles:", ", ".join(continentes))

    continente = input("Ingrese el continente: ").strip()
    if not continente:
        print("[ERROR] El continente no puede estar vacío.")
        return

    resultados = [p for p in paises if p["continente"].lower() == continente.lower()]

    if not resultados:
        print(f"[INFO] No se encontraron países en '{continente}'.")
    else:
        print(f"\nPaíses en {continente} ({len(resultados)}):")
        _mostrar_lista(resultados)


def _filtrar_por_rango(paises, campo, unidad):
    """
    Filtra países cuyo valor de 'campo' esté entre un mínimo y un máximo.
    Acepta el mínimo como 0 si no se ingresa ninguno.
    """
    print(f"\nFiltrar por {campo} ({unidad}).")

    minimo = _pedir_entero_positivo_opcional(f"  Mínimo (Enter = 0)")
    if minimo is None:
        minimo = 0

    maximo = _pedir_entero_positivo_opcional(f"  Máximo (Enter = sin límite)")

    # Aplicar filtro
    if maximo is None:
        resultados = [p for p in paises if p[campo] >= minimo]
    else:
        if maximo < minimo:
            print("[ERROR] El máximo no puede ser menor que el mínimo.")
            return
        resultados = [p for p in paises if minimo <= p[campo] <= maximo]

    if not resultados:
        print(f"[INFO] No se encontraron países en el rango especificado.")
    else:
        print(f"\nResultados ({len(resultados)}):")
        _mostrar_lista(resultados)


# ═══════════════════════════════════════════════════════════
# MÓDULO 5 – ORDENAMIENTOS
# ═══════════════════════════════════════════════════════════

def ordenar_paises(paises):
    """
    Ordena la lista de países por nombre, población o superficie.
    Permite elegir orden ascendente o descendente.
    Usa la función sorted() con key; no modifica la lista original.
    """
    print("\n─── ORDENAR PAÍSES ───")

    if not paises:
        print("[AVISO] No hay países cargados.")
        return

    print("Ordenar por:")
    print("  1. Nombre")
    print("  2. Población")
    print("  3. Superficie")
    opcion = input("Opción: ").strip()

    # Determinar el campo de ordenamiento
    if opcion == "1":
        campo = "nombre"
    elif opcion == "2":
        campo = "poblacion"
    elif opcion == "3":
        campo = "superficie"
    else:
        print("[ERROR] Opción no válida.")
        return

    print("Orden:")
    print("  1. Ascendente")
    print("  2. Descendente")
    orden_opcion = input("Opción: ").strip()

    if orden_opcion == "1":
        descendente = False
    elif orden_opcion == "2":
        descendente = True
    else:
        print("[ERROR] Opción no válida.")
        return

    # sorted() devuelve una nueva lista ordenada (no modifica la original)
    ordenados = sorted(paises, key=lambda p: p[campo], reverse=descendente)

    direccion = "descendente" if descendente else "ascendente"
    print(f"\nPaíses ordenados por {campo} ({direccion}):")
    _mostrar_lista(ordenados)


# ═══════════════════════════════════════════════════════════
# MÓDULO 6 – ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════

def mostrar_estadisticas(paises):
    """
    Calcula y muestra estadísticas sobre el conjunto de países:
    - País con mayor y menor población
    - Promedio de población
    - Promedio de superficie
    - Cantidad de países por continente
    """
    print("\n─── ESTADÍSTICAS ───")

    if not paises:
        print("[AVISO] No hay países cargados.")
        return

    total = len(paises)

    # País con mayor y menor población
    pais_max_pob = _encontrar_extremo(paises, "poblacion", maximo=True)
    pais_min_pob = _encontrar_extremo(paises, "poblacion", maximo=False)

    # Promedios
    promedio_pob = _calcular_promedio(paises, "poblacion")
    promedio_sup = _calcular_promedio(paises, "superficie")

    # Cantidad por continente
    conteo_continentes = _contar_por_continente(paises)

    # Mostrar resultados
    print(f"\n  Total de países cargados : {total}")
    print(f"\n  Población:")
    print(f"    Mayor  → {pais_max_pob['nombre']} ({pais_max_pob['poblacion']:,} hab.)")
    print(f"    Menor  → {pais_min_pob['nombre']} ({pais_min_pob['poblacion']:,} hab.)")
    print(f"    Promedio → {promedio_pob:,.0f} hab.")
    print(f"\n  Superficie:")
    print(f"    Promedio → {promedio_sup:,.0f} km²")
    print(f"\n  Países por continente:")
    for continente, cantidad in sorted(conteo_continentes.items()):
        print(f"    {continente:<20} {cantidad} país/es")


def _encontrar_extremo(paises, campo, maximo):
    """
    Recorre la lista y devuelve el diccionario con el valor
    máximo o mínimo para el campo indicado.
    No usa las funciones max()/min() con key para mostrar el recorrido manual.
    """
    extremo = paises[0]
    for pais in paises[1:]:
        if maximo:
            if pais[campo] > extremo[campo]:
                extremo = pais
        else:
            if pais[campo] < extremo[campo]:
                extremo = pais
    return extremo


def _calcular_promedio(paises, campo):
    """
    Suma los valores de un campo numérico y divide por la cantidad.
    Devuelve 0 si la lista está vacía.
    """
    if not paises:
        return 0
    total = 0
    for pais in paises:
        total += pais[campo]
    return total / len(paises)


def _contar_por_continente(paises):
    """
    Construye un diccionario {continente: cantidad_de_paises}.
    Recorre la lista una sola vez.
    """
    conteo = {}
    for pais in paises:
        continente = pais["continente"]
        if continente in conteo:
            conteo[continente] += 1
        else:
            conteo[continente] = 1
    return conteo


# ═══════════════════════════════════════════════════════════
# MÓDULO 7 – MOSTRAR TODOS LOS PAÍSES
# ═══════════════════════════════════════════════════════════

def mostrar_todos(paises):
    """Muestra todos los países cargados en formato de tabla."""
    print("\n─── LISTA COMPLETA DE PAÍSES ───")
    if not paises:
        print("[AVISO] No hay países cargados.")
        return
    print(f"Total: {len(paises)} países\n")
    _mostrar_lista(paises)


# ═══════════════════════════════════════════════════════════
# MÓDULO 8 – FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════

def _mostrar_lista(lista_paises):
    """
    Imprime una lista de países en formato de tabla con encabezado.
    Separa columnas con caracteres de borde para mayor legibilidad.
    """
    ancho_nombre = 35
    ancho_pob = 16
    ancho_sup = 16
    ancho_cont = 12

    separador = (
        "─" * (ancho_nombre + 2) + "┼" +
        "─" * (ancho_pob + 2) + "┼" +
        "─" * (ancho_sup + 2) + "┼" +
        "─" * (ancho_cont + 2)
    )

    encabezado = (
        f" {'Nombre':<{ancho_nombre}} │"
        f" {'Población':>{ancho_pob}} │"
        f" {'Superficie (km²)':>{ancho_sup}} │"
        f" {'Continente':<{ancho_cont}}"
    )

    print(encabezado)
    print(separador)

    for pais in lista_paises:
        nombre = pais["nombre"][:ancho_nombre]
        print(
            f" {nombre:<{ancho_nombre}} │"
            f" {pais['poblacion']:>{ancho_pob},} │"
            f" {pais['superficie']:>{ancho_sup},} │"
            f" {pais['continente']:<{ancho_cont}}"
        )


def _formato_pais(pais):
    """Devuelve una cadena de texto con los datos de un país."""
    return (
        f"{pais['nombre']} | Pob: {pais['poblacion']:,} | "
        f"Sup: {pais['superficie']:,} km² | {pais['continente']}"
    )


def _buscar_indice(paises, nombre):
    """
    Devuelve el índice del país con ese nombre en la lista.
    Comparación insensible a mayúsculas/minúsculas.
    Devuelve -1 si no se encuentra.
    """
    nombre_lower = nombre.lower()
    for i in range(len(paises)):
        if paises[i]["nombre"].lower() == nombre_lower:
            return i
    return -1


def _pedir_texto(mensaje):
    """
    Solicita al usuario una cadena no vacía.
    Devuelve None si el usuario deja el campo vacío.
    """
    valor = input(f"  {mensaje}: ").strip()
    if not valor:
        print(f"[ERROR] El campo '{mensaje}' no puede estar vacío.")
        return None
    return valor


def _pedir_entero_positivo(mensaje):
    """
    Solicita un número entero positivo al usuario.
    Repite hasta obtener un valor válido o que el usuario cancele con 'q'.
    """
    while True:
        entrada = input(f"  {mensaje} (q para cancelar): ").strip()
        if entrada.lower() == "q":
            print("[INFO] Operación cancelada.")
            return None
        resultado = _convertir_entero_positivo(entrada, mensaje)
        if resultado is not None:
            return resultado


def _pedir_entero_positivo_opcional(mensaje):
    """
    Solicita un número entero positivo; acepta Enter como valor vacío (None).
    """
    entrada = input(f"{mensaje}: ").strip()
    if not entrada:
        return None
    return _convertir_entero_positivo(entrada, "Valor")


def _convertir_entero_positivo(texto, etiqueta):
    """
    Convierte texto a entero positivo.
    Muestra un mensaje de error y devuelve None si no es posible.
    """
    try:
        valor = int(texto)
        if valor <= 0:
            print(f"[ERROR] '{etiqueta}' debe ser un número mayor a cero.")
            return None
        return valor
    except ValueError:
        print(f"[ERROR] '{etiqueta}' debe ser un número entero válido.")
        return None


# ═══════════════════════════════════════════════════════════
# MÓDULO 9 – MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def mostrar_menu():
    """Imprime el menú principal de opciones."""
    print("\n" + "═" * 50)
    print("   GESTIÓN DE DATOS DE PAÍSES - MENÚ PRINCIPAL")
    print("═" * 50)
    print("  1. Mostrar todos los países")
    print("  2. Agregar un país")
    print("  3. Actualizar población y superficie de un país")
    print("  4. Buscar país por nombre")
    print("  5. Filtrar países")
    print("  6. Ordenar países")
    print("  7. Mostrar estadísticas")
    print("  8. Guardar cambios en CSV")
    print("  0. Salir")
    print("─" * 50)


def main():
    """
    Punto de entrada del programa.
    Carga los países desde el CSV y presenta el menú en bucle
    hasta que el usuario elija salir.
    """
    print("═" * 50)
    print("   SISTEMA DE GESTIÓN DE PAÍSES")
    print("   TPI - Programación 1 - UTN TUP")
    print("═" * 50)

    # Cargar datos iniciales
    paises = cargar_paises(ARCHIVO_CSV)
    print(f"\n[OK] {len(paises)} países cargados desde '{ARCHIVO_CSV}'.")

    # Mapa de opciones a funciones
    opciones = {
        "1": mostrar_todos,
        "2": agregar_pais,
        "3": actualizar_pais,
        "4": buscar_pais,
        "5": filtrar_paises,
        "6": ordenar_paises,
        "7": mostrar_estadisticas,
    }

    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ").strip()

        if opcion == "0":
            print("\n[INFO] ¿Desea guardar los cambios antes de salir? (s/n): ", end="")
            respuesta = input().strip().lower()
            if respuesta == "s":
                guardar_paises(paises, ARCHIVO_CSV)
            print("\nHasta luego.\n")
            break

        elif opcion == "8":
            guardar_paises(paises, ARCHIVO_CSV)

        elif opcion in opciones:
            opciones[opcion](paises)

        else:
            print("[ERROR] Opción no válida. Ingrese un número del 0 al 8.")

        input("\nPresione Enter para continuar...")


# ─────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
