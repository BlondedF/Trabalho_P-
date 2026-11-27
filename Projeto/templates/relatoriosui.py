import streamlit as st
import pandas as pd
from datetime import date
from service import Service

class RelatoriosUI:
    @staticmethod
    def total_profissionais():
        st.header("Totalizar atendimentos dos profissionais")
        c1,c2=st.columns(2); inicio=c1.date_input("Data inicial",date.today().replace(day=1),key="rel_prof_ini"); fim=c2.date_input("Data final",date.today(),key="rel_prof_fim")
        if inicio>fim: st.error("A data inicial deve ser anterior à data final."); return
        dados=Service.totalizar_atendimentos_profissionais(inicio,fim); df=pd.DataFrame(dados)
        st.dataframe(df,use_container_width=True,hide_index=True)
        if not df.empty: st.bar_chart(df.set_index("Profissional"))
    @staticmethod
    def meus_atendimentos():
        st.header("Totalizar meus atendimentos")
        c1,c2=st.columns(2); inicio=c1.date_input("Data inicial",date.today().replace(day=1),key="rel_meu_ini"); fim=c2.date_input("Data final",date.today(),key="rel_meu_fim")
        if inicio>fim: st.error("A data inicial deve ser anterior à data final."); return
        dados=Service.totalizar_meus_atendimentos(st.session_state["usuario_id"],inicio,fim); df=pd.DataFrame(dados)
        st.dataframe(df,use_container_width=True,hide_index=True)
        if not df.empty: st.bar_chart(df.set_index("Serviço"))

class AgendaSemanaUI:
    @staticmethod
    def main():
        st.header("Agenda da semana")
        st.caption("Horários agendados de hoje até os próximos sete dias.")
        dados=Service.horario_agenda_semana()
        if dados: st.dataframe(pd.DataFrame(dados),use_container_width=True,hide_index=True)
        else: st.info("Não há horários agendados para os próximos sete dias.")
