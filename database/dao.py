
from database.DB_connect import DBConnect
from model.Rifugio import Rifugio
from model.Connessione import Connessione


class DAO:

    @staticmethod
    def get_rifugi():
        conn = DBConnect.get_connection()
        result = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id, nome, localita, altitudine, capienza, aperto 
                FROM rifugio
            """
            cursor.execute(query)
            for row in cursor:
                result.append(Rifugio(row['id'], row['nome'], row['localita'],
                                      row['altitudine'], row['capienza'], row['aperto']))
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def get_connessioni_fino_a_anno(anno):
        conn = DBConnect.get_connection()
        unique_connessioni = {}

        if conn:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT id_rifugio1, id_rifugio2, distanza, difficolta, durata, anno
                FROM connessione
                WHERE anno <= %s
            """
            cursor.execute(query, (anno,))

            for row in cursor:
                id1 = row['id_rifugio1']
                id2 = row['id_rifugio2']

                key = tuple(sorted((id1, id2)))

                connessione = Connessione(id1, id2, row['distanza'], row['difficolta'],
                                          row['durata'], row['anno'])

                if key not in unique_connessioni or connessione.anno > unique_connessioni[key].anno:
                    unique_connessioni[key] = connessione

            cursor.close()
            conn.close()

        return list(unique_connessioni.values())