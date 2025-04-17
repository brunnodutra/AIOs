import streamlit as st
import openai

# Configurações do app
st.set_page_config(page_title="Classificador de Atividades", layout="centered")
st.title("📘 Classificador de Atividades em Planos de Aula")

# Chave da API via st.secrets
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Input do usuário
url_input = st.text_input("Informe a URL do plano de aula:", placeholder="https://novaescola.org.br/planos-de-aula/...")

if st.button("Classificar Atividades"):
    if not url_input:
        st.warning("Por favor, insira uma URL.")
    else:
        with st.spinner("Analisando o plano de aula..."):
            prompt = f"""
Você é um especialista em educação. Sua tarefa é analisar o plano de aula encontrado na URL abaixo, identificar as atividades pedagógicas propostas e classificá-las como **básico**, **intermediário** ou **avançado**, com base na complexidade e autonomia exigida dos estudantes.

Critérios:
- **Básico**: atividades de leitura, cópia, reconhecimento simples.
- **Intermediário**: interpretação, organização de ideias, produção com apoio.
- **Avançado**: produção autoral, resolução complexa, debates ou criação livre.

Retorne a classificação diretamente como texto corrido, indicando claramente as atividades encontradas e seus respectivos níveis de dificuldade.

URL: {url_input}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é um classificador pedagógico especialista em planos de aula."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1200
                )

                resultado = response.choices[0].message.content.strip()
                st.success("Classificação concluída:")
                st.markdown(resultado)

            except Exception as e:
                st.error(f"Erro ao conectar com a API da OpenAI: {str(e)}")
