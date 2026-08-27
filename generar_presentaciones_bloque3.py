#!/usr/bin/env python3
"""
Compilador de Presentaciones Enriquecidas (Bloque 3: Sesiones 21 a 30)
Unidad 3: Generación de Código Intermedio y Optimizaciones
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os

TEORIA_BLOQUE_3 = {
    21: {
        "tema": "Fundamentos de Código de Tres Direcciones (TAC)",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "La Representación Intermedia Lineal y Cuádruplos",
            "lead": "El código intermedio desacopla el frontend (análisis sintáctico/semántico) del backend (arquitectura de hardware objetivo).",
            "tarjetas": [
                ("01. Estructura de 3 Direcciones", "Instrucciones de la forma 'x = y op z', donde cada paso involucra a lo sumo dos operandos y un resultado.", "Simplifica expresiones complejas anidadas convirtiéndolas en una secuencia lineal de pasos atómicos."),
                ("02. Representación en Cuádruplos", "Tupla formal de 4 campos: (operador, argumento1, argumento2, resultado).", "Permite almacenar las instrucciones intermedias en un arreglo o lista enlazada homogénea."),
                ("03. Generación de Temporales Únicos", "El compilador asigna variables sintéticas autoincrementales (_t0, _t1, _t2...) para guardar resultados parciales.", "Facilita el análisis de vida de variables (Liveness Analysis) en fases posteriores de asignación de registros.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estructura de Datos de la Lista de Cuádruplos",
            "descripcion": "Modelado de instrucciones intermedias en memoria dinámica:",
            "tarjetas": [
                ("Estructura Quad", "struct Quad { OpCode op; char arg1[32]; char arg2[32]; char res[32]; struct Quad *sig; };", "Cada cuádruplo se encadena en una lista lineal de instrucciones emitida por el traductor de AST."),
                ("Ventaja sobre Triplos", "Los cuádruplos desacoplan el identificador del resultado de la posición física del arreglo.", "Permite mover, reordenar y eliminar instrucciones durante la optimización sin invalidar referencias cruzadas.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Generación de TAC",
            "items": [
                "Reutilizar nombres de temporales antes de que expire su tiempo de vida, corrompiendo datos en subexpresiones.",
                "Omitir el operador de asignación simple (x = y) intentando forzar un operador binario ficticio.",
                "Punteros nulos en argumentos no utilizados en operaciones unarias (ej. negación '_t0 = -a')."
            ]
        }
    },
    22: {
        "tema": "Generación de TAC para Expresiones Aritmético-Lógicas",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Aplanado Recursivo del AST en Instrucciones TAC",
            "lead": "El recorrido postorden del AST sintetiza nombres de variables temporales para aplanar la jerarquía de operadores.",
            "tarjetas": [
                ("01. Recorrido Postorden Generador", "Evalúa recursivamente las ramas izquierda y derecha, obteniendo sus nombres de retorno, y emite el cuádruplo del operador.", "Garantiza que los operandos estén calculados antes de utilizarlos."),
                ("02. Conservación de Precedencia", "La estructura jerárquica del AST dicta el orden de emisión en TAC sin necesidad de paréntesis explícitos.", "La expresión 'a + b * c' se convierte estrictamente en: '_t0 = b * c' seguido de '_t1 = a + _t0'."),
                ("03. Expresiones Booleanas como Enteros", "Las comparaciones ('<', '==', '!=') generan cuádruplos de asignación condicional o banderas booleanas (0 o 1).", "Permite tratar condiciones lógicas con la misma infraestructura que las operaciones aritméticas.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Sintetización del Atributo 'Lugar' (Place)",
            "descripcion": "Propagación ascendente de identificadores durante la traducción:",
            "tarjetas": [
                ("Atributo char* lugar", "Cada llamada a 'generar_tac(nodo)' retorna una cadena con el nombre de la variable o temporal donde reside el resultado.", "Las hojas devuelven su propio lexema ('x', '42'); los nodos internos devuelven su nuevo temporal ('_t0')."),
                ("Generador de Nombres (new_temp)", "Función atómica que incrementa un contador global: 'sprintf(buffer, \"_t%d\", contador++)'.", "Garantiza unicidad de identificadores temporales en toda la unidad de traducción.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Expresiones",
            "items": [
                "Inversión del orden de argumentos en operadores asimétricos: emitir '_t0 = b - a' para 'a - b'.",
                "Desbordamiento de buffer al formatear nombres de temporales con números altos (>10,000).",
                "Pérdida de la variable temporal devuelta por una rama en llamadas recursivas profundas."
            ]
        }
    },
    23: {
        "tema": "Etiquetas y Saltos Incondicionales (Goto)",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Modelado del Grafo de Flujo de Control (CFG)",
            "lead": "Las estructuras de control estructuradas se transforman en una red lineal de etiquetas (Labels) y bifurcaciones.",
            "tarjetas": [
                ("01. Instrucción Label", "Marca un punto de destino en el flujo de ejecución: 'LABEL L0'.", "No consume ciclos de hardware en sí misma; actúa como marcador de dirección en memoria."),
                ("02. Salto Incondicional (Goto)", "Transfiere la ejecución directamente a una etiqueta destino: 'GOTO L1'.", "Rompe la ejecución secuencial lineal de la lista de cuádruplos."),
                ("03. Bloques Básicos (Basic Blocks)", "Secuencia continua de instrucciones con una sola entrada (al inicio) y una sola salida (al final).", "La unidad fundamental sobre la cual operan los optimizadores de código.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Generador de Etiquetas y Punteros a Bloques",
            "descripcion": "Estructura de gestión de etiquetas simbólicas:",
            "tarjetas": [
                ("Generador new_label()", "Retorna identificadores únicos de destino: 'L0', 'L1', 'L2'...", "Permite anidar estructuras de control complejas sin colisión de nombres."),
                ("Cuádruplos de Salto", "Cuádruplo con operador OP_GOTO y arg1 apuntando a la cadena de la etiqueta destino.", "El backend traduce estas instrucciones directamente a 'jmp' en x86-64.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Saltos",
            "items": [
                "Saltos a etiquetas no declaradas o inexistentes en la tabla de cuádruplos.",
                "Etiquetas huérfanas sin instrucciones posteriores asociadas.",
                "Bucles infinitos no intencionados por etiquetas mal colocadas al cerrar funciones."
            ]
        }
    },
    24: {
        "tema": "Control de Flujo: Sentencias If e If-Else",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Saltos Condicionales y Evaluación de Cortocircuito",
            "lead": "La bifurcación condicional bifurca el flujo según el valor de verdad de una expresión booleana.",
            "tarjetas": [
                ("01. Instrucción ifFalse / ifTrue", "Evalúa un temporal booleano y salta si la condición se cumple o no: 'IFFALSE _t0 GOTO L_else'.", "Permite saltar sobre el bloque 'then' cuando la condición es falsa."),
                ("02. Estructura TAC de If-Else", "Patrón estándar: 'Condición -> IFFALSE L_else -> Cuerpo_Then -> GOTO L_fin -> LABEL L_else -> Cuerpo_Else -> LABEL L_fin'.", "Garantiza la exclusión mutua estricta entre ambas ramas."),
                ("03. Evaluación de Cortocircuito (Short-Circuit)", "En 'A && B', si A es falso, no se evalúa B; en 'A || B', si A es verdadero, no se evalúa B.", "Ahorra tiempo de cómputo y evita fallos de ejecución como desreferenciación nula en condiciones.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Plantilla de Emisión para Nodos If-Else",
            "descripcion": "Secuencia determinista de generación de etiquetas:",
            "tarjetas": [
                ("Reserva de Etiquetas al Iniciar", "Se reservan dos etiquetas: 'L_else = new_label()' y 'L_fin = new_label()'.", "Evita colisiones con etiquetas generadas recursivamente dentro del cuerpo del if."),
                ("Salto de Escape (Bypass)", "Al final del bloque 'then', es obligatorio emitir 'GOTO L_fin' para no ejecutar accidentalmente el bloque 'else'.", "El generador debe enlazar correctamente ambos flujos.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas en If-Else",
            "items": [
                "Olvidar el 'GOTO L_fin' al final del bloque 'then', provocando que se ejecuten ambas ramas consecutivamente.",
                "Evaluación estricta en lugar de cortocircuito cuando la condición contiene efectos secundarios.",
                "Etiquetas 'fin' duplicadas en sentencias if anidadas."
            ]
        }
    },
    25: {
        "tema": "Control de Flujo: Bucles While y For",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Estructuras Cíclicas, Invariantes y Salidas Múltiples",
            "lead": "Los ciclos repiten la ejecución de un bloque hasta que una condición de guardia se invalide.",
            "tarjetas": [
                ("01. Estructura TAC de Bucle While", "Patrón: 'LABEL L_inicio -> Evaluar_Condicion -> IFFALSE L_fin -> Cuerpo -> GOTO L_inicio -> LABEL L_fin'.", "Garantiza que la condición se evalúe antes de cada iteración."),
                ("02. Desugaring de Bucle For", "Un bucle 'for (init; cond; post) { body }' se transforma internamente en: 'init; while(cond) { body; post; }'.", "Simplifica el compilador al reutilizar la misma rutina de generación para ambos ciclos."),
                ("03. Sentencias Break y Continue", "'break' emite un 'GOTO L_fin'; 'continue' emite un 'GOTO L_inicio' o salto a la sección 'post'.", "Requiere mantener una pila de etiquetas de bucles activos para resolver destinos.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Pila de Contexto de Bucles (Loop Stack)",
            "descripcion": "Gestión de destinos para 'break' y 'continue' anidados:",
            "tarjetas": [
                ("Estructura LoopContext", "Contiene 'char label_inicio[32]' y 'char label_fin[32]' del bucle activo.", "Se empuja a una pila en 'push_loop()' y se retira en 'pop_loop()' al cerrar el ciclo."),
                ("Validación de Break Huérfano", "Si se encuentra una sentencia 'break' y la pila de bucles está vacía, emitir error semántico fatal.", "Previene saltos ilegales fuera de contextos de bucle o switch.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Ciclos",
            "items": [
                "Olvidar actualizar la variable de paso (post-incremento) en la transformación de bucles 'for'.",
                "Resolver un 'break' hacia el bucle exterior en ciclos anidados por no usar una pila LIFO.",
                "Emisión de la etiqueta de inicio después de la condición, impidiendo la reevaluación del ciclo."
            ]
        }
    },
    26: {
        "tema": "TAC para Llamadas a Funciones y Retornos",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Protocolo de Invocación, Parámetros y Cuádruplos Call",
            "lead": "El código intermedio desacopla el paso de argumentos preparando la secuencia de instrucciones de invocación.",
            "tarjetas": [
                ("01. Instrucción PARAM", "Emite cada argumento antes de la llamada: 'PARAM arg1', 'PARAM arg2'...", "En C, los parámetros se evalúan típicamente de derecha a izquierda o de izquierda a derecha."),
                ("02. Instrucción CALL", "Invoca la función especificando el nombre y el número de argumentos: '_t0 = CALL funcion, N'.", "El número N permite al backend saber cuántos parámetros limpiar de la pila si aplica."),
                ("03. Instrucción RETURN", "Emite 'RETURN expr' para funciones con valor o 'RETURN' para funciones void.", "Marca la salida del flujo de control de la rutina actual.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Llamadas Anidadas y Preservación de Temporales",
            "descripcion": "Resolución de expresiones como 'f(g(x), h(y))':",
            "tarjetas": [
                ("Evaluación Recursiva de Argumentos", "Primero se evalúa 'g(x)' y se guarda en '_t0'; luego 'h(y)' en '_t1'; finalmente 'PARAM _t0', 'PARAM _t1', 'CALL f, 2'.", "Garantiza que los temporales de llamadas internas no se sobrescriban."),
                ("Asignación del Resultado", "Si la función retorna valor, el cuádruplo asigna el resultado directamente a un nuevo temporal.", "Permite encadenar llamadas en expresiones matemáticas: 'x = f() + 5'.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas en Invocaciones",
            "items": [
                "Discrepancia entre la aridad del CALL y el número real de cuádruplos PARAM emitidos.",
                "Sobrescribir temporales de retorno al encadenar múltiples llamadas en la misma línea.",
                "No emitir instrucción RETURN al final de funciones que finalizan sin bloque explícito."
            ]
        }
    },
    27: {
        "tema": "Indexación de Arreglos en Código Intermedio",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Aplanado de Direcciones y Acceso Indexado",
            "lead": "En TAC, el acceso a arreglos 'A[i]' se descompone en un cálculo de desplazamiento y una lectura indexada.",
            "tarjetas": [
                ("01. Cálculo del Desplazamiento Lineal", "Multiplica el índice por el ancho del tipo: '_t0 = i * sizeof(T)'.", "Convierte el índice abstracto a un offset físico de memoria en bytes."),
                ("02. Lectura Indexada (Array Read)", "Instrucción de acceso indirecto: '_t1 = A[_t0]'.", "Carga en un temporal el valor ubicado en la dirección 'Base(A) + _t0'."),
                ("03. Escritura Indexada (Array Write)", "Instrucción de asignación a memoria: 'A[_t0] = valor'.", "Modifica el contenido del arreglo en memoria sin asignar a temporales intermediarios.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Aplanado de Arreglos Multidimensionales",
            "descripcion": "Cálculo de matrices bidimensionales A[N][M]:",
            "tarjetas": [
                ("Fórmula de Aplanado", "Para 'A[i][j]', calcula: '_t0 = i * M', '_t1 = _t0 + j', '_t2 = _t1 * sizeof(T)', '_t3 = A[_t2]'.", "Reduce accesos multidimensionales a un único cálculo de dirección lineal."),
                ("Optimización por Desplazamientos Constantes", "Si 'i' y 'j' son constantes numéricas conocidas, el offset total se calcula en tiempo de compilación.", "Elimina todas las multiplicaciones intermedias en runtime.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Indexación TAC",
            "items": [
                "Olvidar multiplicar el índice por el tamaño del elemento en bytes (sizeof).",
                "Confundir la lectura indexada con la escritura en sentencias de asignación 'A[i] = B[j]'.",
                "Desbordamiento de entero en el cálculo de offsets para arreglos tridimensionales grandes."
            ]
        }
    },
    28: {
        "tema": "Optimización Local: Plegado de Constantes (Constant Folding)",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Reducción Estática y Propagación de Constantes",
            "lead": "El optimizador simplifica expresiones constantes en tiempo de compilación para ahorrar instrucciones de CPU.",
            "tarjetas": [
                ("01. Plegado de Constantes (Constant Folding)", "Si los dos argumentos de un cuádruplo son literales ('_t0 = 3 + 5'), se evalúa en compilación reemplazándolo por '_t0 = 8'.", "Reduce el número total de instrucciones que llegarán al ensamblador."),
                ("02. Propagación de Constantes (Constant Propagation)", "Si una variable tiene asignado un valor constante ('x = 10'), sus usos posteriores se reemplazan por el valor literal.", "Habilita nuevos plegados de constantes en instrucciones dependientes."),
                ("03. Identidades Algebraicas", "Simplificación de operaciones redundantes: 'x + 0 -> x', 'x * 1 -> x', 'x * 0 -> 0', 'x * 2 -> x + x'.", "Sustituye operaciones costosas (multiplicaciones) por operaciones más rápidas o las elimina.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Algoritmo de Paso Local sobre Cuádruplos",
            "descripcion": "Transformación iterativa de la lista de instrucciones:",
            "tarjetas": [
                ("Pase de Análisis de Constantes", "Recorre la lista de cuádruplos; si detecta constantes, calcula el resultado y modifica el cuádruplo a una asignación directa.", "Se repite en bucle hasta alcanzar un punto fijo donde no haya más simplificaciones posibles."),
                ("Preservación de Semántica", "El optimizador debe respetar estrictamente el tamaño de los enteros para no alterar desbordamientos legítimos.", "Garantiza que el código optimizado produzca el mismo resultado que el original.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos Críticos en Plegado",
            "items": [
                "Intentar plegar una división entre cero ('_t0 = 10 / 0') provocando la caída del propio compilador.",
                "Propagar constantes a través de etiquetas de salto donde la variable podría haber sido modificada por otra ruta.",
                "Divergencia de precisión en operaciones de punto flotante entre host y target."
            ]
        }
    },
    29: {
        "tema": "Optimización: Eliminación de Código Muerto (Dead Code Elimination)",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Detección de Instrucciones Inalcanzables y Variables Huérfanas",
            "lead": "Elimina instrucciones que calculan valores nunca leídos o que residen en bloques inalcanzables.",
            "tarjetas": [
                ("01. Instrucciones Inalcanzables (Unreachable Code)", "Código colocado inmediatamente después de un 'GOTO' o 'RETURN' sin una etiqueta intermedia.", "Se eliminan de forma segura ya que el flujo de ejecución nunca puede alcanzarlas."),
                ("02. Variables Muertas (Dead Variables)", "Asignaciones a temporales o variables locales que nunca vuelven a leerse antes de ser sobrescritas o salir de ámbito.", "Reduce la presión sobre los registros de CPU en el backend."),
                ("03. Poda de Ramas Condicionales Muertas", "En 'if (0) { ... }' o 'if (1) { ... }', el optimizador elimina la rama que nunca se ejecutará y el salto condicional.", "Convierte bifurcaciones complejas en código secuencial directo.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Análisis de Alcance y Grafo de Flujo (Reachability)",
            "descripcion": "Algoritmo de marcado y barrido sobre el CFG:",
            "tarjetas": [
                ("Grafo de Bloques Básicos", "Se construye un grafo dirigido donde cada nodo es un bloque básico y las aristas son saltos.", "Un recorrido BFS/DFS desde el bloque inicial marca todos los bloques alcanzables."),
                ("Barrido de Instrucciones Huérfanas", "Cualquier bloque no marcado como alcanzable se desvincula y se libera de la memoria de cuádruplos.", "Reduce significativamente el tamaño del binario final.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Eliminación de Código",
            "items": [
                "Eliminar una instrucción con efectos secundarios (como llamadas a funciones de I/O) creyendo erróneamente que es código muerto.",
                "Borrar etiquetas que son destinos de saltos indirectos o tablas de saltos (switch).",
                "Romper punteros de la lista de cuádruplos al desvincular un nodo eliminado."
            ]
        }
    },
    30: {
        "tema": "Hito 3: Generador de TAC y Optimizador End-to-End",
        "unidad": "Unidad 3: Código Intermedio y Optimización",
        "teoria_principal": {
            "titulo": "Integración del Generador de Código Intermedio y Optimizaciones",
            "lead": "Culminación de la Unidad 3. El compilador traduce un programa fuente completo a código TAC lineal y aplica optimizaciones locales.",
            "tarjetas": [
                ("01. Pipeline Intermedio Completo", "Flujo: 'AST Decorado -> Emisión de Cuádruplos -> Plegado de Constantes -> Eliminación de Código Muerto -> TAC Optimizado'.", "Produce una lista de instrucciones atómicas lista para la generación de ensamblador."),
                ("02. Emisión Textual de TAC", "Capacidad de volcar la lista de cuádruplos a un archivo '.tac' legible para inspección y depuración.", "Permite verificar visual y algorítmicamente la corrección de las optimizaciones aplicadas."),
                ("03. Entrega de Hito 3 (Git Tag)", "Etiquetado formal de versión en GitHub: 'git tag v0.3-hito3'.", "Representa el 25% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría de Integridad del Código Intermedio",
            "descripcion": "Verificación estricta de la suite de cuádruplos:",
            "tarjetas": [
                ("Verificación de Unicidad de Etiquetas", "Comprobación de que no existan etiquetas duplicadas ni saltos a destinos indefinidos.", "Garantiza que el generador de código x86-64 no produzca errores de ensamblado."),
                ("Batería de Pruebas de Estrés de Optimización", "Prueba con programas de alta complejidad: ciclos anidados con arreglos, expresiones aritméticas extensas y múltiples funciones.", "Comprueba que el código optimizado mantenga equivalencia semántica estricta.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 3",
            "items": [
                "Generar cuádruplos sintácticamente inválidos o con argumentos superpuestos.",
                "Corrupción de la lógica del programa tras aplicar el pase de Constant Folding.",
                "Fugas de memoria al desvincular cuádruplos durante la optimización de código muerto."
            ]
        }
    }
}

def compilar_presentacion_5_slides(num, data):
    n_str = f"{num:02d}"
    tema = data["tema"]
    unidad = data["unidad"]
    tp = data["teoria_principal"]
    am = data["arquitectura_memoria"]
    cb = data["casos_borde"]

    cards_s2 = ""
    for t_tit, t_desc, t_det in tp["tarjetas"]:
        cards_s2 += f"""
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">{t_tit}</span><span class="expand-hint">[+]</span></div>
          <p>{t_desc}</p>
          <div class="card-details">{t_det}</div>
        </div>"""

    cards_s3 = ""
    for a_tit, a_desc, a_det in am["tarjetas"]:
        cards_s3 += f"""
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">{a_tit}</span><span class="expand-hint">[+]</span></div>
          <p>{a_desc}</p>
          <div class="card-details">{a_det}</div>
        </div>"""

    items_s4 = "".join([f"<li><strong>{item}</strong></li>" for item in cb["items"]])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sesión {n_str}: {tema} | Lenguajes y Autómatas II</title>
  <style>
    :root {{
      --bg: #f4f8fb;
      --card-bg: rgba(255, 255, 255, 0.88);
      --card-bg-hover: rgba(255, 255, 255, 0.98);
      --border: #d0dbe5;
      --border-focus: #0969da;
      --accent: #0969da;
      --accent-green: #1a7f37;
      --accent-silver: #627282;
      --accent-orange: #d29922;
      --text: #334155;
      --text-bright: #0f172a;
      --font-mono: 'Fira Code', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    header {{
      padding: 12px 28px;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{ font-weight: 700; color: var(--text-bright); font-size: 0.95rem; }}
    .tag {{
      background-color: #ddf4ff;
      color: var(--accent);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      font-weight: 600;
      border: 1px solid #b6e3ff;
    }}
    main {{ flex: 1; display: flex; position: relative; overflow: hidden; }}
    .slide {{
      position: absolute;
      inset: 0;
      padding: 30px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      opacity: 0;
      visibility: hidden;
      transform: translateX(30px);
      transition: all 0.3s ease;
    }}
    .slide.active {{ opacity: 1; visibility: visible; transform: translateX(0); }}
    h1 {{ font-size: 2rem; color: var(--text-bright); margin-bottom: 12px; }}
    h2 {{ font-size: 1.5rem; color: var(--text-bright); margin-bottom: 16px; }}
    p.lead {{ font-size: 1.05rem; line-height: 1.5; max-width: 900px; margin-bottom: 18px; color: #475569; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px;
      cursor: pointer;
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
    }}
    .card:hover {{ background: var(--card-bg-hover); border-color: var(--border-focus); transform: translateY(-2px); }}
    .card.expanded {{ border-color: var(--accent); background: #ffffff; }}
    .card-header {{ font-weight: 600; color: var(--text-bright); margin-bottom: 8px; display: flex; justify-content: space-between; }}
    .expand-hint {{ font-size: 0.75rem; color: var(--accent); font-family: var(--font-mono); }}
    .card p, .card li {{ font-size: 0.88rem; line-height: 1.45; color: var(--text); }}
    .card-details {{ max-height: 0; overflow: hidden; opacity: 0; transition: all 0.3s ease; font-size: 0.82rem; color: #475569; }}
    .card.expanded .card-details {{ max-height: 240px; opacity: 1; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); }}
    .interactive-box {{
      margin-top: 18px;
      padding: 14px 18px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }}
    footer {{
      padding: 12px 28px;
      background: rgba(255, 255, 255, 0.85);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .progress {{ font-size: 0.85rem; font-family: var(--font-mono); color: var(--accent); font-weight: 600; }}
    .controls {{ display: flex; gap: 10px; }}
    button {{
      background: #ffffff;
      color: var(--text-bright);
      border: 1px solid var(--border);
      padding: 7px 18px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
    }}
    button:hover {{ background: #f1f5f9; }}
    button:disabled {{ opacity: 0.4; cursor: not-allowed; }}
  </style>
</head>
<body>
  <header>
    <div class="brand">TecNM Cancún &bull; SCD-1016</div>
    <div class="tag">SESIÓN {n_str} / 40 &bull; {tema}</div>
  </header>

  <main>
    <section class="slide active">
      <div class="tag" style="width: fit-content; margin-bottom: 10px;">{unidad.upper()}</div>
      <h1>{tema}</h1>
      <p class="lead">Sesión {n_str} del curso. Generación de código intermedio, aplanado de estructuras de control y optimizaciones locales con la Tríada Metodológica.</p>
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>
          <p>Codificación manual sin IA para comprender la manipulación de cuádruplos y temporales.</p>
          <div class="card-details">Construcción directa de traductores de AST a instrucciones lineales de tres direcciones.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>
          <p>Especificación de requerimientos C-R-E-O para la emisión atómica de instrucciones intermedias.</p>
          <div class="card-details">Definición de invariantes en grafos de control, etiquetas y preservación semántica en optimizaciones.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>
          <p>Test Harness automatizado para auditar la equivalencia funcional del código optimizado.</p>
          <div class="card-details">Pruebas destructivas sobre cortocircuito booleano, ciclos anidados y eliminación de código inalcanzable.</div>
        </div>
      </div>
    </section>

    <section class="slide">
      <h2>00–20 min: Fundamentos Teóricos — {tp["titulo"]}</h2>
      <p class="lead">{tp["lead"]}</p>
      <div class="grid-3">
        {cards_s2}
      </div>
      <div class="interactive-box">
        <strong>Invariante de Código Intermedio:</strong> Toda operación compleja debe aplanarse a instrucciones con a lo sumo dos operandos y un resultado.
      </div>
    </section>

    <section class="slide">
      <h2>Arquitectura de Memoria y Estructuras de Datos: {am["titulo"]}</h2>
      <p class="lead">{am["descripcion"]}</p>
      <div class="grid-2">
        {cards_s3}
      </div>
    </section>

    <section class="slide">
      <h2>{cb["titulo"]}</h2>
      <p class="lead">Puntos críticos de falla que deben protegerse en la generación de TAC y auditarse en las respuestas del LLM:</p>
      <div class="card" style="padding: 24px;">
        <ul style="padding-left: 20px; line-height: 2;">
          {items_s4}
        </ul>
      </div>
    </section>

    <section class="slide">
      <h2>Dinámica del Laboratorio y Protocolo de Entrega</h2>
      <div class="grid-2">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Estructura de la Clase (60 min)</span><span class="expand-hint">[+]</span></div>
          <ul>
            <li><strong>00–20 min:</strong> Fundamento teórico y aplanado de estructuras.</li>
            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual sin IA).</li>
            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>
            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness).</li>
            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>
          </ul>
          <div class="card-details">Verifica que las pruebas del Test Harness pasen al 100% antes de subir tu bitácora.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>
          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>
          <div class="card-details">La entrega de la Sesión 30 concluye formalmente el Hito 3 del Proyecto Integrador.</div>
        </div>
      </div>
      <div class="interactive-box">
        <strong>Docente Titular:</strong> MCC. Iván Márquez Larios (<code>ijmarquezl</code>) &bull; TecNM Cancún
      </div>
    </section>
  </main>

  <footer>
    <div class="progress" id="slideIndicator">SLIDE 1 / 5</div>
    <div class="controls">
      <button id="prevBtn" onclick="prevSlide()" disabled>&larr; Anterior</button>
      <button id="nextBtn" onclick="nextSlide()">Siguiente &rarr;</button>
    </div>
  </footer>

  <script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const indicator = document.getElementById('slideIndicator');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    function updateSlides() {{
      slides.forEach((slide, index) => slide.classList.toggle('active', index === currentSlide));
      indicator.textContent = `SLIDE ${{currentSlide + 1}} / ${{slides.length}}`;
      prevBtn.disabled = currentSlide === 0;
      nextBtn.disabled = currentSlide === slides.length - 1;
    }}
    function nextSlide() {{ if (currentSlide < slides.length - 1) {{ currentSlide++; updateSlides(); }} }}
    function prevSlide() {{ if (currentSlide > 0) {{ currentSlide--; updateSlides(); }} }}
    function toggleCard(card) {{
      card.classList.toggle('expanded');
      const hint = card.querySelector('.expand-hint');
      if (hint) hint.textContent = card.classList.contains('expanded') ? '[-]' : '[+]';
    }}
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    }});
  </script>
</body>
</html>
"""
    return html

def main():
    print("🚀 Compilando presentaciones enriquecidas (Bloque 3: Sesiones 21 a 30)...")
    os.makedirs("presentaciones", exist_ok=True)
    for num, data in TEORIA_BLOQUE_3.items():
        n_str = f"{num:02d}"
        html_content = compilar_presentacion_5_slides(num, data)
        out_path = f"presentaciones/sesion{n_str}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  -> Generada: {out_path} (5 slides completos)")
    print("✅ Bloque 3 de presentaciones actualizado con éxito.")

if __name__ == "__main__":
    main()