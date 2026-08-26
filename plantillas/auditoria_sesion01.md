# Bitácora de Requerimientos y Auditoría IA — Sesión 01
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Estudiante:** [Nombre Completo]  
**Matrícula:** [No. de Control]  
**Fecha:** [AAAA-MM-DD]  
**Track:** [ C | Rust ]  

---

## 1. Fase 1: El Artesano (Intuición y Dificultad Manual)
*Describe el reto de memoria/punteros que identificaste al intentar resolver el problema a mano sin ayuda de IA:*
> (Ejemplo: Al mover el puntero fin con `str + strlen(str) - 1`, me encontré con un acceso fuera de límites si la cadena estaba vacía).

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos y Contexto)

### 2.1 Matriz de Especificación y Casos Borde
Completa el contrato formal antes de redactar tu prompt:

| Dimensión | Especificación Técnica Formal |
| :--- | :--- |
| **Firma de la función** | `void invertir_cadena(char *str)` (o firma equivalente en Rust) |
| **Precondiciones** | El puntero debe apuntar a memoria modificable (*Heap* o *Stack*), o manejar `NULL`. |
| **Postcondiciones** | La cadena original queda invertida in-place; $O(n)$ tiempo, $O(1)$ memoria auxiliar. |
| **Restricciones de Entorno** | C99 / GCC, sin bibliotecas externas, sin `malloc`, sin usar arreglos auxiliares. |
| **Casos Límite a Proteger** | 1. Puntero `NULL`, 2. Cadena vacía `""`, 3. Longitud par/impar, 4. Búfer de 1 caracter. |

### 2.2 Diseño del Prompt Contextualizado
*Pega aquí el prompt estructurado que construiste utilizando la matriz anterior:*

```text
[Pega tu prompt con Rol, Contexto de memoria, Especificación y Restricciones explícitas]

## 3. Código devuelto por el modelo
*Pega aquí el fragmento de código generado por el LLM
C

## 4. Fase 3: El Auditor (Batería de Pruebas y Veredicto)

### 4.1 Resultados del Test Harness
Indica si el código generado superó las pruebas de estrés ejecutadas en Colab:

[ ] Puntero Nulo (NULL): ¿Sobrevive sin Segmentation Fault?

[ ] Cadena vacía (""): ¿Mantiene el terminador nulo sin alterar memoria?

[ ] Cadena de 1 caracter ("A"): ¿Evita cruces inválidos de punteros?

[ ] Longitud Par e Impar ("AB", "ABC"): ¿Invierte correctamente todos los índices?

### 4.2 Reporte Crítico y Correcciones
¿Qué caso límite o problema de arquitectura omitió la IA y cómo lo solucionaste en tu versión final?

(Describe tu análisis y corrección aquí).

Firma digital: [Usuario de GitHub]
