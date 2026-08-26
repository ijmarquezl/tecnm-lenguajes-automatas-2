# Bitácora de Requerimientos y Auditoría IA — Sesión 02
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Estudiante:** [Nombre Completo]  
**Matrícula:** [No. de Control]  
**Fecha:** [AAAA-MM-DD]  
**Track Seleccionado:** [ C | Rust ]  

---

## 1. Fase 1: El Artesano (Intuición y Dificultad Manual)
*Describe qué problema encontraste al implementar la liberación de nodos en memoria sin asistencia:*
> (Ejemplo: Al invocar `free(actual)`, perdí la dirección de `actual->siguiente`, lo que provocó una lectura inválida en la siguiente iteración).

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos y Contexto C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Estructura de lista enlazada simple para tokens de compilador en C99 / Rust 2021. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores especialista en seguridad de memoria. |
| **Especificación (E)** | Crear nodo con buffer seguro, insertar al final y liberar lista completa validando casos nulos. |
| **Output (O)** | Exclusivamente las funciones modulares sin preámbulos y análisis de complejidad $O(n)$. |

### 2.2 Diseño del Prompt Contextualizado
*Pega el prompt que diseñaste con base en la matriz anterior:*

```text
[Pega aquí tu prompt estructurado]
```

## 3. Código Devuelto por el Modelo
*Pega el bloque de código generado por el LLM:*
```code
C
// Código generado por la IA
```

## 4. Fase 3: El Auditor (Batería de Pruebas y Veredicto)
### 4.1 Resultados del Test Harness
```text
[ ] Lista vacía: ¿La rutina maneja liberar_lista(NULL) sin fallar?

[ ] Puntero nulo en creación: ¿Retorna NULL si el lexema de entrada es nulo?

[ ] Truncamiento de búfer: ¿Previene el desbordamiento de búfer en cadenas mayores a 31 caracteres?

[ ] Fugas de memoria: ¿Todos los nodos intermedios son liberados correctamente?
```
### 4.2 Reporte Crítico
¿La IA protegió el código contra Use-After-Free y asignación fallida (malloc == NULL) de forma nativa o tuviste que corregirlo?
```text
(Documenta tu análisis crítico aquí).
```
Firma digital: [Usuario de GitHub]
