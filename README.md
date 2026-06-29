# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador (TPI) – Programación 1**
**Tecnicatura Universitaria en Programación (TUP) – UTN**

---

## Descripción

Aplicación de consola en Python que permite gestionar un dataset de países leído desde un archivo CSV. El sistema implementa funcionalidades de búsqueda, filtrado, ordenamiento y estadísticas, aplicando los conceptos de **Programación 1**: listas, diccionarios, funciones, condicionales, bucles y manejo de archivos.

---

## Requisitos

- Python 3.x (sin librerías externas, solo `csv` y `os` de la biblioteca estándar)

---

## Estructura del proyecto

```
tpi_paises/
├── gestion_paises.py   # Código fuente principal
├── paises.csv          # Dataset base con 44 países
└── README.md           # Este archivo
```

---

## Cómo ejecutar

```bash
python3 gestion_paises.py
```

El programa cargará automáticamente el archivo `paises.csv` del directorio actual y presentará el menú principal.

---

## Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1 | Mostrar todos los países en tabla |
| 2 | Agregar un nuevo país (sin campos vacíos) |
| 3 | Actualizar población y/o superficie de un país |
| 4 | Buscar país por nombre (coincidencia parcial) |
| 5 | Filtrar por continente, rango de población o superficie |
| 6 | Ordenar por nombre, población o superficie (asc/desc) |
| 7 | Estadísticas: máx/mín población, promedios, conteo por continente |
| 8 | Guardar cambios en el CSV |
| 0 | Salir (con opción de guardar) |

---

## Ejemplos de uso

### Buscar un país

```
Opción: 4
Ingrese el nombre o parte del nombre a buscar: arg

 Nombre                              │        Población │  Superficie (km²) │ Continente
─────────────────────────────────────────────────────────────────────────────
 Argentina                           │       45,376,763 │         2,780,400 │ América
```

### Filtrar por continente

```
Opción: 5 → 1
Continentes disponibles: África, América, Asia, Europa, Oceanía
Ingrese el continente: Europa

Países en Europa (10):
 Alemania | España | Francia | ...
```

### Estadísticas

```
Opción: 7

  Total de países cargados : 44
  Población:
    Mayor  → China (1,412,600,000 hab.)
    Menor  → Fiyi (930,748 hab.)
    Promedio → 140,113,748 hab.
  Superficie:
    Promedio → 1,832,660 km²
  Países por continente:
    África               10 país/es
    América              10 país/es
    Asia                 10 país/es
    Europa               10 país/es
    Oceanía               4 país/es
```

---

## Formato del CSV

```
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
```

---

## Dataset base

El archivo `paises.csv` incluye **44 países** distribuidos entre América, Europa, Asia, África y Oceanía.

---

## Integrante

| Nombre | Matricula |
|--------|--------|
| Troncoso Leonardo Gabriel | 103359 |


---

## Links

- **Repositorio GitHub:** https://github.com/Argenproyec/Gestion-de-paises.git
- **Video demostrativo:** 
- **Documentación PDF:** https://github.com/Argenproyec/Gestion-de-paises.git
