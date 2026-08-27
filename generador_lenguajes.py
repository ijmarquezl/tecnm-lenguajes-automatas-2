import os
import json

MATRIZ_SESIONES = [
    (1, "Encuadre, Diagnóstico de Punteros y Metodología IA", "Inversión de buffer in-place (char*)", "Punteros, O(n) tiempo, O(1) memoria", "Valores NULL, buffers vacios y longitudes impares"),
    (2, "Gestión en GitHub Web y Nodos Dinámicos", "Lista enlazada de tokens en Heap", "Gestión de memoria dinámica C99/Rust", "Prevención de Use-After-Free y cadenas nulas"),
    (3, "Google Colab, Mágicos y Flujo de Entrega", "Manipulación de archivos y llamadas OS", "Salida estándar y códigos de retorno ABI", "Detección de errores de compilación GCC"),
    (4, "Anatomía de un Árbol Sintáctico (AST)", "Estructura de nodo binario (ASTNode)", "Gramática E -> E + T | T con tipos de nodo", "Árbol vacío y evaluación de nodo raíz"),
    (5, "Recorridos del AST y Notación Polaca", "Impresión en Postorden / RPN", "Invariantes de recorrido recursivo", "Validación contra desbordamiento de pila"),
    (6, "Sistema de Tipos Primitivos", "Chequeo de compatibilidad de tipos", "Matriz de compatibilidad estática", "Rechazo de asignaciones incompatibles"),
    (7, "Evaluación de Expresiones Aritméticas", "Evaluador recursivo de operaciones", "Manejo estricto de división entre cero", "Expresiones complejas y división por 0"),
    (8, "Inferencia y Promoción de Tipos", "Reglas de casteo implícito", "Promoción entera y ensanchamiento", "Mezcla de tipos enteros y flotantes"),
    (9, "Reporte Formal de Errores Semánticos", "Diagnóstico con línea y columna", "Estructura estándar de errores GCC", "Múltiples errores sin abortar parser"),
    (10, "Hito 1: Mini-Evaluador de Expresiones", "Integración AST y Tipado Estático", "Contrato formal de Frontend Semántico", "Batería de 10 expresiones mixtas complejas"),
    (11, "Arquitectura de la Tabla de Símbolos", "Tabla Hash con encadenamiento", "Función de dispersión y colisiones O(1)", "Manejo de claves duplicadas y colisiones"),
    (12, "Atributos de Símbolos y Memoria", "Estructura de registro de símbolos", "Cálculo de desplazamientos y alineación", "Alineación de tipos y tamaños en bytes"),
    (13, "Manejo de Ámbitos (Scope Global/Local)", "Pila de tablas de símbolos (Stack Scopes)", "Ocultamiento de variables (Shadowing)", "Búsqueda jerárquica de identificadores"),
    (14, "Declaración vs Uso de Variables", "Detección de variables no declaradas", "Invariante de definición previa", "Uso antes de declarar y redeclaración"),
    (15, "Bloques Anidados y Ciclo de Vida", "Operaciones Push y Pop de ámbito", "Liberación de memoria al cerrar bloque", "Aislamiento de variables fuera de bloque"),
    (16, "Firmas de Función y Parámetros", "Registro de prototipos y aridad", "Coincidencia estricta de parámetros", "Llamadas con número incorrecto de args"),
    (17, "Comprobación Semántica de Retornos", "Validación de tipo de sentencia return", "Rutas de ejecución con retorno garantizado", "Funciones sin retorno o retornos mixtos"),
    (18, "Arreglos y Verificación de Límites", "Cálculo de tamaño de arreglo en memoria", "Indexación entera no negativa", "Límites estáticos y dimensiones inválidas"),
    (19, "Estructuras (struct) y Miembros", "Offsets de miembros en estructuras", "Alineación de memoria por palabras", "Acceso a miembros inexistentes"),
    (20, "Hito 2: Analizador Semántico y Scopes", "Integración de Tabla de Símbolos y AST", "Contrato de Validación Semántica Integral", "Casos complejos de shadowing y ámbito"),
    (21, "Fundamentos de Código de 3 Direcciones", "Representación en Cuádruplos (op,a,b,r)", "Generación de temporales únicos (_t0..)", "Expresiones aritméticas compuestas"),
    (22, "Generación de TAC para Expresiones", "Traductor de nodos AST a TAC", "Conservación de precedencia de operadores", "Expresiones anidadas con paréntesis"),
    (23, "Etiquetas y Saltos Incondicionales", "Generador de etiquetas e instrucciones goto", "Trazabilidad del flujo de control", "Saltos adelante y atrás estructurados"),
    (24, "Control de Flujo: Sentencia if-else", "Saltos condicionales y evaluación booleana", "Cortocircuito lógico en expresiones", "Condiciones compuestas con AND y OR"),
    (25, "Control de Flujo: Bucles while y for", "Estructura de ciclo en instrucciones TAC", "Garantía de actualización de iterador", "Bucles anidados y condiciones de parada"),
    (26, "TAC para Llamadas a Funciones", "Instrucciones param, call y return", "Convención de paso de argumentos TAC", "Llamadas anidadas f(g(x))"),
    (27, "Indexación de Arreglos en TAC", "Cálculo de desplazamientos base + offset", "Aplanado de direcciones unidimensionales", "Arreglos multidimensionales en TAC"),
    (28, "Optimización: Constant Folding", "Plegado y simplificación de constantes", "Reducción estática en compilación", "Simplificación de expresiones constantes"),
    (29, "Optimización: Dead Code Elimination", "Detección de código inalcanzable", "Análisis de flujo tras retornos y gotos", "Eliminación de bloques inalcanzables"),
    (30, "Hito 3: Generador de TAC End-to-End", "Traductor completo de AST a TAC", "Contrato de Emisión Lineal Optimizada", "Suite de 5 programas complejos"),
    (31, "Introducción a Ensamblador x86-64", "Mapeo de TAC a instrucciones mov/add/sub", "Sintaxis estándar de ensamblador GNU", "Ejecución de operaciones aritméticas en CPU"),
    (32, "Asignación Ingenua de Registros", "Asignador directo de temporales a registros", "Uso de registros de propósito general", "Mapeo eficiente de registros RAX, RBX"),
    (33, "Derramamiento a Memoria (Spilling)", "Manejo de pila ante agotamiento de registros", "Instrucciones push/pop hacia stack frame", "Estrés con más de 10 variables activas"),
    (34, "Marco de Pila y Prólogo/Epílogo", "Configuración de punteros RBP y RSP", "Convención de llamada ABI System V", "Preservación de registros Callee-Saved"),
    (35, "Paso de Argumentos por Registro", "Mapeo a registros RDI, RSI, RDX, RCX, R8, R9", "Alineación de pila a 16 bytes", "Funciones con múltiples parámetros"),
    (36, "Traducción de Comparaciones y Saltos", "Instrucciones cmp, jmp y saltos condicionales", "Mapeo de banderas de estado de CPU", "Estructuras if y ciclos en ensamblador"),
    (37, "Integración de Pipeline del Compilador", "Conexión de Frontend, TAC y Backend", "Flujo modular completo sin fisuras", "Compilación de código fuente a ASM"),
    (38, "Enlace y Creación de Binarios ELF", "Llamada a ensamblador as y enlazador gcc", "Generación de binario ejecutable nativo", "Comprobación de código de salida ($?)"),
    (39, "Auditoría de Rendimiento y Memoria", "Inspección de tiempos y fugas de memoria", "Compilador sin memory leaks en Heap", "Compilación de programas largos"),
    (40, "Hito 4: Demostración Final del Compilador", "Compilador Modular Funcional Completo", "Reporte Final de Arquitectura y Pruebas", "Batería de 10 programas completos de prueba")
]

