import streamlit as st
from service import Service

class AbrirContaUI:
    @staticmethod
    def main():
        st.header("Abrir Conta no Sistema")
        nome=st.text_input("Informe o nome")
        email=st.text_input("Informe o e-mail")
        fone=st.text_input("Informe o telefone")
        senha=st.text_input("Informe a senha",type="password")
        if st.button("Criar conta"):
            try:
                Service.cliente_inserir(nome,email,fone,senha)
                st.success("Conta criada com sucesso! Agora você pode entrar no sistema.")
            except ValueError as erro: st.error(str(erro))
