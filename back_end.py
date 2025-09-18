import sqlite3
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
dbname = 'database.db'
swagger = Swagger(app)

def data_base_connection():
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

def format_date_br(date_str):
    # Aceita yyyy-mm-dd ou yyyy-mm-ddTHH:MM:SS
    if not date_str:
        return None
    try:
        parts = date_str.split("T")[0].split("-")
        if len(parts) == 3:
            y, m, d = parts
            return f"{d.zfill(2)}/{m.zfill(2)}/{y}"
    except Exception:
        pass
    return date_str

@app.route('/categoria', methods=['GET'])
def get_categoria():
    """
    Lista de categorias
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias obtida com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da categoria
              name:
                type: string
                description: Nome da categoria
              description:
                type: string
                description: Descrição da categoria
    """
    conn = data_base_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categoria")
    rows = cursor.fetchall()
    categories = [dict(row) for row in rows]
    conn.close()
    return jsonify(categories)

@app.route('/login', methods=['POST'])
def login():
    """
    Autenticação de usuário
    ---
    tags:
      - Autenticação
    consumes:
      - application/json
    parameters:
      - in: body
        name: credenciais
        required: true
        schema:
          type: object
          required: [usuario, senha]
          properties:
            usuario:
              type: string
              description: Nome de usuário (corresponde a Usuario.Nome_usuario)
              example: "daniel"
            senha:
              type: string
              description: Senha do usuário (corresponde a Usuario.senha)
              example: "123456"
    responses:
      200:
        description: Login bem-sucedido
        schema:
          type: object
          properties:
            user_id:
              type: integer
            usuario:
              type: string
            message:
              type: string
      401:
        description: Credenciais inválidas
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json(silent=True) or {}
    usuario = data.get('usuario')
    senha = data.get('senha')

    if not usuario or not senha:
        return jsonify({"error": "Informe usuario e senha"}), 400

    conn = data_base_connection()
    cur = conn.cursor()
    # Tabela: Usuario | Campos: Nome_usuario, senha
    cur.execute("""
        SELECT rowid AS id, Nome_usuario
        FROM Usuario
        WHERE Nome_usuario = ? AND senha = ?
        LIMIT 1
    """, (usuario, senha))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Credenciais inválidas"}), 401

    return jsonify({
        "user_id": row["id"],
        "usuario": row["Nome_usuario"],
        "message": "Login bem-sucedido"
    }), 200

@app.route('/adicionarusuario', methods=['POST'])
def adicionar_usuario():
    """
    Adiciona um novo usuário à tabela Usuario
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    parameters:
      - in: body
        name: usuario
        required: true
        schema:
          type: object
          required: [Nome_usuario, senha]
          properties:
            Nome_usuario:
              type: string
            senha:
              type: string
    responses:
      201:
        description: Usuário adicionado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            message:
              type: string
      400:
        description: Dados inválidos ou usuário já existe
    """
    data = request.get_json(silent=True) or {}
    nome_usuario = data.get("Nome_usuario")
    senha = data.get("senha")
    if not nome_usuario or not senha:
        return jsonify({"error": "Nome_usuario e senha obrigatórios"}), 400

    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT rowid FROM Usuario WHERE Nome_usuario = ?", (nome_usuario,))
    if cur.fetchone():
        conn.close()
        return jsonify({"error": "Usuário já existe"}), 400

    cur.execute("INSERT INTO Usuario (Nome_usuario, senha) VALUES (?, ?)", (nome_usuario, senha))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return jsonify({"id": user_id, "message": "Usuário adicionado com sucesso"}), 201

# -------------------------------
# GET /tarefas  (lista bruta)
# -------------------------------
@app.route('/tarefas', methods=['GET'])
def get_tarefas():
    """
    Lista todas as tarefas
    ---
    tags:
      - Tarefas
    responses:
      200:
        description: Lista de tarefas obtida com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              titulo:
                type: string
              descricao:
                type: string
              fk_status:
                type: string
                description: Status usado no Kanban
    """
    conn = data_base_connection()
    cur = conn.cursor()
    # Tabela: Tarefas | Campos mínimos esperados: id, titulo, descricao, fk_status
    cur.execute("SELECT * FROM Tarefas")
    rows = cur.fetchall()
    tarefas = [dict(r) for r in rows]
    conn.close()
    return jsonify(tarefas), 200




@app.route('/tarefas/status/<int:status_id>', methods=['GET'])
def get_tarefas_por_status(status_id):
    """
    Lista todas as tarefas filtradas pelo fk_status informado
    ---
    tags:
      - Tarefas
    parameters:
      - name: status_id
        in: path
        type: integer
        required: true
        description: ID do status (fk_status) para filtrar as tarefas
    responses:
      200:
        description: Lista de tarefas com o fk_status informado
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da tarefa
              titulo:
                type: string
                description: Título da tarefa
              descricao:
                type: string
                description: Descrição da tarefa
              fk_status:
                type: integer
                description: ID do status (fk_status)
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tarefas WHERE fk_status = ?", (status_id,))
    rows = cur.fetchall()
    conn.close()

    tarefas = [dict(r) for r in rows]
    return jsonify(tarefas), 200

