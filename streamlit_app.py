import streamlit as st
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Resumo SEO Generativo", layout="centered")
st.title("🔍 Gerador de Resumo Otimizado para Buscas Generativas")

# Inicialização do cliente OpenAI com a nova interface
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Campo de entrada da URL
url_input = st.text_input("Informe a URL do conteúdo da Nova Escola:", placeholder="https://novaescola.org.br/planos-de-aula/...")
gerar_resumo = st.button("Gerar Resumo Otimizado")

if gerar_resumo:
    if not url_input:
        st.warning("Por favor, insira uma URL.")
    else:
        with st.spinner("Gerando resumo otimizado para buscas generativas..."):
            prompt = f"""
Você é um especialista em SEO e otimização para mecanismos de busca generativa como ChatGPT, Claude e Gemini.

Analise o conteúdo acessível a partir da seguinte URL: {url_input}

A seguir, gere um **resumo otimizado**, com as seguintes características:
1. Deve ter entre 300 a 500 palavras.
2. Ser informativo, claro e preciso.
3. Conter naturalmente palavras-chave relevantes para o tema abordado.
4. Antecipar e responder perguntas comuns que usuários fariam sobre esse conteúdo.
5. Estruturar com boa escaneabilidade (títulos, listas, negritos se necessário).
6. Usar linguagem acessível e evitar jargões técnicos desnecessários.

Formato esperado:
# Título SEO-friendly
## Subtítulo descritivo
Resumo em até 500 palavras, dividido em blocos de texto claros, contendo as respostas e informações mais buscadas.
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é um especialista em SEO para IA generativa, focado em conteúdo educacional."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    max_tokens=1500
                )

                resultado = response.choices[0].message.content.strip()
                st.success("Resumo gerado com sucesso:")
                st.markdown(resultado)

            except Exception as e:
                st.error(f"Erro ao conectar com a API da OpenAI: {str(e)}")
