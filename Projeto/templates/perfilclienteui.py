import streamlit as st
import base64 as biblioteca_baseb64
from service import Service

class PerfilClienteUI:
    @staticmethod
    def main():
        st.header("Meu Perfil")
        op=Service.cliente_listar_id(st.session_state["usuario_id"])
        if not op: st.error("Cliente não encontrado."); return
        if op.get_foto(): st.image(biblioteca_baseb64.b64decode(op.get_foto()),width=150)
        foto=st.file_uploader("Alterar foto do perfil",type=["png","jpg","jpeg"])
        nome=st.text_input("Nome",op.get_nome()); email=st.text_input("E-mail",op.get_email()); fone=st.text_input("Telefone",op.get_fone()); senha=st.text_input("Senha",op.get_senha(),type="password")
        if st.button("Salvar alterações"):
            imagem=foto.getvalue() if foto else op.get_foto()
            foto_txt=biblioteca_baseb64.b64encode(imagem).decode() if foto else op.get_foto()
            try: Service.cliente_atualizar(op.get_id(),nome,email,fone,senha,foto_txt); st.success("Perfil atualizado!"); st.rerun()
            except ValueError as e: st.error(str(e))
