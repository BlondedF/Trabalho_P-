import streamlit as st
from service import Service

class CancelarAgendamentoUI:
    @staticmethod
    def main():
        st.header("Cancelar agendamento")
        horarios=Service.horario_visualizar_meus_servicos(st.session_state["usuario_id"])
        horarios=[h for h in horarios if not h.get_confirmado()]
        if not horarios:
            st.info("Você não possui agendamentos que possam ser cancelados.")
            return
        op=st.selectbox("Selecione o agendamento",horarios,format_func=lambda h: f"{h.get_data().strftime('%d/%m/%Y %H:%M')} – {Service.servico_listar_id(h.get_id_servico()).get_descricao() if Service.servico_listar_id(h.get_id_servico()) else 'Serviço'}")
        if st.button("Cancelar agendamento"):
            try:
                Service.horario_cancelar_agendamento(op.get_id(),st.session_state["usuario_id"] )
                st.success("Agendamento cancelado. O horário voltou a ficar disponível.")
                st.rerun()
            except ValueError as erro: st.error(str(erro))