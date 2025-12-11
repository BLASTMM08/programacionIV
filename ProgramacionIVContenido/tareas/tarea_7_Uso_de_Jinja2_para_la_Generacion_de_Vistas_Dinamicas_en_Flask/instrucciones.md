🎯 Objetivo
Modificar la aplicación web de biblioteca personal para implementar correctamente Jinja2 como motor de plantillas, separando la lógica del backend de la presentación visual. Las vistas HTML deben ser generadas dinámicamente usando variables, estructuras de control y herencia de plantillas.

📝 Contexto
En esta fase, los estudiantes mejorarán la estructura de su aplicación web al integrar completamente Jinja2, el motor de plantillas utilizado por Flask. El objetivo es generar contenido dinámico desde el backend y mantener un código HTML limpio, reutilizable y organizado.

📌 Requisitos funcionales
La aplicación web debe seguir ofreciendo todas las funcionalidades implementadas previamente, ahora con el uso explícito de Jinja2:

Agregar nuevo libro
➤ Página HTML con formulario generado desde una plantilla Jinja2.
Actualizar información de un libro
➤ Formulario dinámico que cargue los datos del libro existente.
Eliminar libro existente
➤ Página de confirmación renderizada antes de proceder con la eliminación.
Ver listado de libros
➤ Página HTML que muestre una tabla con todos los libros usando un bucle for.
Buscar libros
➤ Página que muestre los resultados de búsqueda de manera dinámica.
🔄 Cambios y objetivos clave
Implementar Jinja2 en todas las vistas HTML del proyecto.
Crear una estructura de plantillas con base.html como plantilla principal.
Utilizar la herencia de plantillas ({% extends %} y {% block %}) para evitar duplicación.
Aplicar variables, bucles (for) y condicionales (if) en las plantillas.
Mantener un diseño visual coherente y limpio para la experiencia del usuario.
💡 Consideraciones técnicas
Crear la carpeta /templates para las plantillas y /static para los archivos CSS, JS e imágenes.
Incluir mensajes visuales (éxito, error, etc.) usando flash() y get_flashed_messages() con Jinja2.
Formularios y tablas deben estar generados completamente desde las plantillas, no desde el backend.
La plantilla base.html debe contener el layout general (barra de navegación, estructura HTML, etc.).
El archivo requirements.txt debe incluir Flask y cualquier otra librería usada.