def construir_html(num, tema, artesano, cientifico, auditor):
    n_str = f"{num:02d}"
    lineas = [
        "<!DOCTYPE html>",
        '<html lang="es">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"  <title>Sesión {n_str}: {tema} | Lenguajes y Autómatas II</title>",
        "  <style>",
        "    :root {",
        "      --bg: #f4f8fb; --card-bg: rgba(255, 255, 255, 0.88); --card-bg-hover: rgba(255, 255, 255, 0.98);",
        "      --border: #d0dbe5; --border-focus: #0969da; --accent: #0969da; --accent-green: #1a7f37;",
        "      --accent-silver: #627282; --text: #334155; --text-bright: #0f172a; --font-mono: 'Fira Code', monospace;",
        "    }",
        "    * { box-sizing: border-box; margin: 0; padding: 0; }",
        "    body { background-color: var(--bg); color: var(--text); font-family: -apple-system, sans-serif; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }",
        "    header { padding: 12px 28px; background: rgba(255, 255, 255, 0.85); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }",
        "    .brand { font-weight: 700; color: var(--text-bright); font-size: 0.95rem; }",
        "    .tag { background-color: #ddf4ff; color: var(--accent); padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-family: var(--font-mono); font-weight: 600; }",
        "    main { flex: 1; display: flex; position: relative; overflow: hidden; }",
        "    .slide { position: absolute; inset: 0; padding: 30px 60px; display: flex; flex-direction: column; justify-content: center; opacity: 0; visibility: hidden; transform: translateX(30px); transition: all 0.3s ease; }",
        "    .slide.active { opacity: 1; visibility: visible; transform: translateX(0); }",
        "    h1 { font-size: 2rem; color: var(--text-bright); margin-bottom: 12px; }",
        "    h2 { font-size: 1.5rem; color: var(--text-bright); margin-bottom: 16px; }",
        "    p.lead { font-size: 1.05rem; line-height: 1.5; max-width: 900px; margin-bottom: 18px; color: #475569; }",
        "    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }",
        "    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }",
        "    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 18px; cursor: pointer; transition: all 0.25s ease; }",
        "    .card:hover { background: var(--card-bg-hover); border-color: var(--border-focus); transform: translateY(-2px); }",
        "    .card.expanded { border-color: var(--accent); background: #ffffff; }",
        "    .card-header { font-weight: 600; color: var(--text-bright); margin-bottom: 8px; display: flex; justify-content: space-between; }",
        "    .expand-hint { font-size: 0.75rem; color: var(--accent); font-family: var(--font-mono); }",
        "    .card p, .card li { font-size: 0.88rem; line-height: 1.45; color: var(--text); }",
        "    .card-details { max-height: 0; overflow: hidden; opacity: 0; transition: all 0.3s ease; font-size: 0.82rem; color: #475569; }",
        "    .card.expanded .card-details { max-height: 240px; opacity: 1; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); }",
        "    .interactive-box { margin-top: 18px; padding: 14px 18px; background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 6px; font-family: var(--font-mono); font-size: 0.85rem; }",
        "    footer { padding: 12px 28px; background: rgba(255, 255, 255, 0.85); border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }",
        "    .progress { font-size: 0.85rem; font-family: var(--font-mono); color: var(--accent); font-weight: 600; }",
        "    .controls { display: flex; gap: 10px; }",
        "    button { background: #ffffff; color: var(--text-bright); border: 1px solid var(--border); padding: 7px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; }",
        "    button:hover { background: #f1f5f9; }",
        "    button:disabled { opacity: 0.4; cursor: not-allowed; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <header>",
        "    <div class=\"brand\">TecNM Cancún &bull; SCD-1016</div>",
        f"    <div class=\"tag\">SESIÓN {n_str} / 40 &bull; {tema}</div>",
        "  </header>",
        "  <main>",
        '    <section class="slide active">',
        '      <div class="tag" style="width: fit-content; margin-bottom: 10px;">LENGUAJES Y AUTÓMATAS II</div>',
        f"      <h1>{tema}</h1>",
        f"      <p class=\"lead\">Sesión {n_str} del curso. Aplicación del protocolo de compiladores con la Tríada Metodológica.</p>",
        '      <div class="grid-3">',
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Codificación manual sin IA: <strong>{artesano}</strong>.</p>",
        '          <div class="card-details">Desarrolla la intuición técnica de bajo nivel y comprende el comportamiento de memoria antes de consultar modelos.</div>',
        "        </div>",
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Especificación C-R-E-O: <strong>{cientifico}</strong>.</p>",
        '          <div class="card-details">Define el contrato formal de pre/postcondiciones y estructura el prompt técnico para el LLM.</div>',
        "        </div>",
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Test Harness Automatizado: <strong>{auditor}</strong>.</p>",
        '          <div class="card-details">Somete la solución generada por la IA a pruebas destructivas y registra la auditoría crítica en GitHub.</div>',
        "        </div>",
        "      </div>",
        "    </section>",
        '    <section class="slide">',
        "      <h2>Dinámica de la Sesión y Entregables</h2>",
        '      <div class="grid-2">',
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span>Estructura de la Clase (60 min)</span><span class="expand-hint">[+]</span></div>',
        "          <ul>",
        "            <li><strong>00–20 min:</strong> Fundamento conceptual y casos de borde.</li>",
        "            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual).</li>",
        "            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>",
        "            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness).</li>",
        "            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>",
        "          </ul>",
        '          <div class="card-details">Asegúrate de ejecutar todas las pruebas unitarias antes de guardar tu bitácora.</div>',
        "        </div>",
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico de pruebas.</p>",
        '          <div class="card-details">El progreso acumulado cuenta para el 40% de laboratorios y alimenta tu Proyecto Integrador.</div>',
        "        </div>",
        "      </div>",
        '      <div class="interactive-box">',
        '        <strong>Docente Titular:</strong> MCC. Iván Márquez Larios (<code>ijmarquezl</code>) &bull; TecNM Cancún',
        "      </div>",
        "    </section>",
        "  </main>",
        "  <footer>",
        '    <div class="progress" id="slideIndicator">SLIDE 1 / 2</div>',
        '    <div class="controls">',
        '      <button id="prevBtn" onclick="prevSlide()" disabled>&larr; Anterior</button>',
        '      <button id="nextBtn" onclick="nextSlide()">Siguiente &rarr;</button>',
        "    </div>",
        "  </footer>",
        "  <script>",
        "    let currentSlide = 0;",
        "    const slides = document.querySelectorAll('.slide');",
        "    const indicator = document.getElementById('slideIndicator');",
        "    const prevBtn = document.getElementById('prevBtn');",
        "    const nextBtn = document.getElementById('nextBtn');",
        "    function updateSlides() {",
        "      slides.forEach((slide, index) => slide.classList.toggle('active', index === currentSlide));",
        "      indicator.textContent = `SLIDE ${currentSlide + 1} / ${slides.length}`;",
        "      prevBtn.disabled = currentSlide === 0;",
        "      nextBtn.disabled = currentSlide === slides.length - 1;",
        "    }",
        "    function nextSlide() { if (currentSlide < slides.length - 1) { currentSlide++; updateSlides(); } }",
        "    function prevSlide() { if (currentSlide > 0) { currentSlide--; updateSlides(); } }",
        "    function toggleCard(card) {",
        "      card.classList.toggle('expanded');",
        "      const hint = card.querySelector('.expand-hint');",
        "      if (hint) hint.textContent = card.classList.contains('expanded') ? '[-]' : '[+]';",
        "    }",
        "    document.addEventListener('keydown', (e) => {",
        "      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();",
        "      if (e.key === 'ArrowLeft') prevSlide();",
        "    });",
        "  </script>",
        "</body>",
        "</html>"
    ]
    return "\n".join(lineas)

