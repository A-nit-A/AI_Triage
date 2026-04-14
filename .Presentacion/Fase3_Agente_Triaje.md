# 🤖 Fase 3: Agente de Triaje de Emails
## Cerebro del agente — TechPyme Atención al Cliente

---

En este notebook construimos el **agente completo** que lee correos de clientes, busca en la base de conocimiento RAG y toma decisiones de forma autónoma.

### ¿Qué hace el agente en cada correo?
```
Correo entrante
      │
      ▼
 [Retriever]  →  Busca en ChromaDB los 2 fragmentos más relevantes
      │
      ▼
  [LLM local]  →  Razona con el correo + contexto recuperado
      │
      ├── ¿Respuesta en el contexto? → ✅ Redacta respuesta automática
      │                                             │
      │                                             ▼
      │                                    💾 Guarda en correos_respondidos.csv
      └── ¿No hay info / cliente enfadado? → ⚠️  ESCALAR_A_HUMANO
                                                    │
                                                    ▼
                                           💾 Guarda en correos_escalados.csv
```

### Requisitos previos
- ✅ **Fase 2 completada**: la carpeta `../F2 - RAG/chroma_db` debe existir
- ✅ **Ollama instalado** y ejecutándose en segundo plano
- ✅ **Modelo descargado**: ejecutar `ollama pull llama3` en terminal

---
## Paso 1 — Instalación de librerías adicionales

Necesitamos `langchain-ollama` para conectar con el modelo local.

> ℹ️ Si ya instalaste las librerías en la Fase 2, solo necesitas el paquete nuevo.

---
## Paso 2 — Verificar que Ollama está activo

Antes de continuar, comprobamos que el servidor de Ollama responde correctamente.

---
## Paso 3 — Bandeja de entrada simulada (`correos.json`)

Para no depender de conexiones reales a Gmail/Outlook en clase, simulamos la bandeja de entrada con un archivo JSON.

Incluimos **4 casos de prueba** que cubren todos los escenarios del agente:

| # | Remitente | Escenario esperado |
|---|-----------|--------------------|
| 1 | carlos | Pregunta de envío → respuesta automática |
| 2 | laura | Producto roto + enfadada → escalar |
| 3 | pedro | Soporte externo (Amazon) → escalar |
| 4 | marta | Pregunta de horario → respuesta automática |

---
## Paso 4 — Conectar con la Base de Conocimiento RAG

Cargamos la ChromaDB que creamos en la **Fase 2**. El agente la usará para buscar información relevante antes de responder.

---
## Paso 5 — Despertar la IA local (Ollama + LLaMA3)

Conectamos con el modelo de lenguaje que corre localmente a través de Ollama.

### Parámetros clave:
- **`model="llama3"`**: El modelo a usar (debe estar descargado con `ollama pull llama3`)
- **`temperature=0`**: Sin creatividad — el modelo responde con precisión, sin inventar

---
## Paso 6 — Definir el System Prompt (Las reglas del agente)

El **System Prompt** es el conjunto de instrucciones que define el comportamiento del agente. Es como el "manual de empleado" de la IA.

### Reglas del agente TechPyme:
1. **Solo usa el contexto RAG** para responder — nunca inventa información
2. **Escala a humano** si el cliente está enfadado o el problema es complejo
3. **Escala a humano** si la respuesta no está en el contexto
4. Si puede responder: redacta un correo **amable y profesional**

---
## Paso 7 — Construir la Cadena RAG (El flujo completo del agente)

Unimos todas las piezas en una **cadena de ejecución**:

```
correo  →  [retriever]  →  [prompt + contexto]  →  [LLM]  →  respuesta
```

- `create_stuff_documents_chain`: inyecta los documentos recuperados en el prompt
- `create_retrieval_chain`: orquesta todo el flujo RAG

---
## Paso 8 — 🚀 Ejecutar el Agente de Triaje

El bucle de automatización lee cada correo del JSON, invoca el agente y toma la decisión:
- **✅ Respuesta automática** → la muestra por pantalla
- **⚠️ ESCALAR_A_HUMANO** → lo registra en `correos_escalados.csv`

> ⏳ Puede tardar unos segundos por correo dependiendo del hardware.

---
## Paso 9 — Revisar el registro de correos escalados

---
## 🧪 Bonus — Probar el agente con un correo personalizado

Puedes escribir tu propio correo aquí y ver cómo responde el agente en tiempo real.

---
## 📊 Resumen de la Fase 3

| Paso | Acción | Resultado |
|------|--------|-----------|
| 1 | Instalación `langchain-ollama` | Conector con IA local |
| 2 | Verificación Ollama | Servidor local activo |
| 3 | Carga ChromaDB (Fase 2) | Base de conocimiento conectada |
| 4 | Carga LLaMA3 vía Ollama | Modelo de lenguaje local activo |
| 5 | System Prompt | Reglas del agente definidas |
| 6 | Cadena RAG | Retriever + LLM encadenados |
| 7 | Bucle de triaje | Correos procesados y clasificados |
| 8 | Revisión CSV | Correos escalados registrados |

---

### 🏗️ Arquitectura completa del sistema
```
┌─────────────────────────────────────────────────┐
│              AGENTE DE TRIAJE                   │
│                                                 │
│  correos.json  ──►  RAG Chain  ──►  Decisión    │
│                        │                        │
│              ┌─────────┴─────────┐              │
│         ChromaDB            Ollama/LLaMA3       │
│         (faqs.txt)          (razonamiento)      │
│              └─────────┬─────────┘              │
│                        │                        │
│          ┌─────────────┴────────────┐           │
│    ✅ Respuesta              ⚠️  CSV escalados  │
│       automática              (humano revisa)   │
└─────────────────────────────────────────────────┘
```
