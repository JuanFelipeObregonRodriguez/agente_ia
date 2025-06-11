# 🤖 Agente IA Open Source

Un asistente de inteligencia artificial completamente local y open source que funciona con modelos Ollama. Este agente puede realizar búsquedas web, ejecutar código Python, manejar archivos, hacer cálculos y mucho más, todo desde tu computadora sin depender de servicios externos.

## ✨ Características

- **🔒 100% Local**: Funciona completamente offline usando Ollama
- **🌐 Búsqueda Web**: Integración con DuckDuckGo para información actualizada
- **🧮 Calculadora Avanzada**: Operaciones matemáticas complejas
- **📁 Gestión de Archivos**: Crear, leer, editar y eliminar archivos
- **🐍 Ejecución de Python**: Ejecuta código Python de forma segura
- **🌦️ Información del Clima**: Consulta el clima actual
- **💻 Info del Sistema**: Obtén detalles de tu sistema operativo
- **📝 Historial de Conversación**: Guarda y exporta tus conversaciones
- **🎨 Interfaz Mejorada**: Output visual con colores y formato (Rich)

## 🛠️ Instalación

### Prerrequisitos

1. **Python 3.8+**
2. **Ollama** instalado y funcionando

### Instalar Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Descarga desde [ollama.com](https://ollama.com) e instala el ejecutable.

### Instalar Dependencias de Python

```bash
pip install requests beautifulsoup4 duckduckgo-search rich psutil
```

### Descargar un Modelo

```bash
# Modelo recomendado (ligero y eficiente)
ollama pull llama3.2

# Alternativas más potentes
ollama pull llama3.1
ollama pull codellama
ollama pull mistral
```

## 🚀 Uso

### Modo Interactivo

```bash
python agente_ia.py
```

### Consulta Única

```bash
python agente_ia.py --query "¿Cuál es la capital de Francia?"
```

### Opciones Avanzadas

```bash
# Usar un modelo específico
python agente_ia.py --model llama3.1

# Modo verbose para debugging
python agente_ia.py --verbose

# Ayuda completa
python agente_ia.py --help
```

## 🔧 Herramientas Disponibles

### 🌐 Búsqueda Web
```
"Busca información sobre inteligencia artificial 2025"
"¿Cuáles son las últimas noticias de tecnología?"
```

### 🧮 Calculadora
```
"Calcula la raíz cuadrada de 144"
"¿Cuánto es 15 * 23 + 47?"
"Resuelve (25 + 30) / 5"
```

### 📁 Gestión de Archivos
```
"Lista los archivos en el directorio"
"Crea un archivo llamado notas.txt con mi lista de tareas"
"Lee el contenido del archivo datos.json"
"Elimina el archivo temporal.txt"
```

### 🐍 Código Python
```
"Ejecuta este código: print('Hola mundo')"
"Calcula los primeros 10 números de Fibonacci"
"Genera una lista de números pares del 1 al 20"
```

### 🌦️ Clima
```
"¿Cómo está el clima?"
"Clima en Madrid"
"Temperatura en Nueva York"
```

### ⏰ Fecha y Hora
```
"¿Qué hora es?"
"¿Qué día de la semana es hoy?"
"Dame la fecha completa"
```

### 💻 Información del Sistema
```
"Muestra información de mi sistema"
"¿Cuánta RAM tengo?"
"¿Qué sistema operativo uso?"
```

## 📋 Comandos Especiales

- `quit` / `exit` - Salir del agente
- `save` - Guardar la conversación actual
- `help` - Mostrar ayuda
- `clear` - Limpiar la pantalla

## 📁 Estructura del Proyecto

```
agente-ia/
├── agente_ia.py          # Archivo principal
├── agente_workspace/     # Directorio de trabajo (se crea automáticamente)
├── README.md            # Este archivo
└── requirements.txt     # Dependencias (opcional)
```

## 🔒 Seguridad

El agente implementa múltiples medidas de seguridad:

- **Sandbox de Python**: Ejecución limitada de código con namespace restringido
- **Validación de Archivos**: Solo maneja tipos de archivo seguros
- **Directorio Aislado**: Todas las operaciones de archivo se realizan en `agente_workspace/`
- **Filtrado de Código**: Bloquea importaciones y operaciones peligrosas

## 🎯 Ejemplos Prácticos

### Análisis de Datos
```
Usuario: "Crea un archivo CSV con datos de ventas y luego analízalos"
```

### Investigación Web
```
Usuario: "Busca información sobre el cambio climático y crea un resumen"
```

### Automatización
```
Usuario: "Crea un script que calcule el factorial de un número"
```

### Productividad
```
Usuario: "¿Qué clima hace hoy y cuáles son las noticias importantes?"
```

## 🔧 Configuración Avanzada

### Cambiar el Modelo por Defecto

Edita la línea en `agente_ia.py`:
```python
def __init__(self, model_name="tu_modelo_preferido", verbose=True):
```

### Personalizar Herramientas

Agrega nuevas herramientas en el diccionario `self.tools`:
```python
self.tools = {
    # ... herramientas existentes
    "mi_herramienta": self.mi_funcion_personalizada
}
```

## 🐛 Solución de Problemas

### Ollama No Responde
```bash
# Verificar que Ollama esté funcionando
ollama list

# Reiniciar Ollama si es necesario
ollama serve
```

### Modelo No Encontrado
```bash
# Listar modelos disponibles
ollama list

# Descargar el modelo necesario
ollama pull llama3.2
```

### Error de Conexión Web
- Verifica tu conexión a internet
- Las funciones offline seguirán funcionando

### Problemas de Permisos
```bash
# Asegurar permisos en el directorio
chmod 755 agente_workspace/
```

## 📊 Rendimiento

### Modelos Recomendados por Uso

| Modelo | Tamaño | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----------|---------|-----------------|
| llama3.2 | ~2GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Uso general |
| llama3.1 | ~4GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tareas complejas |
| codellama | ~3GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Programación |
| mistral | ~4GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Análisis profundo |

## 🤝 Contribuir

¿Quieres mejorar el agente? ¡Las contribuciones son bienvenidas!

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-herramienta`)
3. Commit tus cambios (`git commit -am 'Agrega nueva herramienta X'`)
4. Push a la rama (`git push origin feature/nueva-herramienta`)
5. Abre un Pull Request

### Ideas para Contribuir

- 🔧 Nuevas herramientas (base de datos, APIs, etc.)
- 🎨 Mejoras en la interfaz
- 🔒 Funciones de seguridad adicionales
- 📱 Soporte para más plataformas
- 🌍 Internacionalización

## 📜 Licencia

Este proyecto es de código abierto. Siéntete libre de usar, modificar y distribuir según tus necesidades.

## 🙏 Agradecimientos

- **Ollama** - Por hacer los LLMs locales accesibles
- **DuckDuckGo** - Por la API de búsqueda gratuita
- **Rich** - Por la hermosa interfaz de terminal
- **Comunidad Open Source** - Por las herramientas y librerías

## 📞 Soporte

¿Necesitas ayuda?

- 🐛 **Reportar bugs**: Abre un issue en GitHub
- 💡 **Sugerencias**: Comparte tus ideas en las discusiones
- 📖 **Documentación**: Consulta este README
- 🤖 **Prueba el agente**: `python agente_ia.py --query "ayuda"`

---

**¿Te gusta este proyecto? ⭐ Dale una estrella en GitHub y compártelo con otros desarrolladores!**

---

*Última actualización: Junio 2025*