@app.route('/tarefas', methods=['POST'])
def create_tarefa():
    """
    Cria uma nova tarefa
    ---
    tags:
      - Tarefas
    consumes:
      - application/json
    parameters:
      - in: body
        name: tarefa
        required: true
        schema:
          type: object
          required: [Titulo, Descricao_tarefa, Data_de_criacao, Prazo_de_conclusao, Tempo_estimado, fk_prioridade, fk_status, fk_usuario]
          properties:
            Titulo:
              type: string
              example: "Implementar rota de criação"
            Descricao_tarefa:
              type: string
              example: "Criar endpoint POST /tarefas"
            Data_de_criacao:
              type: string
              format: date
              example: "2025-09-06"
            Prazo_de_conclusao:
              type: string
              format: date
              example: "2025-09-15"
            Tempo_estimado:
              type: string
              example: "5 dias"
            fk_prioridade:
              type: integer
              example: 1
            fk_status:
              type: integer
              example: 1
            fk_usuario:
              type: integer
              example: 10
    responses:
      201:
        description: Tarefa criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            message:
              type: string
      400:
        description: Dados inválidos
    """
    data = request.get_json(silent=True) or {}

    campos_obrigatorios = ["Titulo", "Descricao_tarefa", "Data_de_criacao", 
                           "Prazo_de_conclusao", "Tempo_estimado", 
                           "fk_prioridade", "fk_status", "fk_usuario"]

    if not all(campo in data for campo in campos_obrigatorios):
        return jsonify({"error": "Todos os campos obrigatórios devem ser informados"}), 400

    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Tarefas 
        (Titulo, Descricao_tarefa, Data_de_criacao, Prazo_de_conclusao, Tempo_estimado, fk_prioridade, fk_status, fk_usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["Titulo"],
        data["Descricao_tarefa"],
        data["Data_de_criacao"],
        data["Prazo_de_conclusao"],
        data["Tempo_estimado"],
        data["fk_prioridade"],
        data["fk_status"],
        data["fk_usuario"]
    ))
    conn.commit()
    tarefa_id = cur.lastrowid
    conn.close()

    return jsonify({"id": tarefa_id, "message": "Tarefa criada com sucesso"}), 201

@app.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def delete_tarefa(tarefa_id):
    """
    Deleta uma tarefa pelo ID
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
        description: ID da tarefa a ser deletada
    responses:
      200:
        description: Tarefa deletada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Tarefa não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    conn = data_base_connection()
    cur = conn.cursor()

    # Verifica se a tarefa existe
    cur.execute("SELECT * FROM Tarefas WHERE ID = ?", (tarefa_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    # Deleta a tarefa
    cur.execute("DELETE FROM Tarefas WHERE ID = ?", (tarefa_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Tarefa {tarefa_id} deletada com sucesso"}), 200

# -------------------------------
# GET /prioridades
# -------------------------------
@app.route('/prioridades', methods=['GET'])
def get_prioridades():
    """
    Lista todas as prioridades
    ---
    tags:
      - Prioridades
    responses:
      200:
        description: Lista de prioridades obtida com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da prioridade
              nome:
                type: string
                description: Nome da prioridade
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Prioridade")
    rows = cur.fetchall()
    conn.close()

    prioridades = [dict(r) for r in rows]
    return jsonify(prioridades), 200


# -------------------------------
# GET /status
# -------------------------------
@app.route('/status', methods=['GET'])
def get_status():
    """
    Lista todos os status
    ---
    tags:
      - Status
    responses:
      200:
        description: Lista de status obtida com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID do status
              nome:
                type: string
                description: Nome do status
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Status")
    rows = cur.fetchall()
    conn.close()

    status_list = [dict(r) for r in rows]
    return jsonify(status_list), 200

@app.route('/tarefas/<int:tarefa_id>', methods=['GET'])
def get_tarefa_por_id(tarefa_id):
    """
    Busca uma tarefa pelo ID, retornando os nomes de prioridade, status e usuário.
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
        description: ID da tarefa a ser buscada
    responses:
      200:
        description: Tarefa encontrada
        schema:
          type: object
          properties:
            id:
              type: integer
            titulo:
              type: string
            descricao:
              type: string
            prioridade:
              type: string
            status:
              type: string
            usuario:
              type: string
      404:
        description: Tarefa não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Tarefas WHERE ID = ?', (tarefa_id,))
    tarefa = cur.fetchone()
    if not tarefa:
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    tarefa_dict = dict(tarefa)

    # Buscar nome da prioridade
    prioridade_nome = None
    if tarefa_dict.get("fk_prioridade"):
        cur.execute('SELECT Nome_prioridade FROM Prioridade WHERE ID = ?', (tarefa_dict["fk_prioridade"],))
        row = cur.fetchone()
        prioridade_nome = row["Nome_prioridade"] if row else None

    # Buscar nome do status
    status_nome = None
    if tarefa_dict.get("fk_status"):
        cur.execute('SELECT Nome_status FROM Status WHERE ID = ?', (tarefa_dict["fk_status"],))
        row = cur.fetchone()
        status_nome = row["Nome_status"] if row else None

    # Buscar nome do usuário
    usuario_nome = None
    if tarefa_dict.get("fk_usuario"):
        cur.execute('SELECT Nome_usuario FROM Usuario WHERE ID = ?', (tarefa_dict["fk_usuario"],))
        row = cur.fetchone()
        usuario_nome = row["Nome_usuario"] if row else None

    conn.close()

    # Montar resposta
    resposta = {
        "id": tarefa_dict.get("ID"),
        "Titulo": tarefa_dict.get("Titulo"),
        "Descricao_tarefa": tarefa_dict.get("Descricao_tarefa"),
        "Data_de_criacao": format_date_br(tarefa_dict.get("Data_de_criacao")),
        "Prazo_de_conclusao": format_date_br(tarefa_dict.get("Prazo_de_conclusao")),
        "Tempo_estimado": tarefa_dict.get("Tempo_estimado"),
        "prioridade": prioridade_nome,
        "status": status_nome,
        "usuario": usuario_nome
    }
    return jsonify(resposta), 200