def construir_ipynb(num, tema, artesano, cientifico, auditor):
    n_str = f"{num:02d}"
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# Lenguajes y Autómatas II (SCD-1016)\n",
                    f"## Sesión {n_str}: {tema}\n",
                    f"**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)\n",
                    f"**Repositorio Maestro:** `https://github.com/ijmarquezl/tecnm-lenguajes-automatas-2`\n",
                    f"\n---\n",
                    f"### Protocolo de la Sesión\n",
                    f"1. **Fase 1 (El Artesano):** Resolver a mano: *{artesano}*.\n",
                    f"2. **Fase 2 (El Científico):** Definir contrato C-R-E-O: *{cientifico}* y formular prompt.\n",
                    f"3. **Fase 3 (El Auditor):** Someter la solución al Test Harness: *{auditor}*.\n",
                    f"4. **Entrega:** Documentar en `auditorias/auditoria_sesion{n_str}.md`."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["### Paso 0: Inicialización del Entorno (C y Rust)"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "if os.system('which rustc > /dev/null 2>&1') != 0:\n",
                    "    print('⏳ Instalando Rust en Colab...')\n",
                    "    !apt-get update -qq && apt-get install -y -qq rustc > /dev/null 2>&1\n",
                    "print('✅ Entorno listo:')\n",
                    "!gcc --version | head -n 1\n",
                    "!rustc --version"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"---\n",
                    f"## SECCIÓN A: TRACK C\n",
                    f"### Fase 1: El Artesano (15 min - Sin IA)\n",
                    f"**Reto:** {artesano}"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"%%writefile artesano_sesion{n_str}_c.c\n",
                    "#include <stdio.h>\n",
                    "#include <stdlib.h>\n",
                    "\n",
                    "// TODO: Implementación manual\n",
                    "int main() {\n",
                    f"    printf(\"[SESION {n_str}] Reto Artesano: {artesano}\\n\");\n",
                    "    return 0;\n",
                    "}\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [f"!gcc -Wall -Wextra artesano_sesion{n_str}_c.c -o bin_c && ./bin_c"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"### Fase 2: El Científico (Prompting C-R-E-O)\n",
                    f"Pega aquí la implementación optimizada propuesta por la IA:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"%%writefile ia_sesion{n_str}_c.c\n",
                    "#include <stdio.h>\n",
                    "\n",
                    "// Pega aquí el código generado por la IA para auditarlo\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"### Fase 3: El Auditor (Test Harness en C)\n",
                    f"Pruebas de estrés: {auditor}"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"%%writefile harness_sesion{n_str}_c.c\n",
                    "#include <stdio.h>\n",
                    "#include <assert.h>\n",
                    "\n",
                    "int main() {\n",
                    f"    printf(\"=== AUDITORIA CRITICA: SESION {n_str} ===\\n\");\n",
                    "    printf(\"Ejecutando pruebas de estres... PASO ✅\\n\");\n",
                    "    return 0;\n",
                    "}\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [f"!gcc -Wall -Wextra harness_sesion{n_str}_c.c -o test_bin && ./test_bin"]
            }
        ],
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 2
    }
    return json.dumps(nb, indent=2, ensure_ascii=False)

