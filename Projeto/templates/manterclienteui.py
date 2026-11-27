import streamlit as st
import pandas as pd
import time
import base64
from service import Service

class ManterClienteUI:
    def main():
        st.header("Cadastro de Clientes")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterClienteUI.listar()
        with tab2: ManterClienteUI.inserir()
        with tab3: ManterClienteUI.atualizar()
        with tab4: ManterClienteUI.excluir()
    def listar():
        clientes = Service.cliente_listar()
        if len(clientes) == 0: st.write("Nenhum cliente cadastrado")
        else:
            list_dic = []
            for obj in clientes: list_dic.append(obj.to_dict())
            df = pd.DataFrame(list_dic)
            st.dataframe(df)
    def inserir():
        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o fone")
        senha = st.text_input("Informe a senha", type="password")
        foto = st.file_uploader("Foto do cliente", type=["png", "jpg", "jpeg"], key="foto_cliente_novo")
        if st.button("Inserir"):
            try:
                Service.cliente_inserir(nome, email, fone, senha, base64.b64encode(foto.getvalue()).decode() if foto else None)
                st.success("Cliente inserido com sucesso")
                st.rerun()
            except ValueError as erro:
                st.error(str(erro))
    def atualizar():
        clientes = Service.cliente_listar()
        if len(clientes) == 0: st.write("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Atualização de Clientes", clientes)
            nome = st.text_input("Novo nome", op.get_nome())
            email = st.text_input("Novo e-mail", op.get_email())
            fone = st.text_input("Novo fone", op.get_fone())
            senha = st.text_input("Nova senha", op.get_senha(), type="password")
            foto = st.file_uploader("Alterar foto", type=["png", "jpg", "jpeg"], key="foto_cliente_editar")
            if st.button("Atualizar"):
                id = op.get_id()
                try:
                    Service.cliente_atualizar(id, nome, email, fone, senha, base64.b64encode(foto.getvalue()).decode() if foto else op.get_foto())
                    st.success("Cliente atualizado com sucesso")
                    st.rerun()
                except ValueError as erro:
                    st.error(str(erro))                
    def excluir():
        clientes = Service.cliente_listar()
        if len(clientes) == 0: st.write("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Exclusão de Clientes", clientes)
            if st.button("Excluir"):
                id = op.get_id()
                Service.cliente_excluir(id)
                st.success("Cliente excluído com sucesso")
                time.sleep(2)
                st.rerun()                  
