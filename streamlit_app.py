import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# Configuração do cliente OpenAI com API Key
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Classificador e Gerador de Atividades", layout="centered")
st.title("📘 Classificador de Atividades em Planos de Aula")

# Função para extrair conteúdo da página
def extrair_conteudo_da_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, f"Erro ao acessar a URL. Código {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        # Esta parte deve ser adaptada com base na estrutura real do HTML da Nova Escola
        # Aqui tentamos encontrar blocos de conteúdo comuns
        container = soup.find('div', class_='sc-bcXHqe')  # Exemplo: container geral
        if not container:
            container = soup.find('main')

        texto = container.get_text(separator='\n') if container else soup.get_text()
        return texto.strip(), None
    except Exception as e:
        return None, str(e)

# Inicializa sessão
if "atividades_anteriores" not in st.session_state:
    st.session_state.atividades_anteriores = ""

# Input de URL
url_input = st.text_input("Informe a URL do plano de aula:", placeholder="https://novaescola.org.br/planos-de-aula/...")

# Botão de classificação
if st.button("Classificar Atividades"):
    if not url_input:
        st.warning("Por favor, insira uma URL.")
    else:
        with st.spinner("Extraindo conteúdo da URL..."):
            texto_extraido, erro = extrair_conteudo_da_url(url_input)
        
        if erro:
            st.error(f"Erro ao processar a URL: {erro}")
        elif not texto_extraido or len(texto_extraido) < 100:
            st.warning("Não foi possível extrair conteúdo suficiente da página.")
        else:
            with st.spinner("Analisando conteúdo com GPT..."):
                prompt_classificacao = f"""
Você é um especialista em educação. Analise o conteúdo a seguir de um plano de aula e identifique claramente as atividades pedagógicas propostas. Para cada uma, classifique o nível de dificuldade como:

- **Básico**: leitura, cópia, reconhecimento simples;
- **Intermediário**: interpretação, organização, produção com apoio;
- **Avançado**: produção autoral, debate, investigação complexa.

Retorne as atividades com uma breve descrição e sua classificação de dificuldade.

Conteúdo do plano:

{texto_extraido}
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

# Se já classificou
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

Crie novas atividades no nível de dificuldade **{nivel_desejado}**, mantendo coerência com o tema original, mas sem repetir exatamente as anteriores.

Descreva cada nova atividade com clareza.
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
