-- Schema for Adventurer's Guild Database

-- Table: heroes
-- Stores information about adventurers.
CREATE TABLE IF NOT EXISTS heroes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    clase TEXT NOT NULL,
    nivel_experiencia INTEGER NOT NULL CHECK (nivel_experiencia >= 0)
);

-- Table: misiones
-- Stores details about quests available or completed.
CREATE TABLE IF NOT EXISTS misiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    nivel_dificultad INTEGER NOT NULL CHECK (nivel_dificultad > 0),
    localizacion TEXT NOT NULL,
    recompensa INTEGER NOT NULL CHECK (recompensa >= 0)
);

-- Table: monstruos
-- Stores information about monsters found in the world.
CREATE TABLE IF NOT EXISTS monstruos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    nivel_amenaza INTEGER NOT NULL CHECK (nivel_amenaza > 0)
);

-- Table: misiones_heroes
-- Join table for the many-to-many relationship between missions and heroes.
-- Represents which heroes participated in which missions.
CREATE TABLE IF NOT EXISTS misiones_heroes (
    mision_id INTEGER,
    heroe_id INTEGER,
    PRIMARY KEY (mision_id, heroe_id),
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
    FOREIGN KEY (heroe_id) REFERENCES heroes(id) ON DELETE CASCADE
);

-- Table: misiones_monstruos
-- Join table for the many-to-many relationship between missions and monsters.
-- Represents which monsters appear in which missions.
CREATE TABLE IF NOT EXISTS misiones_monstruos (
    mision_id INTEGER,
    monstruo_id INTEGER,
    PRIMARY KEY (mision_id, monstruo_id),
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
    FOREIGN KEY (monstruo_id) REFERENCES monstruos(id) ON DELETE CASCADE
);
