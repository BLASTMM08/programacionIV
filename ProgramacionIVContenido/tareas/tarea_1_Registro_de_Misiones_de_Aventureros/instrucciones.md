🎯 Objetivo
Diseñar una base de datos relacional utilizando SQLite que permita registrar información clave sobre misiones, héroes participantes y monstruos enfrentados en un mundo de aventuras.

📝 Contexto
Un gremio de aventureros necesita un sistema para registrar:

Las misiones realizadas (ubicación, dificultad y recompensa)
Los héroes participantes (clase, nivel de experiencia, múltiples misiones)
Los monstruos enfrentados en cada misión
📌 Requisitos del modelo
Tu base de datos debe incluir al menos las siguientes entidades y relaciones:

🔹 Entidades principales
Héroes

Nombre
Clase (por ejemplo: Guerrero, Mago, Arquero, etc.)
Nivel de experiencia
Misiones

Nombre o descripción
Nivel de dificultad
Localización
Recompensa (monedas de oro)
Monstruos

Nombre
Tipo (por ejemplo: Dragón, Goblin, No-muerto, etc.)
Nivel de amenaza
🔹 Relaciones
Un héroe puede participar en muchas misiones y una misión puede tener muchos héroes ➜ relación muchos-a-muchos
Una misión puede tener muchos monstruos, y un monstruo puede aparecer en varias misiones ➜ relación muchos-a-muchos
🛠️ Entregables
Modelo lógico 
Debes incluir una tabla por entidad y por relación. Ejemplo de formato:

Tabla: heroes
- id (INTEGER, PRIMARY KEY)
- nombre (TEXT)
- clase (TEXT)
- nivel_experiencia (INTEGER)
Modelo entidad-relación (ER)


📁 Estructura esperada del modelo lógico
Tabla	Descripción
heroes	Información de cada héroe
misiones	Detalles de cada misión
monstruos	Información de cada monstruo
misiones_heroes	Relación entre misiones y héroes (participación)
misiones_monstruos	Relación entre misiones y monstruos (enemigos enfrentados)

💡 Consideraciones técnicas
Utiliza claves primarias (INTEGER PRIMARY KEY) y foráneas (FOREIGN KEY) adecuadamente
Añade restricciones donde sea relevante (por ejemplo, CHECK para niveles de amenaza o dificultad)
Las tablas puente (misiones_heroes, misiones_monstruos) deben usar claves compuestas o su propio id
