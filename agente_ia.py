# Agente de IA Open Source - Versión Optimizada
# Autor: Tu nombre
# Fecha: 2025
# Requiere: pip install requests beautifulsoup4 duckduckgo-search rich

import json
import re
import requests
from duckduckgo_search import DDGS
from datetime import datetime
import subprocess
import os
import sys
import traceback
from pathlib import Path

# Opcional: para mejor output visual
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

class OpenSourceAgent:
    def __init__(self, model_name="llama3.2", verbose=True):
        """
        Agente de IA completamente open source - Versión Optimizada
        
        Args:
            model_name: Modelo de Ollama a usar
            verbose: Mostrar información detallada
        """
        self.model_name = model_name
        self.verbose = verbose
        self.conversation_history = []
        self.tools = {
            "web_search": self.web_search,
            "calculator": self.calculator,
            "file_operations": self.file_operations,
            "python_code": self.execute_python,
            "get_time": self.get_time,
            "system_info": self.get_system_info,
            "weather": self.get_weather
        }
        
        # Configuración de directorios
        self.work_dir = Path("agente_workspace")
        self.work_dir.mkdir(exist_ok=True)
        
        # Verificar instalación
        self.setup_check()
    
    def print_message(self, message, style="info"):
        """Imprime mensajes con estilo si Rich está disponible"""
        if RICH_AVAILABLE and console:
            if style == "success":
                console.print(f"✅ {message}", style="green")
            elif style == "error":
                console.print(f"❌ {message}", style="red")
            elif style == "warning":
                console.print(f"⚠️  {message}", style="yellow")
            elif style == "info":
                console.print(f"ℹ️  {message}", style="blue")
            else:
                console.print(message)
        else:
            print(f"{message}")
    
    def setup_check(self):
        """Verificación completa del sistema"""
        self.print_message("Iniciando verificación del sistema...", "info")
        
        # Verificar Ollama
        if not self.check_ollama():
            self.print_message("Ollama no está configurado correctamente", "error")
            sys.exit(1)
        
        # Verificar modelo
        if not self.check_model():
            self.print_message(f"El modelo {self.model_name} no está disponible", "warning")
            self.suggest_models()
        
        # Verificar conexión a internet
        if self.check_internet():
            self.print_message("Conexión a internet: OK", "success")
        else:
            self.print_message("Sin conexión a internet - funciones web limitadas", "warning")
        
        self.print_message("Sistema listo para usar", "success")
    
    def check_ollama(self):
        """Verifica si Ollama está instalado y funcionando"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                 capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def check_model(self):
        """Verifica si el modelo especificado está disponible"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                 capture_output=True, text=True, timeout=10)
            return self.model_name in result.stdout
        except:
            return False
    
    def suggest_models(self):
        """Sugiere modelos disponibles o cómo instalarlos"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                 capture_output=True, text=True, timeout=10)
            available_models = [line.split()[0] for line in result.stdout.split('\n')[1:] if line.strip()]
            
            if available_models:
                self.print_message(f"Modelos disponibles: {', '.join(available_models)}", "info")
                if available_models:
                    self.model_name = available_models[0]
                    self.print_message(f"Usando modelo: {self.model_name}", "info")
            else:
                self.print_message("No hay modelos instalados. Ejecuta: ollama pull llama3.2", "warning")
        except:
            pass
    
    def check_internet(self):
        """Verifica conexión a internet"""
        try:
            requests.get("https://httpbin.org/get", timeout=5)
            return True
        except:
            return False
    
    def call_ollama(self, prompt, system_prompt=None, max_retries=3):
        """Llama al modelo local usando Ollama con reintentos"""
        for attempt in range(max_retries):
            try:
                # Construir el prompt completo
                if system_prompt:
                    full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
                else:
                    full_prompt = prompt
                
                # Mostrar progreso si Rich está disponible
                if RICH_AVAILABLE and console:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                        transient=True,
                    ) as progress:
                        task = progress.add_task(description="Pensando...", total=None)
                        
                        # Llamar a Ollama
                        cmd = ['ollama', 'run', self.model_name, full_prompt]
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                else:
                    print("🤖 Pensando...", end='', flush=True)
                    cmd = ['ollama', 'run', self.model_name, full_prompt]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                    print("\r", end='')
                
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    self.print_message(f"Error en intento {attempt + 1}: {result.stderr}", "warning")
                    
            except subprocess.TimeoutExpired:
                self.print_message(f"Timeout en intento {attempt + 1}", "warning")
            except Exception as e:
                self.print_message(f"Error en intento {attempt + 1}: {str(e)}", "warning")
        
        return "Error: No se pudo obtener respuesta después de varios intentos"
    
    def web_search(self, query, max_results=5):
        """Búsqueda web optimizada usando DuckDuckGo - Devuelve información directa"""
        try:
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        'title': r['title'],
                        'body': r['body'][:400] + '...' if len(r['body']) > 400 else r['body'],
                        'url': r['href']
                    })
                
                if results:
                    # Formatear resultados de manera más legible
                    formatted_results = f"🔍 BÚSQUEDA: {query}\n" + "="*50 + "\n"
                    
                    for i, result in enumerate(results, 1):
                        formatted_results += f"\n📄 RESULTADO {i}:\n"
                        formatted_results += f"🔗 Título: {result['title']}\n"
                        formatted_results += f"📝 Contenido: {result['body']}\n"
                        formatted_results += f"🌐 URL: {result['url']}\n"
                        formatted_results += "-" * 30 + "\n"
                    
                    return formatted_results
                else:
                    return f"❌ No se encontraron resultados para: {query}"
                    
        except Exception as e:
            return f"❌ Error en búsqueda web: {str(e)}"
    
    def calculator(self, expression):
        """Calculadora avanzada con más funciones"""
        try:
            # Limpieza y validación
            expression = expression.replace(' ', '')
            allowed_chars = set('0123456789+-*/.()^%')
            if not all(c in allowed_chars for c in expression):
                return "Error: Solo se permiten operaciones matemáticas básicas"
            
            # Reemplazar ^ con **
            expression = expression.replace('^', '**')
            
            # Evaluación segura
            result = eval(expression, {"__builtins__": {}}, {})
            return f"🧮 CÁLCULO: {expression.replace('**', '^')}\n✅ Resultado: {result}"
            
        except ZeroDivisionError:
            return "❌ Error: División por cero"
        except Exception as e:
            return f"❌ Error en cálculo: {str(e)}"
    
    def file_operations(self, operation, filename=None, content=None):
        """Operaciones de archivos mejoradas"""
        try:
            work_path = self.work_dir / (filename or "")
            
            if operation == "list":
                files = list(self.work_dir.iterdir())
                file_info = []
                for f in files[:20]:  # Limitar a 20 archivos
                    if f.is_file():
                        size = f.stat().st_size
                        file_info.append(f"📄 {f.name} ({size} bytes)")
                return f"📁 ARCHIVOS EN {self.work_dir}:\n" + "\n".join(file_info)
            
            elif operation == "read" and filename:
                if work_path.exists() and work_path.suffix in ['.txt', '.md', '.py', '.json', '.csv']:
                    content = work_path.read_text(encoding='utf-8')[:2000]  # Limitar contenido
                    return f"📖 CONTENIDO DE {filename}:\n" + "="*30 + f"\n{content}"
                return f"❌ Archivo {filename} no encontrado o tipo no permitido"
            
            elif operation == "write" and filename and content:
                work_path.write_text(content, encoding='utf-8')
                return f"✅ Archivo {filename} creado exitosamente en {work_path}"
            
            elif operation == "delete" and filename:
                if work_path.exists():
                    work_path.unlink()
                    return f"🗑️ Archivo {filename} eliminado exitosamente"
                return f"❌ Archivo {filename} no encontrado"
            
            return "❌ Operación no válida. Usa: list, read, write, delete"
            
        except Exception as e:
            return f"❌ Error en operación de archivo: {str(e)}"
    
    def execute_python(self, code):
        """Ejecuta código Python con mayor seguridad"""
        # Validaciones de seguridad
        dangerous_keywords = [
            'import os', 'import sys', 'import subprocess', 'exec', 'eval', 
            '__import__', 'open(', 'file(', 'input(', 'raw_input'
        ]
        
        if any(keyword in code for keyword in dangerous_keywords):
            return "❌ Error: Código no permitido por seguridad"
        
        try:
            # Crear namespace limitado
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'sorted': sorted,
                    'abs': abs,
                    'round': round,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple
                }
            }
            
            # Capturar output
            import io
            from contextlib import redirect_stdout
            
            output = io.StringIO()
            with redirect_stdout(output):
                exec(code, safe_globals)
            
            result = output.getvalue()
            return f"🐍 CÓDIGO PYTHON EJECUTADO:\n" + "="*30 + f"\n{code}\n" + "="*30 + f"\n📋 RESULTADO:\n{result}" if result else f"✅ Código ejecutado correctamente (sin output visible)"
            
        except Exception as e:
            return f"❌ Error al ejecutar código Python: {str(e)}"
    
    def get_time(self):
        """Obtiene información de tiempo completa"""
        now = datetime.now()
        return f"""🕐 INFORMACIÓN DE TIEMPO:
📅 Fecha y hora: {now.strftime("%Y-%m-%d %H:%M:%S")}
📆 Día de la semana: {now.strftime("%A")}
📊 Semana del año: {now.isocalendar()[1]}
⏱️ Timestamp Unix: {int(now.timestamp())}"""
    
    def get_system_info(self):
        """Obtiene información del sistema"""
        try:
            import platform
            
            info = f"""💻 INFORMACIÓN DEL SISTEMA:
🖥️ OS: {platform.system()} {platform.release()}
🏗️ Arquitectura: {platform.architecture()[0]}
⚙️ Procesador: {platform.processor()}
🐍 Python: {platform.python_version()}"""
            
            try:
                import psutil
                info += f"""
🔧 CPU: {psutil.cpu_count()} cores
💾 RAM: {psutil.virtual_memory().total // (1024**3)} GB total
📊 Uso RAM: {psutil.virtual_memory().percent}%"""
            except ImportError:
                info += "\n💡 Instala 'psutil' para más detalles del sistema"
            
            return info
        except Exception as e:
            return f"❌ Error obteniendo información del sistema: {str(e)}"
    
    def get_weather(self, city=""):
        """Obtiene información del clima (usando API gratuita)"""
        try:
            # Usar wttr.in - servicio gratuito de clima
            if not city:
                city = "auto"  # Detectar ubicación automáticamente
            
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                location = data.get('nearest_area', [{}])[0]
                
                weather_info = f"""🌤️ CLIMA EN {city.upper()}:
📍 Ubicación: {location.get('areaName', [{}])[0].get('value', 'Desconocida')}
🌡️ Temperatura: {current['temp_C']}°C ({current['temp_F']}°F)
☁️ Condición: {current['weatherDesc'][0]['value']}
💧 Humedad: {current['humidity']}%
💨 Viento: {current['windspeedKmph']} km/h
👁️ Visibilidad: {current['visibility']} km"""
                
                return weather_info
            else:
                return f"❌ No se pudo obtener información del clima para: {city}"
                
        except Exception as e:
            return f"❌ Error al obtener clima: {str(e)}"
    
    def parse_tool_call(self, response):
        """Extrae llamadas a herramientas de manera más robusta"""
        patterns = [
            r'USE_TOOL:\s*(\w+)\((.*?)\)',
            r'TOOL:\s*(\w+)\((.*?)\)',
            r'CALL:\s*(\w+)\((.*?)\)',
            r'USAR:\s*(\w+)\((.*?)\)'
        ]
        
        matches = []
        for pattern in patterns:
            matches.extend(re.findall(pattern, response, re.IGNORECASE | re.DOTALL))
        
        return matches
    
    def create_enhanced_system_prompt(self):
        """Crea un system prompt optimizado para respuestas directas"""
        return f"""Eres un asistente de IA avanzado que proporciona respuestas directas y completas usando herramientas especializadas.

HERRAMIENTAS DISPONIBLES:
• web_search(query): Buscar información actualizada en internet
• calculator(expression): Realizar cálculos matemáticos
• file_operations(operation, filename, content): Manejar archivos
• python_code(code): Ejecutar código Python
• get_time(): Obtener información de tiempo
• system_info(): Información del sistema
• weather(city): Información del clima

FORMATO PARA USAR HERRAMIENTAS:
USE_TOOL: nombre_herramienta(argumentos)

REGLAS IMPORTANTES:
1. Proporciona respuestas DIRECTAS e INFORMATIVAS
2. NO hagas preguntas innecesarias al usuario
3. Usa las herramientas automáticamente cuando sean necesarias
4. Presenta la información de forma clara y organizada
5. Incluye detalles relevantes sin ser redundante

EJEMPLOS:
- Para "busca información sobre IA": USE_TOOL: web_search("inteligencia artificial 2025")
- Para "¿cuánto es 15 * 23?": USE_TOOL: calculator("15 * 23")
- Para "¿qué hora es?": USE_TOOL: get_time()

Fecha actual: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

RESPONDE SIEMPRE DE FORMA DIRECTA Y COMPLETA."""
    
    def process_query(self, user_query):
        """Procesa una consulta de manera optimizada para respuestas directas"""
        try:
            # DETECCIÓN DIRECTA DE COMANDOS DE HERRAMIENTAS
            if user_query.strip().startswith("USE_TOOL:"):
                return self.execute_direct_tool_command(user_query)
            
            # Detectar si necesita herramientas automáticamente
            needs_search = any(keyword in user_query.lower() for keyword in [
                'busca', 'buscar', 'información', 'noticias', 'actualiza', 'último',
                'search', 'find', 'what is', 'qué es', 'cómo está', 'últimas noticias',
                'que es', 'define', 'definición'
            ])
            
            needs_calc = any(keyword in user_query.lower() for keyword in [
                'calcula', 'calculate', 'cuánto es', 'how much', 'suma', 'resta', 
                'multiplica', 'divide', '+', '-', '*', '/', '=', 'math'
            ])
            
            needs_time = any(keyword in user_query.lower() for keyword in [
                'hora', 'time', 'fecha', 'date', 'qué hora', 'what time'
            ])
            
            needs_weather = any(keyword in user_query.lower() for keyword in [
                'clima', 'weather', 'temperatura', 'lluvia', 'sol'
            ])
            
            # EJECUCIÓN DIRECTA DE HERRAMIENTAS CUANDO ES OBVIO
            if needs_search:
                # Extraer términos de búsqueda
                search_terms = self.extract_search_terms(user_query)
                if search_terms:
                    search_result = self.web_search(search_terms)
                    return f"🔍 BÚSQUEDA EJECUTADA DIRECTAMENTE:\n\n{search_result}\n\n💡 Información encontrada sobre: {search_terms}"
            
            elif needs_calc:
                # Buscar expresión matemática
                calc_expr = self.extract_math_expression(user_query)
                if calc_expr:
                    calc_result = self.calculator(calc_expr)
                    return calc_result
            
            elif needs_time:
                return self.get_time()
            
            elif needs_weather:
                city = self.extract_city_from_query(user_query)
                return self.get_weather(city)
            
            # Si no es una consulta obvia de herramientas, usar el modelo normal
            system_prompt = self.create_enhanced_system_prompt()
            response = self.call_ollama(user_query, system_prompt)
            
            if "Error:" in response:
                return response
            
            # Buscar y ejecutar herramientas en la respuesta del modelo
            tool_calls = self.parse_tool_call(response)
            final_response = response
            
            if tool_calls:
                final_response += "\n\n" + "="*50 + "\n🔧 HERRAMIENTAS EJECUTADAS:\n" + "="*50
                
                for tool_name, args in tool_calls:
                    if tool_name in self.tools:
                        try:
                            self.print_message(f"Ejecutando: {tool_name}({args})", "info")
                            tool_result = self.execute_tool_safely(tool_name, args)
                            final_response += f"\n\n{tool_result}"
                            
                        except Exception as e:
                            error_msg = f"❌ Error ejecutando {tool_name}: {str(e)}"
                            self.print_message(error_msg, "error")
                            final_response += f"\n\n{error_msg}"
            
            # Guardar en historial
            self.conversation_history.append({
                'user': user_query,
                'assistant': final_response,
                'timestamp': datetime.now().isoformat(),
                'tools_used': [tool for tool, _ in tool_calls]
            })
            
            return final_response
            
        except Exception as e:
            error_msg = f"❌ Error procesando consulta: {str(e)}"
            if self.verbose:
                traceback.print_exc()
            return error_msg
    
    def save_conversation(self, filename=None):
        """Guarda la conversación en un archivo"""
        if not filename:
            filename = f"conversacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            filepath = self.work_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            self.print_message(f"Conversación guardada en: {filepath}", "success")
            return str(filepath)
        except Exception as e:
            self.print_message(f"Error guardando conversación: {str(e)}", "error")
            return None
    
    def chat_loop(self):
        """Loop de conversación interactiva optimizado"""
        # Mensaje de bienvenida
        if RICH_AVAILABLE and console:
            welcome_panel = Panel.fit(
                """🤖 Agente IA Open Source v2.1 - OPTIMIZADO
💡 Herramientas: web_search, calculator, file_ops, python_code, weather, system_info
📁 Directorio de trabajo: agente_workspace/
🚀 Respuestas directas sin preguntas innecesarias
❌ Comandos: 'quit', 'save', 'help', 'clear'""",
                title="[bold blue]Agente IA Optimizado[/bold blue]",
                border_style="blue"
            )
            console.print(welcome_panel)
        else:
            print("🤖 Agente IA Open Source v2.1 - OPTIMIZADO")
            print("💡 Respuestas directas con herramientas automáticas")
            print("📁 Directorio de trabajo: agente_workspace/")
            print("❌ Comandos: 'quit', 'save', 'help', 'clear'\n")
        
        while True:
            try:
                user_input = input("\n👤 Tu: ").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiales
                if user_input.lower() in ['quit', 'exit', 'salir']:
                    self.print_message("¿Quieres guardar la conversación antes de salir? (y/n)", "info")
                    save_choice = input().lower()
                    if save_choice in ['y', 'yes', 'sí', 'si']:
                        self.save_conversation()
                    self.print_message("¡Hasta luego!", "success")
                    break
                
                elif user_input.lower() == 'save':
                    self.save_conversation()
                    continue
                
                elif user_input.lower() == 'help':
                    help_text = """
🔧 COMANDOS DISPONIBLES:
• quit/exit - Salir del agente
• save - Guardar conversación  
• clear - Limpiar pantalla
• help - Mostrar esta ayuda

💡 EJEMPLOS DE CONSULTAS (RESPUESTAS DIRECTAS):
• "Busca información sobre machine learning 2025"
• "Calcula la raíz cuadrada de 144"
• "¿Qué hora es ahora?"
• "¿Cómo está el clima?"
• "Información del sistema"
• "Crea un archivo Python con un programa simple"

🚀 EL AGENTE PROPORCIONA RESPUESTAS DIRECTAS SIN PREGUNTAS ADICIONALES
                    """
                    self.print_message(help_text, "info")
                    continue
                
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                # Procesar consulta normal
                response = self.process_query(user_input)
                
                # Mostrar respuesta
                if RICH_AVAILABLE and console:
                    console.print("\n🤖 Agente:", style="bold blue")
                    if response.count('\n') > 10:  # Respuesta muy larga
                        console.print(Panel(response, border_style="blue", title="Respuesta Completa"))
                    else:
                        console.print(response)
                else:
                    print(f"\n🤖 Agente: {response}")
                
            except KeyboardInterrupt:
                self.print_message("\n\n¿Quieres salir? (y/n)", "warning")
                choice = input().lower()
                if choice in ['y', 'yes', 'sí', 'si']:
                    self.print_message("¡Hasta luego!", "success")
                    break
            except Exception as e:
                self.print_message(f"Error inesperado: {str(e)}", "error")
                if self.verbose:
                    traceback.print_exc()

def main():
    """Función principal con manejo de argumentos"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agente IA Open Source Optimizado")
    parser.add_argument("--model", default="llama3.2", help="Modelo de Ollama a usar")
    parser.add_argument("--verbose", action="store_true", help="Modo verbose")
    parser.add_argument("--query", help="Ejecutar una consulta única")
    
    args = parser.parse_args()
    
    # Crear agente
    agent = OpenSourceAgent(model_name=args.model, verbose=args.verbose)
    
    if args.query:
        # Modo consulta única
        response = agent.process_query(args.query)
        print(response)
    else:
        # Modo interactivo
        agent.chat_loop()

if __name__ == "__main__":
    main()