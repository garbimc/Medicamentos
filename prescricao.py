import sqlite3
import streamlit as st

# Funções para o banco de dados
def conectar_bd():
    return sqlite3.connect("medicamentos.db")

def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            concentracao_mg REAL,
            concentracao_ml REAL,
            dose_minima_kg_dia REAL,
            dose_maxima_kg_dia REAL,
            volume_embalagem_ml REAL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_medicamento(nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicamentos (nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml))
    conn.commit()
    conn.close()

def get_medicamentos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicamentos")
    medicamentos = cursor.fetchall()
    conn.close()
    return medicamentos

def atualizar_medicamento(id, nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE medicamentos 
        SET nome = ?, tipo = ?, concentracao_mg = ?, concentracao_ml = ?, dose_minima_kg_dia = ?, dose_maxima_kg_dia = ?, volume_embalagem_ml = ?
        WHERE id = ?
    ''', (nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml, id))
    conn.commit()
    conn.close()

def deletar_medicamento(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicamentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def calcular_dosagem(peso, medicamento, doses_por_dia):
    concentracao_mg_ml = medicamento[3] / medicamento[4]
    dose_total_dia = peso * medicamento[6]
    dose_por_administracao = dose_total_dia / doses_por_dia
    volume_por_administracao = dose_por_administracao / concentracao_mg_ml
    
    dose_total_minima_dia = peso * medicamento[5]
    dose_minima_por_administracao = dose_total_minima_dia / doses_por_dia
    volume_minima_por_administracao = dose_minima_por_administracao / concentracao_mg_ml

    return volume_por_administracao, volume_minima_por_administracao

# Interface com emojis
# Set up page configuration
st.set_page_config(page_title="Prescrição Medicamentos", page_icon="💊")

st.title("💊 Medicamentos - Pediatria")

abas_gerenciamento = st.tabs(["➕ Cadastrar Medicamento", "🔄 Atualizar Medicamento", "❌ Deletar Medicamento", "🧾 Prescrição"])

# Aba de cadastro de medicamento
with abas_gerenciamento[0]:
    st.subheader("➕ Cadastrar Medicamento")
    with st.form("form_cadastro_medicamento"):
        nome = st.text_input("📋 Nome do Medicamento")
        tipo = st.text_input("🔍 Tipo de Medicamento")
        concentracao_mg = st.number_input("💊 Concentração (mg)", min_value=1.0, step=0.1)
        concentracao_ml = st.number_input("💧 Concentração (ml)", min_value=1.0, step=0.1)
        dose_minima_kg_dia = st.number_input("📉 Dose mínima por kg/dia (mg)", min_value=1.0, step=0.1)
        dose_maxima_kg_dia = st.number_input("📈 Dose máxima por kg/dia (mg)", min_value=1.0, step=0.1)
        volume_embalagem_ml = st.number_input("📦 Volume da embalagem (ml)", min_value=1.0, step=0.1)
        
        submit_button = st.form_submit_button(label="Salvar Medicamento")
        if submit_button:
            inserir_medicamento(nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml)
            st.success(f"Medicamento '{nome}' cadastrado com sucesso!")

# Aba de atualização de medicamento
with abas_gerenciamento[1]:
    st.subheader("🔄 Atualizar Medicamento")
    medicamentos = get_medicamentos()
    medicamento_selecionado = st.selectbox("Selecione um medicamento para atualizar", [med[1] for med in medicamentos])
    
    if medicamento_selecionado:
        medicamento = next(med for med in medicamentos if med[1] == medicamento_selecionado)
        with st.form("form_atualizar_medicamento"):
            nome = st.text_input("📋 Nome do Medicamento", value=medicamento[1])
            tipo = st.text_input("🔍 Tipo de Medicamento", value=medicamento[2])
            concentracao_mg = st.number_input("💊 Concentração (mg)", min_value=1.0, value=float(medicamento[3]), step=0.1)
            concentracao_ml = st.number_input("💧 Concentração (ml)", min_value=1.0, value=float(medicamento[4]), step=0.1)
            dose_minima_kg_dia = st.number_input("📉 Dose mínima por kg/dia (mg)", min_value=1.0, value=float(medicamento[5]), step=0.1)
            dose_maxima_kg_dia = st.number_input("📈 Dose máxima por kg/dia (mg)", min_value=1.0, value=float(medicamento[6]), step=0.1)
            volume_embalagem_ml = st.number_input("📦 Volume da embalagem (ml)", min_value=1.0, value=float(medicamento[7]), step=0.1)

            submit_button = st.form_submit_button(label="Atualizar Medicamento")
            if submit_button:
                atualizar_medicamento(medicamento[0], nome, tipo, concentracao_mg, concentracao_ml, dose_minima_kg_dia, dose_maxima_kg_dia, volume_embalagem_ml)
                st.success(f"Medicamento '{nome}' atualizado com sucesso!")

# Aba de deleção de medicamento
with abas_gerenciamento[2]:
    st.subheader("❌ Deletar Medicamento")
    medicamento_selecionado = st.selectbox("Selecione um medicamento para deletar", [med[1] for med in medicamentos])
    
    if medicamento_selecionado:
        medicamento = next(med for med in medicamentos if med[1] == medicamento_selecionado)
        if st.button(f"Deletar {medicamento[1]}"):
            deletar_medicamento(medicamento[0])
            st.success(f"Medicamento '{medicamento[1]}' deletado com sucesso!")

# Aba de prescrição
with abas_gerenciamento[3]:
    st.subheader("🧾 Prescrição")
    peso = st.number_input("⚖️ Peso da Criança (kg)", min_value=1.0, step=0.1)
    medicamento_nome = st.selectbox("📋 Selecione o Medicamento", [med[1] for med in get_medicamentos()])
    doses_por_dia = st.selectbox("⏰ Quantidade de doses por dia(6hs, 8hs, 12hs, 1x)", [4, 3, 2,1])

    if peso and medicamento_nome and doses_por_dia:
        medicamento = next(med for med in get_medicamentos() if med[1] == medicamento_nome)
        volume_por_administracao, volume_minima_por_administracao = calcular_dosagem(peso, medicamento, doses_por_dia)
        
        st.write(f"**Dosagem Máxima por Administração:** {volume_por_administracao:.2f} ml 💊")
        st.write(f"**Dosagem Mínima por Administração:** {volume_minima_por_administracao:.2f} ml 💊")