@app.route('/tarefas/<int:tarefa_id>/status', methods=['PUT'])
def update_tarefa_status(tarefa_id):
    """
    Atualiza o status de uma tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
        description: ID da tarefa a ser atualizada
      - in: body
        name: status
        required: true
        schema:
          type: object
          required: [status_id]
          properties:
            status_id:
              type: integer
              description: Novo ID do status (fk_status)
    responses:
      200:
        description: Status atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            fk_status:
              type: integer
            message:
              type: string
      400:
        description: Dados inválidos
      404:
        description: Tarefa não encontrada
    """
    data = request.get_json(silent=True) or {}
    status_id = data.get("status_id")
    if status_id is None:
        return jsonify({"error": "Campo status_id obrigatório"}), 400

    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tarefas WHERE ID = ?", (tarefa_id,))
    tarefa = cur.fetchone()
    if not tarefa:
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    cur.execute("UPDATE Tarefas SET fk_status = ? WHERE ID = ?", (status_id, tarefa_id))
    conn.commit()
    conn.close()
    return jsonify({"id": tarefa_id, "fk_status": status_id, "message": "Status atualizado com sucesso"}), 200

@app.route('/categoria_tarefa', methods=['POST'])
def add_categoria_tarefa():
    """
    Adiciona relação entre tarefa e categoria
    ---
    tags:
      - CategoriaTarefa
    consumes:
      - application/json
    parameters:
      - in: body
        name: relacao
        required: true
        schema:
          type: object
          required: [fk_tarefa, fk_categoria]
          properties:
            fk_tarefa:
              type: integer
            fk_categoria:
              type: integer
    responses:
      201:
        description: Relação criada
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Dados inválidos
    """
    data = request.get_json(silent=True) or {}
    fk_tarefa = data.get("fk_tarefa")
    fk_categoria = data.get("fk_categoria")
    if not fk_tarefa or not fk_categoria:
        return jsonify({"error": "fk_tarefa e fk_categoria obrigatórios"}), 400

    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categoria_tarefa (fk_tarefa, fk_categoria) VALUES (?, ?)", (fk_tarefa, fk_categoria))
    conn.commit()
    conn.close()
    return jsonify({"message": "Relação categoria-tarefa criada"}), 201

@app.route('/tarefas/<int:tarefa_id>/categorias', methods=['GET'])
def get_categorias_da_tarefa(tarefa_id):
    """
    Busca as categorias relacionadas a uma tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
        description: ID da tarefa
    responses:
      200:
        description: Lista de categorias relacionadas à tarefa
        schema:
          type: array
          items:
            type: object
            properties:
              ID:
                type: integer
              Nome_categoria:
                type: string
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.ID, c.Nome_categoria
        FROM Categoria c
        JOIN categoria_tarefa ct ON ct.fk_categoria = c.ID
        WHERE ct.fk_tarefa = ?
    """, (tarefa_id,))
    rows = cur.fetchall()
    conn.close()
    categorias = [dict(r) for r in rows]
    return jsonify(categorias), 200

@app.route('/tarefas/usuario/<int:usuario_id>', methods=['GET'])
def get_tarefas_por_usuario(usuario_id):
    """
    Lista todas as tarefas filtradas pelo usuário informado
    ---
    tags:
      - Tarefas
    parameters:
      - name: usuario_id
        in: path
        type: integer
        required: true
        description: ID do usuário para filtrar as tarefas
    responses:
      200:
        description: Lista de tarefas do usuário informado
        schema:
          type: array
          items:
            type: object
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tarefas WHERE fk_usuario = ?", (usuario_id,))
    rows = cur.fetchall()
    conn.close()
    tarefas = [dict(r) for r in rows]
    return jsonify(tarefas), 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Lista todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários obtida com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              ID:
                type: integer
              Nome_usuario:
                type: string
    """
    conn = data_base_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID, Nome_usuario FROM Usuario")
    rows = cur.fetchall()
    conn.close()
    usuarios = [dict(r) for r in rows]
    return jsonify(usuarios), 200

if __name__ == '__main__':
    app.run(debug=True)