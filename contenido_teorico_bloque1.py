# contenido_teorico_bloque1.py
# Base de conocimiento conceptual: Unidad 1 (Sesiones 01 a 10)
# Materia: Lenguajes y Autómatas II (SCD-1016)
# Docente Titular: MCC. Iván Márquez Larios (ijmarquezl)

TEORIA_BLOQUE_1 = {
    1: {
        "tema": "Encuadre, Diagnóstico de Punteros y Metodología IA",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "El Código Fuente como Flujo Continuo de Memoria",
            "lead": "Todo compilador trata al programa de entrada como una secuencia contigua de bytes. Manipular punteros es la base del escaneo léxico y semántico.",
            "tarjetas": [
                ("01. Segmentación de Memoria", "El código fuente reside en el Heap o Data Segment; los punteros del escáner avanzan sobre direcciones virtuales lineales.", "Un error de puntero (desplazamiento fuera del buffer) genera un fallo de segmentación (SIGSEGV)."),
                ("02. Aritmética de Punteros", "Avanzar `ptr++` incrementa la dirección en `sizeof(*ptr)` bytes. En `char*`, el salto es de 1 byte exacto.", "Permite calcular distancias entre lexemas y offsets sin copias auxiliares en memoria."),
                ("03. Invariante de Terminación", "Toda cadena en C finaliza en el byte nulo `\\0` (0x00). Si se sobreescribe, el compilador leerá memoria no asignada.", "El cálculo de longitud `strlen()` recorre hasta encontrar `\\0`, con complejidad O(n).")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Inversión In-Place: Stack vs Heap",
            "descripcion": "Modelado del intercambio de punteros en los extremos del buffer:",
            "tarjetas": [
                ("Punteros Contrapuestos", "Un puntero `inicio` en `str` y un puntero `fin` en `str + len - 1` convergen al centro en O(n/2) pasos.", "Requiere verificar que `inicio < fin` en cada iteración."),
                ("Memoria Auxiliar O(1)", "El intercambio usa un solo byte temporal en el registro/pila sin invocar `malloc()` ni duplicar el buffer.", "Garantiza eficiencia máxima en entornos restringidos de compilación.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones y Casos Límite a Proteger",
            "items": [
                "Puntero `NULL`: Intentar desreferenciar `*str` cuando `str == NULL` causa terminación abrupta.",
                "Buffer de solo lectura: Intentar mutar un literal `char *s = \"HOLA\";` causa violación de segmento en el segmento `.rodata`.",
                "Cadenas vacías `\"\"`: `fin` apuntaría a `str - 1`, una dirección ilegal previa al inicio del buffer."
            ]
        }
    },
    2: {
        "tema": "Gestión en GitHub Web y Nodos Dinámicos en Heap",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Estructuras Dinámicas para Tokens y Símbolos",
            "lead": "El compilador no conoce a priori el tamaño del programa. Cada token o nodo debe instanciarse dinámicamente en el Heap.",
            "tarjetas": [
                ("01. Asignación Dinámica", "`malloc(sizeof(Token))` reserva memoria contigua en el Heap y devuelve un puntero genérico `void*`.", "El sistema operativo marca el bloque como ocupado en la tabla de páginas."),
                ("02. Tiempo de Vida (Lifetime)", "A diferencia del Stack (que se limpia al salir de la función), la memoria en Heap persiste hasta invocar `free()`.", "Olvidar liberar memoria genera *Memory Leaks* que saturan la compilación de programas extensos."),
                ("03. Enlazamiento Simple", "Cada nodo contiene su carga útil (lexema, tipo) y un puntero autoreferenciado `struct Token *siguiente`.", "Permite construir flujos de tokens de longitud arbitraria O(n).")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "El Ciclo de Liberación Segura",
            "descripcion": "Prevención del fallo crítico *Use-After-Free*:",
            "tarjetas": [
                ("Puntero Auxiliar Temporal", "Antes de ejecutar `free(actual)`, es indispensable respaldar `actual->siguiente` en una variable temporal.", "Acceder a `actual->siguiente` después de liberar `actual` es comportamiento indefinido (UB)."),
                ("Modelo RAII en Rust", "`Box<Token>` transfiere la propiedad; cuando el nodo sale de ámbito, Rust invoca `drop()` automáticamente.", "Elimina por completo fugas de memoria y punteros colgantes en tiempo de compilación.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en la Gestión de Nodos",
            "items": [
                "Desbordamiento en copia de lexema: Usar `strcpy` en lugar de `strncpy` provocando buffer overflow.",
                "Fallo de asignación: No verificar si `malloc` retornó `NULL` por agotamiento de memoria del sistema.",
                "Liberación de lista vacía: No proteger la función de liberación cuando la cabeza de la lista es `NULL`."
            ]
        }
    },
    3: {
        "tema": "Google Colab, Mágicos y Flujo de Entrega",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Automatización de Compiladores en Entornos Linux",
            "lead": "Un compilador se ejecuta como una herramienta de línea de comandos (CLI) sujeta a convenciones POSIX y códigos de retorno.",
            "tarjetas": [
                ("01. Comandos Mágicos %%writefile", "Colab permite volcar el contenido de una celda directamente al sistema de archivos virtual de Linux.", "Permite crear módulos `.c`, `.rs` y scripts de prueba limpios y reproducibles."),
                ("02. Códigos de Salida ABI (Exit Codes)", "El valor retornado por `main()` (`return 0;` vs `return 1;`) indica al sistema si la compilación fue exitosa.", "Un compilador que falla debe retornar un código distinto de cero para detener el pipeline de construcción."),
                ("03. Banderas Estrictas de GCC", "Compilar con `-Wall -Wextra -Werror` convierte cualquier advertencia de tipos o punteros en un error fatal.", "Evita que errores sutiles de compilación pasen desapercibidos a fases posteriores.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Llamadas al Sistema y Flujos Estándar",
            "descripcion": "Separación de flujos para diagnósticos limpios:",
            "tarjetas": [
                ("stdout vs stderr", "El código generado se emite a `stdout` (1); los mensajes de error semántico deben enviarse a `stderr` (2).", "Permite redirigir el código objeto generado sin contaminarlo con logs de depuración."),
                ("Tuberías (Pipes POSIX)", "La salida de un pase del compilador alimenta la entrada del siguiente: `scanner | parser | codegen`.", "Reduce el acceso a disco intermedio manteniendo los datos en memoria compartida.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en el Pipeline",
            "items": [
                "Escribir logs de depuración en `stdout` rompiendo la generación del archivo ensamblador.",
                "Ignorar advertencias de conversión de tipos enteros con signo a no signo.",
                "No limpiar archivos binarios previos generando pruebas falsas positivas con binarios obsoletos."
            ]
        }
    },
    4: {
        "tema": "Anatomía de un Árbol Sintáctico Abstracto (AST)",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "De Árbol de Derivación Concreta (CST) a AST",
            "lead": "El CST contiene ruido sintáctico (paréntesis, palabras reservadas). El AST preserva únicamente la esencia semántica y la jerarquía de las operaciones.",
            "tarjetas": [
                ("01. Nodos Hoja vs Nodos Internos", "Las hojas almacenan operandos (literales numéricos, variables). Los nodos internos representan operadores y sentencias.", "En `3 + 5 * 2`, las hojas son `3`, `5`, `2`; los nodos internos son `+` y `*`."),
                ("02. Tipos de Nodo Discriminados", "Un AST requiere un discriminante (`enum NodeType`) para interpretar correctamente la unión de datos de cada nodo.", "Permite representar de forma homogénea expresiones binarias, asignaciones y llamadas a función."),
                ("03. Estructura Recursiva", "Cada nodo rama contiene punteros a sus hijos izquierdo y derecho (`struct ASTNode *izq, *der`).", "Refleja la naturaleza recursiva de las gramáticas libres de contexto.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Modelado de Nodos AST en Heap",
            "descripcion": "Uniones discriminadas en C vs Enums con datos en Rust:",
            "tarjetas": [
                ("Uniones Etiquetadas (C)", "Una estructura con `tipo_nodo` y un `union` que comparte espacio para `valor_int`, `nombre_var` o punteros binarios.", "Ahorra memoria en Heap al dimensionar el nodo al tamaño de su miembro más grande."),
                ("Tipos Algebraicos (Rust)", "`enum ASTNode { Num(i32), Var(String), BinOp(char, Box<ASTNode>, Box<ASTNode>) }`.", "El compilador verifica exhaustivamente los patrones mediante `match`, evitando punteros nulos.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en la Construcción del AST",
            "items": [
                "Árbol con ciclos: Un puntero hijo que apunte a un ancestro provocará recursión infinita en todos los recorridos.",
                "Desreferenciación de nodo nulo en operadores unarios (ej. negación `-x` con rama derecha `NULL`).",
                "Fuga de memoria masiva al descartar ramas de árboles tras detectar un error semántico."
            ]
        }
    },
    5: {
        "tema": "Recorridos del AST y Notación Polaca Inversa",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Patrones de Recorrido y Orden Topológico",
            "lead": "Para procesar un AST, debemos visitar sus nodos en un orden determinista según la tarea requerida.",
            "tarjetas": [
                ("01. Preorden (Raíz, Izq, Der)", "Útil para emitir declaraciones, copiar árboles o procesar estructuras de control como `if/while`.", "Visita el nodo padre antes que a cualquiera de sus operandos."),
                ("02. Inorden (Izq, Raíz, Der)", "Permite reconstruir la expresión matemática en infijo original con su orden matemático.", "Solo es aplicable a operadores binarios simétricos."),
                ("03. Postorden (Izq, Der, Raíz)", "El patrón fundamental de evaluación: evalúa primero los operandos hijos y luego aplica el operador padre.", "Genera directamente la Notación Polaca Inversa (RPN), base de las máquinas de pila.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Consumo de Stack en Recorridos Recursivos",
            "descripcion": "Gestión del marco de pila durante la evaluación profunda:",
            "tarjetas": [
                ("Profundidad de Árbol h", "Cada nivel del árbol añade un marco de función al Stack del sistema operativo. Complejidad espacial O(h).", "Árboles degenerados lineales muy profundos (>10,000 nodos) provocan desbordamiento del Stack."),
                ("Evaluación con Pila Explícita", "En RPN, cada hoja se apila (`push`); cada operador desapila dos valores (`pop`), calcula y apila el resultado.", "Permite evaluar expresiones complejas sin llamadas recursivas adicionales.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Recorridos",
            "items": [
                "Inversión de operandos en operadores no conmutativos: Restar `der - izq` en lugar de `izq - der`.",
                "No validar punteros `NULL` antes de invocar la llamada recursiva izquierda o derecha.",
                "Modificación del árbol durante el recorrido sin actualizar los punteros padre."
            ]
        }
    },
    6: {
        "tema": "Sistema de Tipos Primitivos y Verificación Semántica",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "El Rol del Analizador Semántico",
            "lead": "La sintaxis valida que la estructura sea legal; la semántica valida que las operaciones tengan sentido lógico y de tipos.",
            "tarjetas": [
                ("01. Tipado Estático vs Dinámico", "En compiladores estáticos, cada variable y expresión tiene un tipo determinado en tiempo de compilación.", "Previene errores de ejecución antes de generar una sola instrucción binaria."),
                ("02. Tabla de Compatibilidad", "Una matriz booleana que define qué tipos pueden operar entre sí (ej. `int + int -> int`, `int + float -> float`).", "Determina si una operación es legal, requiere conversión o es un error semántico."),
                ("03. Equivalencia de Tipos", "Equivalencia nominal (mismo nombre de tipo) vs estructural (misma disposición de bytes interna).", "C utiliza equivalencia nominal para `struct` y estructural para tipos básicos vía `typedef`.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Atributos Sintetizados de Tipo en el AST",
            "descripcion": "Decoración del árbol con información de tipo durante el postorden:",
            "tarjetas": [
                ("Propagación Ascendente", "El tipo de un nodo operador se sintetiza a partir de los tipos ya validados de sus dos ramas hijas.", "Si `izq->tipo == INT` y `der->tipo == INT`, el nodo actual sintetiza `tipo = INT`."),
                ("Tipo ERROR_TYPE", "Tipo centinela especial asignado a nodos inválidos para evitar que un solo error dispare una cascada de falsas alertas.", "El analizador semántico reporta el primer error y propaga el centinela.")
            ]
        },
        "casos_borde": {
            "titulo": "Errores Semánticos Típicos",
            "items": [
                "Asignación de tipos incompatibles: Asignar un puntero a una variable entera sin casteo explícito.",
                "Operadores incompatibles: Intentar aplicar operaciones aritméticas a estructuras o cadenas.",
                "Cascada infinita de errores por no usar un tipo centinela al detectar el primer fallo."
            ]
        }
    },
    7: {
        "tema": "Evaluación de Expresiones Aritméticas y Casos Límite",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Intérprete AST y Evaluación Constante",
            "lead": "El analizador semántico debe ser capaz de evaluar expresiones constantes en tiempo de compilación para optimizar el código.",
            "tarjetas": [
                ("01. Evaluación Recursiva", "Función `evaluar(ASTNode *nodo)` que resuelve recursivamente subárboles constantes.", "Si ambos hijos son constantes numéricas, el nodo puede colapsarse a una sola hoja."),
                ("02. Desbordamiento Aritmético (Overflow)", "Operaciones que exceden los límites del tipo (ej. `INT_MAX + 1` en enteros de 32 bits).", "El compilador debe advertir o manejar el desbordamiento según la especificación del lenguaje."),
                ("03. División entre Cero", "Detectar operaciones `x / 0` o `x % 0` estáticamente durante el análisis del programa.", "Debe reportarse como error semántico fatal antes de intentar la evaluación en el host.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Manejo Seguro de Excepciones Aritméticas",
            "descripcion": "Validación preventiva en el host de compilación:",
            "tarjetas": [
                ("Verificación de Divisor Nulo", "Antes de ejecutar la operación `/` o `%`, evaluar si la rama derecha se resuelve a valor cero.", "Evita que el propio compilador sufra una interrupción `SIGFPE` (Floating Point Exception)."),
                ("Tipos Seguros con Signo", "Manejo del caso borde de enteros mínimos: `-INT_MIN` causa overflow en arquitecturas de complemento a 2.", "Requiere promociones temporales a tipos de 64 bits durante la evaluación estática.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Evaluación Estática",
            "items": [
                "Interrupción del compilador por división entre cero en expresiones constantes.",
                "Divergencia de precisión de flotantes entre la máquina host (donde compila) y target (donde corre).",
                "Mutación de variables globales durante la evaluación de expresiones que deberían ser puras."
            ]
        }
    },
    8: {
        "tema": "Inferencia y Promoción de Tipos",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Coerción Implícita y Ensanchamiento de Tipos",
            "lead": "Cuando los tipos de los operandos difieren pero son compatibles, el compilador debe insertar conversiones implícitas (*Casting*).",
            "tarjetas": [
                ("01. Jerarquía de Promoción", "Regla general: `char -> short -> int -> long -> float -> double`.", "Los tipos de menor rango se promocionan automáticamente al tipo de mayor rango sin pérdida de datos."),
                ("02. Conversión con Pérdida (Narrowing)", "Convertir un tipo grande a uno menor (ej. `double -> int` o `int -> char`).", "El compilador debe emitir advertencias de posible pérdida de precisión o truncamiento."),
                ("03. Nodos de Conversión en el AST", "La promoción no es mágica: el compilador inserta un nodo explícito `CAST_TO_FLOAT` en el AST.", "Garantiza que las etapas posteriores de generación de código emitan las instrucciones de conversión correctas.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Representación Binaria y Alineación",
            "descripcion": "Transformación de registros enteros a flotantes:",
            "tarjetas": [
                ("Extensión de Signo vs Cero", "Promocionar un entero con signo (`int8 -> int32`) requiere extender el bit de signo (`movsbl`).", "Promocionar tipos sin signo requiere extensión con ceros (`movzbl`)."),
                ("Registros FPU / SSE", "Los enteros residen en registros de propósito general (RAX); los flotantes requieren registros vectoriales (XMM0).", "La conversión implica mover datos entre bancos de registros de CPU diferentes.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas de Promoción",
            "items": [
                "Promoción de tipos no signados a signados provocando cambios de valores positivos a negativos.",
                "Comparaciones ambiguas `unsigned int < int` donde el entero negativo se promociona a un valor positivo gigante.",
                "Olvidar insertar el nodo de casteo en el AST generando código ensamblador con tipos mezclados incompatibles."
            ]
        }
    },
    9: {
        "tema": "Reporte Formal de Errores Semánticos y Diagnóstico",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Ingeniería de Diagnósticos y Resiliencia del Parser",
            "lead": "Un buen compilador no aborta al primer error; reporta diagnósticos precisos y continúa el análisis para encontrar más fallos.",
            "tarjetas": [
                ("01. Metadatos de Localización", "Cada token y nodo AST debe almacenar su número de línea y columna en el archivo fuente.", "Permite emitir mensajes legibles con contexto visual exacto (`archivo.c:14:5: error: ...`)."),
                ("02. Recuperación Semántica", "Al detectar una incompatibilidad de tipos, el compilador registra el error, asigna un tipo centinela y continúa.", "Evita que un error tipográfico detenga la verificación del resto de las funciones."),
                ("03. Niveles de Diagnóstico", "Clasificación formal en `INFO`, `WARNING`, `ERROR` y `FATAL`.", "Las advertencias no detienen la compilación a menos que se active la bandera `-Werror`.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estructura de la Lista de Diagnósticos",
            "descripcion": "Gestión de un pool de errores desacoplado del AST:",
            "tarjetas": [
                ("Estructura DiagnosticEntry", "Almacena código de error, mensaje formateado, coordenadas `(linea, columna)` y puntero al siguiente error.", "Se acumula en una lista enlazada dinámica en Heap durante todo el análisis semántico."),
                ("Límite de Errores (Error Limit)", "Para evitar saturar la consola con miles de errores en cascada, el compilador aborta al llegar a 20 errores.", "Mantiene la salida legible para el desarrollador.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Manejo de Errores",
            "items": [
                "Uso de `exit(1)` inmediato dentro de una función recursiva, impidiendo liberar la memoria del AST.",
                "Mensajes de error crípticos sin coordenadas de línea ni nombres de identificadores.",
                "Generar código binario corrupto a pesar de haber registrado errores semánticos fatales."
            ]
        }
    },
    10: {
        "tema": "Hito 1: Mini-Evaluador de Expresiones y AST Completo",
        "unidad": "Unidad 1: Análisis Semántico y AST",
        "teoria_principal": {
            "titulo": "Integración del Frontend Semántico del Compilador",
            "lead": "Culminación de la Unidad 1. Conexión completa: Escaneo de tokens, construcción del AST, chequeo estático y reporte de tipos.",
            "tarjetas": [
                ("01. Pipeline del Frontend", "Flujo unificado: `Código Fuente -> Tokens -> AST -> Verificación Semántica -> Evaluación Estática`.", "Base estructural sobre la cual se construirán las siguientes unidades del compilador."),
                ("02. Verificación de Invariantes", "El AST resultante debe ser acíclico, con tipos consistentes en todos sus nodos y sin fugas en Heap.", "Se audita automáticamente mediante la suite completa de pruebas unitarias."),
                ("03. Entrega de Hito 1 (Git Tag)", "Etiquetado formal de versión en el repositorio del estudiante: `git tag v0.1-hito1`.", "Representa el 20% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Validación Integral de Memoria (Valgrind)",
            "descripcion": "Auditoría de integridad total del Frontend Semántico:",
            "tarjetas": [
                ("Cero Fugas (Zero Leaks)", "Toda la memoria reservada para tokens, nodos AST y tablas temporales debe liberarse limpiamente al terminar.", "Condición obligatoria para acreditar el hito de evaluación."),
                ("Pruebas de Estrés", "Evaluación de árboles con más de 100 operadores anidados y combinaciones de tipos mixtos.", "Demuestra la solidez y estabilidad del código desarrollado.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 1",
            "items": [
                "Fallo de segmentación al evaluar expresiones con sintaxis incorrecta o punteros nulos.",
                "Aceptar operaciones ilegales entre tipos incompatibles sin emitir error semántico.",
                "Fugas de memoria detectables al destruir el árbol sintáctico."
            ]
        }
    }
}