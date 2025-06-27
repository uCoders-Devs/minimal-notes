import sqlite3


class DatabaseError(Exception):
    """Error en la operación de la base de datos."""
    pass


def create_connection(db_file: str = "notes.db") -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        raise DatabaseError(f"No se pudo conectar a la base de datos: {e}")


def create_table(conn: sqlite3.Connection) -> None:
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"No se pudo crear la tabla: {e}")


def add_note(conn: sqlite3.Connection, content: str) -> int:
    sql = "INSERT INTO notes(content) VALUES(?)" # (VALUES(?) → marcador de posición; evita concatenar strings y previene inyección SQL
    cursor = conn.cursor()
    cursor.execute(sql, (content,))
    conn.commit()
    note_id = cursor.lastrowid
    return note_id


def get_all_notes(conn: sqlite3.Connection) -> list[tuple]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    return rows


def update_note(conn: sqlite3.Connection, note_id: int, new_content: str) -> None:
    sql = "UPDATE notes SET content = ? WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (new_content, note_id))
    conn.commit()


def delete_note(conn: sqlite3.Connection, note_id: int) -> None:
    sql = "DELETE FROM notes WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (note_id,))
    conn.commit()


if __name__ == "__main__":
    # Testing
    conn = create_connection()

    if conn:
        create_table(conn)
        # Ejemplo de flujo CRUD:
        id1 = add_note(conn, "Mi primera nota de prueba.")
        id2 = add_note(conn, "Otra nota desde el script.")
        notas = get_all_notes(conn)
        for nota in notas:
            print(nota)
        update_note(conn, id1, "Nota 1 actualizada.")
        delete_note(conn, id2)
        
        conn.close()
        print("Conexión cerrada.")