# contenido_teorico_bloque2.py
# Base de conocimiento conceptual: Unidad 2 (Sesiones 11 a 20)
# Materia: Lenguajes y Autómatas II (SCD-1016)
# Docente Titular: MCC. Iván Márquez Larios (ijmarquezl)

TEORIA_BLOQUE_2 = {
    11: {
        "tema": "Arquitectura de la Tabla de Símbolos",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Estructuras de Búsqueda y Resolución O(1)",
            "lead": "La tabla de símbolos es el diccionario central del compilador. Asocia identificadores textuales con sus metadatos semánticos durante todo el análisis.",
            "tarjetas": [
                ("01. Tablas Hash con Encadenamiento", "Un arreglo de punteros a listas enlazadas (*buckets*). Una función hash mapea el identificador a un índice.", "Permite inserción y búsqueda en tiempo promedio O(1), resolviendo colisiones por encadenamiento."),
                ("02. Función Hash (djb2 / Murmur)", "Algoritmos de dispersión deterministas que distribuyen uniformemente las cadenas en la tabla.", "Una mala función de hash degrada el rendimiento del compilador de O(1) a O(n)."),
                ("03. Carga Útil del Símbolo", "Almacena el nombre (lexema), categoría (variable, función, tipo), tipo de dato y dirección relativa.", "Sirve como puente de comunicación directo entre el frontend y el backend.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Modelado de Buckets y Nodos de Símbolo",
            "descripcion": "Gestión de memoria dinámica para entradas y colisiones:",
            "tarjetas": [
                ("Estructura SymbolEntry", "Contiene `char *nombre`, `Type *tipo`, `int offset`, `int linea` y un puntero `struct SymbolEntry *sig`.", "Se reserva dinámicamente en Heap cada vez que se procesa una declaración nueva."),
                ("Factor de Carga (Load Factor)", "Relación entre número de símbolos y tamaño de la tabla. Si supera 0.75, requiere rehasheo dinámico.", "Evita listas de colisión excesivamente largas que ralentizan la compilación.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Tablas de Símbolos",
            "items": [
                "Colisiones no resueltas: Sobrescribir una entrada existente al ocurrir una colisión de hash en lugar de encadenar.",
                "Comparación errónea de identificadores: Comparar punteros de memoria (`ptr1 == ptr2`) en lugar del contenido con `strcmp()`.",
                "Punteros colgantes tras rehasheo de tabla."
            ]
        }
    },
    12: {
        "tema": "Atributos de Símbolos y Cálculo de Memoria",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Metadatos Semánticos, Ancho de Tipos y Desplazamientos",
            "lead": "Cada variable declarada debe tener una ubicación relativa calculada en el registro de activación o segmento de datos.",
            "tarjetas": [
                ("01. Ancho de Tipos (Type Width)", "Tamaño en bytes requerido por el tipo de dato: `char: 1`, `short: 2`, `int/float: 4`, `double/ptr: 8`.", "Determina cuánto espacio debe reservar el compilador para cada variable."),
                ("02. Cálculo de Offset (Desplazamiento)", "Distancia en bytes desde la dirección base del marco de pila (`RBP - offset`).", "Las variables locales se acumulan consecutivamente: `offset_actual += ancho_variable`."),
                ("03. Alineación de Memoria (Data Alignment)", "Las CPUs acceden a datos de forma eficiente cuando las direcciones son múltiplos de su tamaño natural (2, 4 u 8 bytes).", "Requiere insertar bytes de relleno (*padding*) entre variables adyacentes.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Alineación y Padding en el Stack Frame",
            "descripcion": "Disposición en el registro de activación de la función:",
            "tarjetas": [
                ("Alineación por Palabras", "Una variable `int` (4 bytes) declarada después de un `char` (1 byte) requiere 3 bytes de padding intermedio.", "Fórmula de alineación: `offset = (offset + align - 1) & ~(align - 1)`."),
                ("Alineación del Stack a 16 Bytes", "La especificación ABI x86-64 System V exige que el Stack Pointer (RSP) esté alineado a 16 bytes antes de un `call`.", "Previene fallos de protección general en instrucciones vectoriales SSE.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Asignación de Memoria",
            "items": [
                "Offsets superpuestos por omitir el tamaño real del tipo de dato previo.",
                "Ignorar el padding de alineación provocando lecturas no alineadas y caídas de rendimiento en CPU.",
                "Desbordamiento de entero en el cálculo del tamaño total de estructuras grandes."
            ]
        }
    },
    13: {
        "tema": "Manejo de Ámbitos (Scope Global vs Local)",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Visibilidad de Identificadores y Ámbitos Anidados",
            "lead": "El alcance léxico determina en qué regiones del código fuente un identificador es accesible.",
            "tarjetas": [
                ("01. Ámbito Léxico Estático", "La visibilidad se resuelve en tiempo de compilación según la estructura de bloques del código.", "Un bloque hijo puede leer identificadores de bloques padre, pero no al revés."),
                ("02. Ocultamiento de Variables (Shadowing)", "Una variable local puede declarar el mismo nombre que una variable de un ámbito exterior.", "La búsqueda de símbolos debe priorizar la declaración más interna y cercana."),
                ("03. Pila de Tablas de Símbolos", "Cada ámbito nuevo (`{ ... }`) crea su propia tabla de símbolos enlazada a la tabla de su ámbito padre.", "Forma un árbol de ámbitos con la tabla global en la raíz.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estructura Enlazada de Scopes (Scope Stack)",
            "descripcion": "Cadena estática de resolución de identificadores:",
            "tarjetas": [
                ("Puntero Padre (Enlace Estático)", "Cada `Scope` contiene su propia tabla hash y un puntero `struct Scope *padre`.", "La búsqueda (`lookup`) revisa el scope actual; si no lo halla, sube recursivamente por `padre`."),
                ("Ciclo de Vida de Scope", "Al entrar a `{`, se ejecuta `push_scope()`; al salir en `}`, se ejecuta `pop_scope()`.", "Garantiza que las variables locales dejen de ser visibles al terminar su bloque.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Gestión de Ámbitos",
            "items": [
                "Búsqueda invertida: Buscar en ámbitos hijos en lugar de subir hacia el ámbito global.",
                "Destruir la tabla local en `pop_scope()` si las fases posteriores de backend aún requieren consultar offsets de variables locales.",
                "Confundir shadowing con redeclaración ilegal en el mismo ámbito."
            ]
        }
    },
    14: {
        "tema": "Declaración vs Uso de Variables",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Invariante de Definición Previa y Control de Redeclaración",
            "lead": "Todo identificador utilizado en una expresión debe haber sido declarado previamente en un ámbito accesible.",
            "tarjetas": [
                ("01. Invariante: Use-Before-Declaration", "El compilador rechaza cualquier lectura o escritura de un símbolo inexistente en la jerarquía de scopes.", "Emite un error fatal: `error: 'x' no ha sido declarada en este ámbito`."),
                ("02. Detección de Redeclaración Ilegal", "Declarar dos variables con el mismo nombre en el *mismo* ámbito exacto es un error semántico.", "La inserción debe verificar primero si el símbolo ya existe exclusivamente en el scope actual."),
                ("03. Estado de Inicialización", "Rastreo de variables utilizadas antes de haber recibido un valor inicial.", "Permite emitir advertencias (*warnings*) de lectura de memoria no inicializada.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Diferenciación entre Inserción y Búsqueda",
            "descripcion": "Dos operaciones fundamentales con semántica distinta:",
            "tarjetas": [
                ("Insertar Símbolo (Scope Actual)", "`insertar(nombre, tipo)` solo consulta el scope actual. Si ya existe, falla con error de redeclaración.", "Si no existe, reserva memoria y lo agrega a la tabla local."),
                ("Resolver Símbolo (Búsqueda Jerárquica)", "`buscar(nombre)` itera desde el scope actual hasta el global.", "Retorna el puntero al `SymbolEntry` más cercano o `NULL` si la variable no existe.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Declaraciones",
            "items": [
                "Permitir que una variable se declare dos veces en la misma función con tipos contradictorios.",
                "Omitir el error cuando una variable se usa dentro de su propia declaración inicial (`int x = x + 1;`).",
                "Falsos positivos de no-declaración al buscar variables globales desde funciones profundas."
            ]
        }
    },
    15: {
        "tema": "Bloques Anidados y Ciclo de Vida de Identificadores",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Gestión Temporal de Bloques y Reutilización de Pila",
            "lead": "Los bloques `{ ... }` crean contextos temporales. Variables en bloques paralelos pueden compartir el mismo espacio de pila.",
            "tarjetas": [
                ("01. Bloques Paralelos", "Dos bloques `{ int a; }` y `{ int b; }` dentro de la misma función nunca están activos al mismo tiempo.", "Un compilador optimizador puede asignar a `a` y a `b` el mismo offset de memoria en el Stack."),
                ("02. Profundidad de Ámbito (Scope Depth)", "Un contador entero que se incrementa en cada nivel de anidamiento.", "Permite determinar rápidamente el nivel de acceso y el ciclo de vida de cada variable."),
                ("03. Preservación para Backend", "Aunque un scope se cierre, la información de sus símbolos debe conservarse en un árbol de scopes para el generador de código.", "Solo se desapila el puntero de búsqueda activa, no se destruyen los metadatos.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Árbol Completo de Scopes (Scope Tree)",
            "descripcion": "Estructura persistente para todo el análisis:",
            "tarjetas": [
                ("Estructura de Árbol", "El scope raíz apunta a sus hijos mediante una lista de sub-scopes: `Scope *primer_hijo, *sig_hermano`.", "Permite al backend recorrer todas las variables de todos los bloques al dimensionar el stack frame."),
                ("Puntero Scope Actual (Cursor)", "Una variable global `Scope *scope_actual` que sube y baja por el árbol de scopes durante el parsing.", "Garantiza contexto correcto en cada nodo procesado.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Bloques Anidados",
            "items": [
                "Acceder a variables locales de un bloque `{ ... }` después de haber cerrado la llave `}`.",
                "Fuga de memoria por no enlazar los scopes hijos al árbol general antes de hacer pop del cursor.",
                "Calcular mal el tamaño total de la función al sumar bloques paralelos en lugar de superponerlos."
            ]
        }
    },
    16: {
        "tema": "Firmas de Función y Parámetros Formales",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Contrato de Invocación, Aridad y Tipado de Argumentos",
            "lead": "Las funciones son símbolos especiales que transportan una lista ordenada de tipos de entrada y un tipo de retorno.",
            "tarjetas": [
                ("01. Aridad (Número de Parámetros)", "La cantidad exacta de argumentos que la función espera recibir en la llamada.", "Llamar a una función con menos o más argumentos de los definidos es un error semántico."),
                ("02. Parámetros Formales como Variables Locales", "Cada parámetro formal se inserta en la tabla de símbolos del cuerpo de la función como una variable local predefinida.", "Tienen offsets específicos asignados según la convención de llamadas de la arquitectura."),
                ("03. Prototipos vs Definición", "Declaración adelantada (*forward declaration*) de la firma antes de la implementación del cuerpo.", "Permite llamadas recursivas y dependencias mutuas entre funciones.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Modelado de Firmas de Función en C",
            "descripcion": "Estructura enlazada de tipos de parámetros:",
            "tarjetas": [
                ("Estructura FunctionSignature", "Contiene `Type *tipo_retorno`, `int num_params` y una lista de `ParamEntry *params`.", "Cada `ParamEntry` tiene el nombre del parámetro y su tipo formal verificado."),
                ("Mapeo a Registros de Argumentos", "En x86-64 System V, los primeros 6 parámetros se pasan en registros: RDI, RSI, RDX, RCX, R8, R9.", "Los parámetros 7 en adelante se apilan en memoria antes del `call`.")
            ]
        },
        "casos_borde": {
            "titulo": "Errores Semánticos en Funciones",
            "items": [
                "Discrepancia de aridad: Invocar una función `suma(int a, int b)` pasando un solo argumento.",
                "Incompatibilidad de tipos en argumentos: Pasar un puntero donde se requiere un entero.",
                "Redefinir una función con una firma incompatible con su prototipo previo."
            ]
        }
    },
    17: {
        "tema": "Comprobación Semántica de Retornos y Rutas de Control",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Validación de Sentencias Return y Análisis de Flujo",
            "lead": "Toda función no-void debe garantizar un retorno de valor válido en todas las posibles rutas de ejecución.",
            "tarjetas": [
                ("01. Coincidencia de Tipo de Retorno", "El tipo de la expresión evaluada en `return expr;` debe coincidir o ser convertible al tipo de la función.", "Un `return` con valor dentro de una función `void` es un error semántico."),
                ("02. Análisis de Retorno en Ramas Condicionales", "Si una función tiene `if-else`, ambas ramas deben retornar un valor; omitir el `else` deja una ruta abierta.", "El compilador debe alertar: `control reaches end of non-void function`."),
                ("03. Sentencias Inalcanzables tras Return", "Cualquier código escrito inmediatamente después de un `return` incondicional en el mismo bloque es código muerto.", "El analizador semántico debe emitir advertencias de código inalcanzable.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ubicación del Valor de Retorno en Hardware",
            "descripcion": "Convención ABI para valores devueltos:",
            "tarjetas": [
                ("Registro RAX / XMM0", "Los enteros y punteros devueltos se cargan en el registro `RAX` (64-bit) o `EAX` (32-bit).", "Los valores de punto flotante (`float`, `double`) se devuelven en el registro vectorial `XMM0`."),
                ("Estructuras Grandes (> 16 bytes)", "Se devuelven mediante un puntero oculto pasado como primer argumento implícito en `RDI`.", "El llamador reserva el espacio en su pila y la función escribe directamente en él.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos Críticos en Sentencias Return",
            "items": [
                "Retornar la dirección de una variable local de pila (`return &local;`), generando punteros colgantes en el llamador.",
                "Rutas de ejecución abiertas en sentencias `switch` sin cláusula `default` retornable.",
                "Retornar valores vacíos `return;` en funciones con tipo de retorno definido como `int`."
            ]
        }
    },
    18: {
        "tema": "Arreglos y Verificación de Límites Estáticos",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Dimensionamiento de Memoria Contigua e Indexación",
            "lead": "Un arreglo es una secuencia homogénea y contigua de elementos en memoria indexada por desplazamientos escalares.",
            "tarjetas": [
                ("01. Cálculo del Tamaño Total", "El tamaño en bytes de un arreglo unidimensional es: $\\text{Bytes} = N \\times \\text{sizeof}(T)$.", "El compilador reserva este bloque continuo en el Stack o segmento de datos."),
                ("02. Indexación y Tipado de Índices", "La expresión dentro de `A[i]` debe evaluarse obligatoriamente a un tipo entero (`int`, `size_t`).", "El compilador rechaza índices de tipo flotante o punteros."),
                ("03. Verificación de Límites Estáticos", "Si el índice es una constante conocida en compilación (`A[15]` en un arreglo de 10 elementos), emitir error estático.", "Previene accesos fuera de límites (*out-of-bounds*) en tiempo de compilación.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Fórmula de Direccionamiento de Arreglos",
            "descripcion": "Cálculo de la dirección efectiva en tiempo de ejecución:",
            "tarjetas": [
                ("Fórmula 1D", "$\\text{Dir}(A[i]) = \\text{Base}(A) + (i \\times \\text{ancho})$.", "En ensamblador x86-64 se traduce directamente al modo de direccionamiento escalado: `[RBP + RAX*4 - offset]`."),
                ("Fórmula 2D (Row-Major Order)", "$\\text{Dir}(A[i][j]) = \\text{Base}(A) + (i \\times \\text{Columnas} + j) \\times \\text{ancho}$.", "C almacena las matrices por filas consecutivas en memoria lineal.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas en Arreglos",
            "items": [
                "Dimensiones no enteras o negativas en la declaración (`int arr[-5];`).",
                "Arreglos de tamaño cero `int arr[0];` en estándares estrictos ANSI C.",
                "Confundir la indexación `arr[i]` con la desreferenciación de punteros no inicializados."
            ]
        }
    },
    19: {
        "tema": "Estructuras (struct) y Offsets de Miembros",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Tipos Compuestos Heterogéneos y Sub-Tablas de Símbolos",
            "lead": "Las estructuras agrupan campos de distintos tipos. Cada `struct` posee su propia tabla de símbolos interna para sus miembros.",
            "tarjetas": [
                ("01. Tabla de Miembros (Member Table)", "Cada definición de estructura contiene una sub-tabla de símbolos con el nombre y offset de cada campo.", "Al evaluar `p.edad`, el compilador consulta la tabla de miembros del tipo de `p`."),
                ("02. Operador de Acceso a Miembro (`.` y `->`)", "El operador `.` accede sobre variables directas; el operador `->` desreferencia primero un puntero a estructura.", "Requiere validar que el operando izquierdo sea efectivamente de tipo `struct`."),
                ("03. Tamaño y Padding Total de Estructura", "El tamaño total de una estructura debe ser múltiplo de la alineación de su miembro más grande.", "Garantiza que en arreglos de estructuras todos los elementos queden correctamente alineados.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Alineación y Disposición de Campos en Memoria",
            "descripcion": "Cálculo paso a paso de offsets y padding interno:",
            "tarjetas": [
                ("Ejemplo de Disposición", "`struct { char a; int b; short c; };` -> `a` en offset 0, 3 bytes padding, `b` en offset 4, `c` en offset 8, 2 bytes padding final. Total: 12 bytes.", "El orden de declaración afecta directamente la memoria consumida."),
                ("Dirección Efectiva del Miembro", "$\\text{Dir}(p.campo) = \\text{Base}(p) + \\text{Offset}(campo)$.", "El compilador emite instrucciones con desplazamiento constante.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Estructuras",
            "items": [
                "Acceso a campos inexistentes (`p.telefono` cuando el campo no fue definido en el struct).",
                "Uso del operador `.` sobre un puntero en lugar de `->` o viceversa.",
                "Estructuras autorreferenciadas sin puntero (`struct Nodo { struct Nodo sig; };`) que generan tipos de tamaño infinito."
            ]
        }
    },
    20: {
        "tema": "Hito 2: Analizador Semántico Completo y Scopes",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Integración del Frontend Semántico Completo",
            "lead": "Culminación de la Unidad 2. El compilador ahora valida completamente tipos, ámbitos, funciones, arreglos y estructuras sin generar código erróneo.",
            "tarjetas": [
                ("01. Validación Semántica Integral", "Todo el código fuente se verifica contra la tabla de símbolos y las reglas de tipo antes de avanzar al código intermedio.", "Cualquier programa inválido es rechazado con mensajes de error precisos."),
                ("02. AST Decorado y Completo", "Cada nodo del AST contiene su tipo verificado, y cada identificador apunta directamente a su `SymbolEntry` con offset resuelto.", "El backend ya no necesita resolver nombres; solo consume desplazamientos y tamaños."),
                ("03. Entrega de Hito 2 (Git Tag)", "Etiquetado formal de versión en GitHub: `git tag v0.2-hito2`.", "Representa el 25% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría de Integridad y Tabla de Símbolos",
            "descripcion": "Verificación del árbol de scopes y cálculo de memoria total:",
            "tarjetas": [
                ("Consistencia de Offsets", "Verificación de que ninguna variable local ni campo de estructura tenga offsets superpuestos en memoria.", "Garantiza que la generación de código x86-64 no corrompa variables adyacentes."),
                ("Batería de Pruebas de Estrés Semántico", "Programas de prueba con funciones mutuamente recursivas, shadowing profundo y estructuras complejas.", "Comprueba la robustez del compilador ante código hostil o ambiguo.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 2",
            "items": [
                "Aceptar variables no declaradas o redeclaraciones en el mismo ámbito sin emitir error.",
                "Fallo de segmentación en la búsqueda de identificadores con shadowing profundo.",
                "Cálculo incorrecto de offsets en estructuras con padding de alineación."
            ]
        }
    }
}