import streamlit as st
from service import Service
class PerfilAdminUI:
    @staticmethod
    def main():
        st.header("Meus Dados")
        op=Service.cliente_listar_id(st.session_state["usuario_id"])
        nome=st.text_input("Nome",op.get_nome(),disabled=True); email=st.text_input("E-mail",op.get_email(),disabled=True); fone=st.text_input("Telefone",op.get_fone()); senha=st.text_input("Senha",op.get_senha(),type="password")
        if st.button("Atualizar"):
            try: Service.cliente_atualizar(op.get_id(),nome,email,fone,senha,op.get_foto()); st.success("Dados atualizados!")
            except ValueError as e: st.error(str(e))