def construir_md(num, tema, artesano, cientifico, auditor):
    n_str = f"{num:02d}"
    lineas = [
        f"# Bitácora de Requerimientos y Auditoría IA — Sesión {n_str}",
        "**Materia:** Lenguajes y Autómatas II (SCD-1016)  ",
        f"**Tema:** {tema}  ",
        "**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  ",
        "**Estudiante:** [Nombre Completo]  ",
        "**Matrícula:** [No. de Control]  ",
        "**Track:** [ C | Rust ]  ",
        "",
        "---",
        "",
        "## 1. Fase 1: El Artesano (Dificultad Manual)",
        f"*Reto:* {artesano}  ",
        "*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*",
        "> ",
        "",
        "---",
        "",
        "## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)",
        "",
        "### 2.1 Matriz de Especificación Formal",
        "| Elemento C-R-E-O | Definición Técnica |",
        "| :--- | :--- |",
        "| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |",
        "| **Rol (R)** | Ingeniero de software de sistemas y compiladores |",
        f"| **Especificación (E)** | {cientifico} |",
        "| **Output (O)** | Solo código modular y análisis de complejidad |",
        "",
        "### 2.2 Prompt Estructurado",
        "```text",
        "[Pega aquí el prompt formal que redactaste para la IA]",
        "```",
        "",
        "---",
        "",
        "## 3. Código Devuelto por el Modelo",
        "```c",
        "// Código devuelto por el LLM",
        "```",
        "",
        "---",
        "",
        "## 4. Fase 3: El Auditor (Resultados del Test Harness)",
        f"*Pruebas ejecutadas:* {auditor}",
        "",
        "* [ ] Caso base y límites superados sin *Crash*.",
        "* [ ] No existen accesos fuera de límites ni *Memory Leaks*.",
        "* [ ] La complejidad teórica coincide con la implementada.",
        "",
        "### Reporte Crítico",
        "*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*",
        "> ",
        "",
        "---",
        "**Firma digital:** [Usuario de GitHub]"
    ]
    return "\n".join(lineas)

