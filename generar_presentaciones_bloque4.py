#!/usr/bin/env python3
"""
Compilador de Presentaciones Enriquecidas (Bloque 4: Sesiones 31 a 40)
Unidad 4: Generación de Código Objeto, Ensamblador y Ejecutable Final
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os

TEORIA_BLOQUE_4 = {
    31: {
        "tema": "Introducción a Ensamblador x86-64 y Arquitectura de CPU",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Mapeo de Código Intermedio a Instrucciones Máquina",
            "lead": "El backend traduce cuádruplos abstractos a instrucciones x86-64 reales que operan sobre registros y memoria.",
            "tarjetas": [
                ("01. Registros de Propósito General", "16 registros de 64 bits (RAX, RBX, RCX, RDX, RSI, RDI, RBP, RSP, R8-R15).", "Permiten realizar operaciones aritméticas a la velocidad del reloj del procesador sin tocar la RAM."),
                ("02. Sintaxis GNU Assembler (AT&T vs Intel)", "AT&T: 'movl %eax, %ebx' (origen -> destino). Intel: 'mov ebx, eax' (destino <- origen).", "GCC utiliza por defecto la convención AT&T con prefijos '%' para registros y '$' para literales."),
                ("03. Instrucciones Aritméticas Básicas", "Traducción de cuádruplos directos: 'addq', 'subq', 'imulq', 'idivq'.", "Operan destructivamente sobre el registro destino: 'addq %rbx, %rax' calcula RAX = RAX + RBX.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Jerarquía de Registros y Sub-Registros",
            "descripcion": "Acceso a partes de 8, 16, 32 y 64 bits del mismo registro físico:",
            "tarjetas": [
                ("Subdivisiones (Ejemplo RAX)", "RAX (64 bits), EAX (32 bits), AX (16 bits), AL/AH (8 bits inferiores/superiores).", "Escribir en un registro de 32 bits (EAX) limpia a ceros automáticamente los 32 bits superiores de RAX."),
                ("Modos de Direccionamiento", "Directo por registro (%rax), Inmediato ($42), y Desplazamiento de memoria (-8(%rbp)).", "Permite leer variables locales ubicadas en la pila con una sola instrucción.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Ensamblador",
            "items": [
                "Mover memoria a memoria directamente ('movq -8(%rbp), -16(%rbp)'), operación ilegal en la arquitectura x86-64.",
                "Confundir sufijos de tamaño ('movb', 'movw', 'movl', 'movq') corrompiendo registros adyacentes.",
                "No extender el signo en divisiones enteras ('cdq' / 'cqo') provocando interrupciones de punto flotante."
            ]
        }
    },
    32: {
        "tema": "Asignación Ingenua de Registros (Naive Allocation)",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Estrategia Cargar-Computar-Almacenar (Load-Op-Store)",
            "lead": "El asignador ingenuo mapea cada temporal a la memoria de pila y utiliza un conjunto mínimo de registros como intermediarios.",
            "tarjetas": [
                ("01. Patrón Load-Op-Store", "Para cada cuádruplo 't2 = t0 + t1': carga t0 en RAX, t1 en RBX, suma y almacena RAX en la dirección de t2.", "Estrategia robusta y sencilla de implementar que no requiere análisis de vida de variables."),
                ("02. Registros de Trabajo Reservados", "Se reservan registros fijos (ej. RAX y RBX para aritmética, R10 y R11 para temporales).", "Evita conflictos de asignación manteniendo un pool constante para todas las operaciones."),
                ("03. Desventaja de Rendimiento", "Genera un tráfico masivo de lecturas y escrituras en el Stack (RAM / Caché L1).", "Compensado por la simplicidad en la generación directa de código.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Tabla de Desplazamientos del Stack Frame",
            "descripcion": "Mapeo estático de variables y temporales a offsets negativos:",
            "tarjetas": [
                ("Offset de Temporales", "Cada '_t0, _t1...' recibe una ranura fija de 8 bytes en la pila: '-8(%rbp), -16(%rbp)...'.", "Calculado consecutivamente durante la fase de análisis de cuádruplos."),
                ("Alineación del Marco", "El tamaño total del marco de pila debe redondearse al múltiplo superior de 16 bytes: 'subq $32, %rsp'.", "Obligatorio según la convención ABI x86-64.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Asignación Ingenua",
            "items": [
                "Superposición de offsets entre variables locales del usuario y temporales generados por el compilador.",
                "Olvidar guardar el resultado del registro de vuelta a la memoria tras la operación.",
                "Agotar el espacio de direccionamiento de 32 bits en funciones con miles de temporales."
            ]
        }
    },
    33: {
        "tema": "Derramamiento a Memoria (Register Spilling)",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Gestión de Presión de Registros y Desalojo",
            "lead": "Cuando el número de variables activas simultáneamente excede los registros físicos disponibles, se deben 'derramar' valores a la pila.",
            "tarjetas": [
                ("01. Presión de Registros (Register Pressure)", "Ocurre en expresiones con muchos operandos concurrentes donde todos los registros de CPU están ocupados.", "El compilador debe seleccionar qué registro desalojar a la pila para liberar espacio."),
                ("02. Criterio de Selección (Heurística de Desalojo)", "Desalojar el temporal cuyo próximo uso esté más lejano en el tiempo.", "Minimiza la penalización de rendimiento de recargar datos desde el Stack."),
                ("03. Instrucciones de Derrame (Spill Code)", "Emisión explícita de 'movq %reg, offset(%rbp)' al desalojar y 'movq offset(%rbp), %reg' al reutilizar.", "Introduce instrucciones adicionales de acceso a memoria para salvar la limitación física.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ranuras de Derrame en el Marco de Pila",
            "descripcion": "Zona reservada en el Stack para variables derramadas:",
            "tarjetas": [
                ("Spill Slots", "Espacio reservado al fondo del stack frame exclusivo para variables que no cupieron en registros.", "Se accede mediante direccionamiento indirecto indexado a RBP."),
                ("Análisis de Vida (Liveness)", "Determina en qué punto una variable muere (no vuelve a leerse), permitiendo reciclar su registro inmediatamente.", "Reduce drásticamente la necesidad de hacer derrame a memoria.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas en Derramamiento",
            "items": [
                "Desalojar un registro que contiene un puntero base activo corrompiendo el marco de pila.",
                "Sobrescribir ranuras de derrame por no calcular correctamente el tamaño del área de spill.",
                "Recargar un registro con el dato incorrecto tras múltiples saltos condicionales."
            ]
        }
    },
    34: {
        "tema": "Marco de Pila (Stack Frame) y Prólogo/Epílogo",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Convención ABI System V x86-64 y Control de Pila",
            "lead": "Cada función debe construir su marco de pila al iniciar (Prólogo) y destruirlo al finalizar (Epílogo).",
            "tarjetas": [
                ("01. Puntero de Base (RBP) y de Pila (RSP)", "RBP marca la base fija del marco actual; RSP marca el límite superior dinámico de la pila.", "Permite acceder a variables locales mediante offsets constantes negativos: '-offset(%rbp)'."),
                ("02. El Prólogo Estándar", "Secuencia obligatoria: 'pushq %rbp', 'movq %rsp, %rbp', 'subq $N, %rsp'.", "Salva el RBP del llamador, establece el nuevo marco y reserva N bytes para variables locales."),
                ("03. El Epílogo Estándar", "Secuencia obligatoria: 'movq %rbp, %rsp', 'popq %rbp', 'ret'. (O equivalentemente: 'leave', 'ret').", "Restaura la pila del llamador y devuelve el control mediante la dirección de retorno en el tope de la pila.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Anatomía del Stack Frame en Memoria",
            "descripcion": "Disposición física de una llamada a función en la pila (crece hacia abajo):",
            "tarjetas": [
                ("Dirección Retorno y RBP Previo", "El 'call' empuja la dirección de retorno de 8 bytes; el prólogo empuja el RBP anterior.", "Garantiza que al hacer 'ret' el procesador sepa exactamente a qué instrucción regresar."),
                ("Alineación a 16 Bytes", "El valor 'N' en 'subq $N, %rsp' debe elegirse de modo que '(N + 8) % 16 == 0'.", "Evita excepciones del procesador en llamadas a bibliotecas externas como 'printf'.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Stack Frames",
            "items": [
                "Desalineación de pila que causa fallos de segmentación dentro de funciones de la biblioteca estándar (libc).",
                "Olvidar salvar registros 'callee-saved' (RBX, R12-R15) si son modificados dentro de la función.",
                "Corrupción de la dirección de retorno por desbordamiento de arreglos locales en el stack."
            ]
        }
    },
    35: {
        "tema": "Paso de Parámetros por Registro y Convención ABI",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Convención de Paso de Argumentos en x86-64",
            "lead": "A diferencia de arquitecturas antiguas de 32 bits, x86-64 pasa los primeros argumentos en registros rápidos en lugar de memoria.",
            "tarjetas": [
                ("01. Los 6 Registros de Argumentos", "Orden estricto para enteros y punteros: 1: RDI, 2: RSI, 3: RDX, 4: RCX, 5: R8, 6: R9.", "El backend debe cargar los parámetros en estos registros antes de emitir la instrucción 'call'."),
                ("02. Parámetros Flotantes (XMM0 a XMM7)", "Los argumentos de tipo 'float' y 'double' se pasan en los primeros 8 registros vectoriales SSE.", "Desacoplados completamente de los registros de propósito general."),
                ("03. Parámetros Excedentes (Stack Overflow)", "Los parámetros a partir del 7mo se empujan al Stack en orden inverso antes del 'call'.", "El llamador es responsable de limpiar estos parámetros de la pila tras el retorno.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Almacenamiento de Parámetros Formales en el Callee",
            "descripcion": "Cómo la función receptora respalda sus argumentos:",
            "tarjetas": [
                ("Copia al Frame Local", "En el prólogo, la función mueve los registros de entrada a su propio stack: 'movq %rdi, -8(%rbp)'.", "Libera los registros RDI, RSI... para que puedan usarse en llamadas internas subsecuentes."),
                ("Registros Caller-Saved vs Callee-Saved", "Caller-saved (RAX, RCX, RDX, RSI, RDI, R8-R11) pueden ser sobrescritos por cualquier 'call'.", "Callee-saved (RBX, RBP, R12-R15) deben preservarse obligatoriamente si se usan.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Paso de Argumentos",
            "items": [
                "Inversión en el orden de asignación de registros (ej. poner arg1 en RSI y arg2 en RDI).",
                "Sobrescribir RDI con el segundo parámetro antes de haber emitido el primero.",
                "No colocar el número de registros flotantes usados en AL antes de llamar a funciones variádicas como 'printf'."
            ]
        }
    },
    36: {
        "tema": "Traducción de Comparaciones y Saltos a Ensamblador",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Instrucciones de Comparación (CMP) y Banderas de CPU",
            "lead": "Las operaciones booleanas y saltos condicionales se implementan mediante la evaluación del registro de banderas EFLAGS.",
            "tarjetas": [
                ("01. Instrucción CMP", "'cmpq %rbx, %rax' realiza internamente una resta sustractiva 'RAX - RBX' sin alterar los operandos.", "Modifica las banderas Zero Flag (ZF), Sign Flag (SF) y Overflow Flag (OF)."),
                ("02. Saltos Condicionales Directos", "'je' (Jump Equal / ZF=1), 'jne' (Jump Not Equal / ZF=0), 'jl' (Jump Less), 'jge' (Jump Greater/Equal).", "Traduce directamente los cuádruplos 'IFFALSE' y 'GOTO' a bifurcaciones nativas del hardware."),
                ("03. Instrucciones SETcc (Booleanos)", "'sete', 'setne', 'setl' escriben un byte (0 o 1) en un registro de 8 bits según las banderas.", "Permite convertir el resultado de una comparación directamente en un entero booleano en memoria.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Mapeo de Estructuras If y Ciclos a Ensamblador",
            "descripcion": "Traducción de etiquetas y bifurcaciones:",
            "tarjetas": [
                ("Emisión de Etiquetas de Ensamblador", "Las etiquetas TAC ('L0', 'L1') se emiten como símbolos globales/locales seguidos de dos puntos: '.L0:'.", "El ensamblador de GNU ('as') resuelve las distancias relativas de salto de 32 bits."),
                ("Salto Incondicional JMP", "El cuádruplo 'GOTO L1' se traduce directamente a 'jmp .L1'.", "Fuerza al contador de programa (RIP) a cargar la nueva dirección de memoria.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas en Saltos Condicionales",
            "items": [
                "Confundir saltos con signo ('jl', 'jg') con saltos sin signo ('jb', 'ja').",
                "Invertir los operandos en CMP provocando que una condición menor (<) se comporte como mayor (>).",
                "Omitir el prefijo de punto ('.L') en etiquetas provocando colisiones con funciones de la biblioteca estándar."
            ]
        }
    },
    37: {
        "tema": "Integración del Pipeline Completo del Compilador",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Conexión Integral: Del Código Fuente al Archivo Ensamblador",
            "lead": "Integración modular de todas las etapas: Scanner -> Parser -> AST -> Semántico -> TAC -> Optimizador -> Emisor ASM.",
            "tarjetas": [
                ("01. Arquitectura en Pases (Multi-Pass Compiler)", "Cada pase consume la estructura de datos del pase anterior y produce una representación más cercana al hardware.", "Garantiza modularidad estricta y aislamiento de fallos."),
                ("02. El Emisor de Ensamblador (Code Generator)", "Recorre la lista de cuádruplos optimizados y emite instrucciones de texto en formato '.s'.", "Escribe la directiva de sección de texto ('.text'), exportación global ('.globl main') y los marcos de función."),
                ("03. Sección de Datos (.data y .rodata)", "Emite literales de cadenas y constantes globales: '.section .rodata', '.string \"Resultado: %d\\n\"'.", "Permite enlazar cadenas de texto usadas por 'printf' o funciones del sistema.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estructura del Archivo Ensamblador Emitido (.s)",
            "descripcion": "Formato estándar para el ensamblador GNU:",
            "tarjetas": [
                ("Encabezado de Sección", "'.text', '.globl main', '.type main, @function'.", "Indica al linker que 'main' es el punto de entrada ejecutable del programa."),
                ("Directivas de Tamaño y Depuración", "'.size main, .-main'.", "Informa al sistema operativo el tamaño exacto del bloque de código binario generado.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en la Integración del Pipeline",
            "items": [
                "Emitir código ensamblador cuando el analizador semántico registró errores fatales previos.",
                "Falta de exportación global ('.globl main') causando errores de símbolo indefinido al enlazar.",
                "Colisión de nombres de variables globales con identificadores de bibliotecas C estándar."
            ]
        }
    },
    38: {
        "tema": "Enlace (Linking) y Creación de Binarios Ejecutables ELF",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Ensamblado con AS y Enlace con GCC / LD",
            "lead": "El archivo ensamblador '.s' se convierte en código máquina reubicable '.o' y finalmente en un ejecutable ELF.",
            "tarjetas": [
                ("01. El Ensamblador (as)", "Traduce las instrucciones mnemónicas ('movq', 'addq') a bytes de código máquina hexadecimales.", "Genera un archivo objeto en formato ELF (Executable and Linkable Format) con símbolos no resueltos."),
                ("02. El Enlazador (Linker / ld)", "Resuelve direcciones de funciones externas ('printf', 'malloc', 'exit') y conecta el código de inicio de C (crt1.o).", "Produce el binario ejecutable final autónomo."),
                ("03. Invocación desde GCC", "El comando 'gcc salida.s -o binario_final' coordina automáticamente el ensamblado y enlace.", "Incluye las rutas de búsqueda de bibliotecas estándar sin necesidad de llamar a 'ld' manualmente.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estructura del Binario ELF en Linux",
            "descripcion": "Segmentos de memoria cargados por el núcleo del sistema operativo:",
            "tarjetas": [
                ("Segmentos ELF", "Segmento de Texto (.text, solo lectura/ejecución), Datos (.data/.rodata, lectura/escritura) y Pila (Stack).", "El cargador de Linux (ELF Loader) mapea estos segmentos en el espacio de direcciones virtuales."),
                ("Código de Salida ($?)", "El valor devuelto por 'main()' en RAX se pasa al sistema operativo como exit code del proceso.", "Verificable en consola mediante 'echo $?'.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en el Enlace",
            "items": [
                "Error 'undefined reference to main': no declarar el punto de entrada global.",
                "Incompatibilidad de arquitectura: intentar compilar código de 32 bits en modo de 64 bits sin banderas multilib.",
                "Permisos de ejecución no asignados en el binario resultante ('chmod +x')."
            ]
        }
    },
    39: {
        "tema": "Auditoría de Rendimiento y Fugas de Memoria en el Compilador",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Perfilado de Rendimiento y Análisis Estático con Valgrind",
            "lead": "Un compilador de calidad industrial debe ser rápido, consumir memoria constante y no sufrir fugas en el Heap.",
            "tarjetas": [
                ("01. Auditoría con Valgrind (Memcheck)", "Herramienta de instrumentación dinámica que detecta lecturas de memoria no inicializada y memory leaks.", "Verifica que cada 'malloc' de tokens, nodos AST y cuádruplos tenga su correspondiente 'free'."),
                ("02. Perfilado de Tiempo de Compilación", "Medición de tiempo consumido en cada pase: frontend, optimización y backend.", "Garantiza que la complejidad global del compilador sea lineal O(n) respecto al tamaño del código fuente."),
                ("03. Pruebas de Estrés Masivas", "Compilación de programas fuente extensos (>1,000 líneas de código con funciones anidadas).", "Comprueba que la memoria del compilador se mantenga acotada y estable.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Patrón Arena Allocator para Compiladores Rápidos",
            "descripcion": "Técnica industrial de asignación en bloque:",
            "tarjetas": [
                ("Asignador de Arena", "En lugar de miles de 'malloc' individuales, se reserva un bloque grande continuo en Heap.", "Al terminar la compilación, se libera toda la arena de un solo golpe, eliminando fugas y acelerando la ejecución."),
                ("Cero Fugas (Zero Leaks)", "El reporte de Valgrind debe certificar: 'All heap blocks were freed -- no leaks are possible'.", "Requisito indispensable para la acreditación técnica final.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Calidad del Compilador",
            "items": [
                "Fugas acumulativas en la tabla de símbolos al compilar múltiples archivos en serie.",
                "Punteros colgantes tras la liberación de cuádruplos optimizados.",
                "Degradación cuadrática O(n^2) en el tiempo de búsqueda de símbolos en tablas de hash mal dimensionadas."
            ]
        }
    },
    40: {
        "tema": "Hito 4: Demostración Final del Compilador End-to-End",
        "unidad": "Unidad 4: Código Objeto y Backend",
        "teoria_principal": {
            "titulo": "Evaluación Integradora y Demostración del Compilador",
            "lead": "Culminación del curso. Demostración práctica de un compilador modular completamente funcional que traduce código de alto nivel a binarios ELF ejecutables.",
            "tarjetas": [
                ("01. Suite de Pruebas de Acreditación", "Batería de 10 programas de prueba completos que evalúan todas las características del lenguaje.", "Abarca: expresiones aritméticas, variables globales/locales, control if/else, ciclos while, funciones recursivas y arreglos."),
                ("02. Reporte Técnico de Arquitectura", "Documento en 'proyecto_integrador/docs/' que detalla las estructuras de datos, gramática, decisiones de diseño y análisis de complejidad.", "Constituye la evidencia formal de ingeniería del estudiante."),
                ("03. Entrega Final y Release en GitHub", "Etiquetado formal de la versión definitiva en el repositorio: 'git tag v1.0-final'.", "Concluye el 30% del Proyecto Integrador y la acreditación final del curso.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Verificación del Binario Resultante",
            "descripcion": "Criterio de éxito: el ejecutable generado produce los resultados correctos de forma nativa:",
            "tarjetas": [
                ("Ejecución Nativa", "'./compilador programa.c -o programa && ./programa'.", "El binario corre directamente en la CPU x86-64 sin intérpretes ni dependencias intermedias."),
                ("Comprobación de Salida", "Los resultados emitidos por el programa generado coinciden exactamente con los oráculos de prueba.", "Certifica la corrección semántica de todo el pipeline del compilador.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Acreditación del Hito 4",
            "items": [
                "El compilador debe compilar y ejecutar exitosamente los 10 programas de prueba sin errores de segmentación.",
                "El código fuente del compilador debe compilar limpiamente con '-Wall -Wextra' sin advertencias.",
                "La bitácora de auditoría y la documentación de arquitectura deben estar completas en GitHub."
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
      <p class="lead">Sesión {n_str} del curso. Generación de código ensamblador x86-64, asignación de registros, stack frames y enlace ELF con la Tríada Metodológica.</p>
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>
          <p>Codificación manual sin IA para comprender los modos de direccionamiento y registros de hardware.</p>
          <div class="card-details">Construcción directa de instrucciones máquina, prólogos y epílogos de funciones.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>
          <p>Especificación de requerimientos C-R-E-O para el backend y convenciones de llamada ABI.</p>
          <div class="card-details">Formalización de alineación de pila a 16 bytes y preservación de registros callee-saved.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>
          <p>Test Harness automatizado con ejecución nativa y verificación de memoria con Valgrind.</p>
          <div class="card-details">Pruebas destructivas sobre desalineación de stack, derramamiento de registros y código de salida ($?).</div>
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
        <strong>Invariante del Backend:</strong> Toda instrucción de alto nivel debe traducirse a una secuencia equivalente y segura de operaciones de hardware.
      </div>
    </section>

    <section class="slide">
      <h2>Arquitectura de Memoria y Hardware: {am["titulo"]}</h2>
      <p class="lead">{am["descripcion"]}</p>
      <div class="grid-2">
        {cards_s3}
      </div>
    </section>

    <section class="slide">
      <h2>{cb["titulo"]}</h2>
      <p class="lead">Puntos críticos de falla que deben protegerse en la generación de ensamblador y auditarse en las respuestas del LLM:</p>
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
            <li><strong>00–20 min:</strong> Fundamento conceptual y arquitectura x86-64.</li>
            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual sin IA).</li>
            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>
            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness y Valgrind).</li>
            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>
          </ul>
          <div class="card-details">Verifica que el binario generado pase todas las pruebas automáticas.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>
          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>
          <div class="card-details">La entrega de la Sesión 40 concluye formalmente el Hito 4 y la acreditación final del curso.</div>
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
    print("🚀 Compilando presentaciones enriquecidas (Bloque 4: Sesiones 31 a 40)...")
    os.makedirs("presentaciones", exist_ok=True)
    for num, data in TEORIA_BLOQUE_4.items():
        n_str = f"{num:02d}"
        html_content = compilar_presentacion_5_slides(num, data)
        out_path = f"presentaciones/sesion{n_str}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  -> Generada: {out_path} (5 slides completos)")
    print("✅ Bloque 4 de presentaciones actualizado con éxito. Las 40 sesiones están completas.")

if __name__ == "__main__":
    main()