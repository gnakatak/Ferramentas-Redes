import streamlit as st
from ferramentas.ping import ping

def render_dashboard():
    st.title("Página do Dashboard")
    st.write("Aqui você verá as ferramentas de rede.")

    # Medidor de Latência
    st.subheader("📍 Medidor de Latência da Rede")

    host = st.text_input("Endereço IP ou domínio", value="8.8.8.8")
    count = st.number_input("Número de pacotes (ping)", min_value=1, max_value=50, value=3)

    if st.button("🔍 Medir Latência (Ping)"):
        try:
            response = ping(host=host, count=count)
            if response["success"]:
                st.markdown(f"**Host:** {response['host']}")
                st.markdown(f"**Pacotes enviados:** {response['count']}")
                st.markdown(f"**Latência mínima:** {response['min_latency_ms']} ms")
                st.markdown(f"**Latência máxima:** {response['max_latency_ms']} ms")
                st.markdown(f"**Latência média:** {response['avg_latency_ms']} ms")
                st.code(response["output"])
            else:
                st.error(f"Erro ao executar o ping: {response['error']}")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")