def main():
    print("🚀 Generando estructura completa del curso Lenguajes y Autómatas II...")
    os.makedirs("presentaciones", exist_ok=True)
    os.makedirs("plantillas", exist_ok=True)
    os.makedirs("auditorias", exist_ok=True)
    os.makedirs("proyecto_integrador/docs", exist_ok=True)
    os.makedirs("proyecto_integrador/src", exist_ok=True)
    os.makedirs("proyecto_integrador/tests", exist_ok=True)

    readme_rows = []

    for num, tema, artesano, cientifico, auditor in MATRIZ_SESIONES:
        n_str = f"{num:02d}"
        lab_dir = f"laboratorios/sesion{n_str}"
        os.makedirs(lab_dir, exist_ok=True)

        html_path = f"presentaciones/sesion{n_str}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(construir_html(num, tema, artesano, cientifico, auditor))

        ipynb_path = f"{lab_dir}/sesion{n_str}_laboratorio.ipynb"
        with open(ipynb_path, "w", encoding="utf-8") as f:
            f.write(construir_ipynb(num, tema, artesano, cientifico, auditor))

        md_path = f"plantillas/auditoria_sesion{n_str}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(construir_md(num, tema, artesano, cientifico, auditor))

        colab_badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/{ipynb_path})"
        slides_link = f"[Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/{html_path})"
        readme_rows.append(f"| **Sesión {n_str}** | {tema} | {slides_link} | {colab_badge} |")

    encabezado_readme = [
        "# Lenguajes y Autómatas II (SCD-1016)",
        "",
        "Repositorio oficial del curso de **Lenguajes y Autómatas II** del Tecnológico Nacional de México / Instituto Tecnológico de Cancún.",
        "",
        "**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)",
        "",
        "---",
        "",
        "## 🚀 Flujo de Trabajo en la Nube (100% en Navegador)",
        "1. Realiza un **Fork** de este repositorio a tu cuenta personal de GitHub.",
        "2. Abre la sesión correspondiente con el botón **Open in Colab**.",
        "3. Sigue el ciclo **El Artesano** $\\to$ **El Científico** $\\to$ **El Auditor**.",
        "4. Copia la plantilla de `plantillas/auditoria_sesionXX.md` a `auditorias/auditoria_sesionXX.md` en tu Fork y realiza el commit.",
        "",
        "---",
        "",
        "## 🏗️ Proyecto Integrador Semestral (30%)",
        "* **Hito 1 (Sesión 10):** Mini-Evaluador y Frontend Semántico (AST + Tipos).",
        "* **Hito 2 (Sesión 20):** Tabla de Símbolos Jerárquica y Gestión de Scopes.",
        "* **Hito 3 (Sesión 30):** Generador de Código de Tres Direcciones (TAC) Optimizado.",
        "* **Hito 4 (Sesión 40):** Backend, Generación de Ensamblador y Binario ELF Final.",
        "",
        "---",
        "",
        "## 📚 Índice General de las 40 Sesiones",
        "",
        "| Sesión | Tema Principal | Presentación | Laboratorio |",
        "| :--- | :--- | :---: | :---: |"
    ]

    pie_readme = [
        "",
        "---",
        "",
        "## 📋 Criterios de Evaluación",
        "* **40% Laboratorios Diarios:** Cuadernos Colab y bitácoras en GitHub.",
        "* **30% Proyecto Integrador:** Compilador modular funcional (4 hitos).",
        "* **20% Evaluaciones Prácticas:** 4 hitos prácticos de unidad.",
        "* **10% Participación Activa:** Sesiones síncronas en MS Teams.",
        "",
        "---",
        "**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  ",
        "**Tecnológico Nacional de México — Campus Cancún**"
    ]

    readme_final = "\n".join(encabezado_readme + readme_rows + pie_readme)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_final)

    print("✅ Generación completa exitosa: 40 HTMLs, 40 IPYNBs, 40 MDs y README.md listos.")

if __name__ == "__main__":
    main()