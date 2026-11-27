import streamlit as st
from service import Service
import base64

class PerfilProfissionalUI:
    @staticmethod
    def main():
        st.header("Meu Perfil")
        op=Service.profissional_listar_id(st.session_state["usuario_id"])
        if not op: st.error("Profissional não encontrado."); return
        if op.get_foto(): st.image(base64.b64decode(op.get_foto()),width=150)
        foto=st.file_uploader("Alterar foto do perfil",type=["png","jpg","jpeg"])
        nome=st.text_input("Nome",op.get_nome()); email=st.text_input("E-mail",op.get_email()); esp=st.text_input("Especialidade",op.get_especialidade()); senha=st.text_input("Senha",op.get_senha(),type="password")
        if st.button("Salvar alterações"):
            foto_txt=base64.b64encode(foto.getvalue()).decode() if foto else op.get_foto()
            try: Service.profissional_atualizar(op.get_id(),nome,email,esp,senha,foto_txt); st.success("Perfil atualizado!"); st.rerun()
            except ValueError as e: st.error(str(e))
