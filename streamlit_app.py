import streamlit as st
import openai

# Setup
st.set_page_config(page_title="Classificador e Gerador de Atividades", layout="centered")
st.title("📘 Classificador e Gerador de Atividades")

# Chave da API
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Input URL
url_input = st.text_input("Informe a URL do plano de aula:", placeholder="https://novaescola.org.br/planos-de-aula/...")

# Inicializa sessão
if "atividades_anteriores" not in st.session_state:
    st.session_state.atividades_anteriores = ""

# Botão de classificação
if st.button("Classificar Atividades"):
    if not url_input:
        st.warning("Por favor, insira uma URL.")
    else:
        with st.spinner("Analisando o plano de aula..."):
            prompt_classificacao = f"""
Você é um especialista em educação. Sua tarefa é analisar o plano de aula encontrado na URL abaixo, identificar as atividades pedagógicas propostas e classificá-las como **básico**, **intermediário** ou **avançado**, com base na complexidade e autonomia exigida dos estudantes.

Critérios:
- **Básico**: atividades de leitura, cópia, reconhecimento simples.
- **Intermediário**: interpretação, organização de ideias, produção com apoio.
- **Avançado**: produção autoral, resolução complexa, debates ou criação livre.

Retorne um texto corrido com a descrição de cada atividade proposta e sua classificação correspondente.

URL: {url_input}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é um classificador pedagógico especialista em planos de aula."},
                        {"role": "user", "content": prompt_classificacao}
                    ],
                    temperature=0.3,
                    max_tokens=1200
                )

                resultado = response.choices[0].message.content.strip()
                st.session_state.atividades_anteriores = resultado

                st.success("Atividades classificadas:")
                st.markdown(resultado)

            except Exception as e:
                st.error(f"Erro na classificação: {str(e)}")

# Se já existem atividades classificadas:
if st.session_state.atividades_anteriores:
    st.divider()
    st.subheader("🎯 Gerar Novas Atividades")

    nivel_desejado = st.selectbox(
        "Escolha o nível de dificuldade para as novas atividades:",
        ["básico", "intermediário", "avançado"]
    )

    if st.button("Gerar Novas Atividades"):
        with st.spinner("Gerando novas atividades..."):
            prompt_geracao = f"""
Com base nas seguintes atividades já existentes de um plano de aula:

{st.session_state.atividades_anteriores}

Crie novas atividades no nível de dificuldade **{nivel_desejado}**, mantendo coerência com o tema original, mas sem repetir exatamente as anteriores. As novas atividades devem ser compatíveis com os critérios do nível escolhido.

Descreva claramente as novas atividades geradas.
"""

            try:
                resposta_geracao = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é um criador de atividades educacionais com foco pedagógico."},
                        {"role": "user", "content": prompt_geracao}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

                novas_atividades = resposta_geracao.choices[0].message.content.strip()
                st.subheader("🆕 Novas Atividades Geradas:")
                st.markdown(novas_atividades)

            except Exception as e:
                st.error(f"Erro ao gerar novas atividades: {str(e)}")
