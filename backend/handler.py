from database import (
    create_connection,
    create_table,
    add_note,
    get_all_notes,
    update_note,
    delete_note
)


def notes_handler(command, db_file="notes.db", note_id=None, content=None):
    """
    Maneja operaciones CRUD para notas en SQLite.

    Args:
        command (str): 'create', 'read', 'update', 'delete'.
        db_file (str): Ruta a la base de datos.
        note_id (int, optional): ID de la nota para 'update'/'delete'.
        content (str, optional): Contenido de la nota para 'create'/'update'.

    Returns:
        Any: Resultado según operación.

    Raises:
        ValueError: Si el comando es inválido o faltan parámetros.
    """
    conn = create_connection(db_file)
    create_table(conn)

    try:
        if command == 'create':
            return add_note(conn, content)
        elif command == 'read':
            return get_all_notes(conn)
        elif command == 'update':
            if note_id is None or content is None:
                raise ValueError("Faltan 'note_id' y/o 'content' para actualizar una nota.")
            update_note(conn, note_id, content)
        elif command == 'delete':
            if note_id is None:
                raise ValueError("Falta 'note_id' para borrar una nota.")
            delete_note(conn, note_id)
        else:
            raise ValueError("Comando inválido. Usá 'create', 'read', 'delete' o 'update'.")
    finally:
        conn.close()