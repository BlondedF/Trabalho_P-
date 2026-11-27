from dao_sql.clientedao import ClienteDAO
from dao_sql.profissionaldao import ProfissionalDAO
from dao_sql.servicodao import ServicoDAO
from dao_sql.horariodao import HorarioDAO
from dao_sql.atendimentodao import AtendimentoDAO
from models.cliente import Cliente
from models.profissional import Profissional
from models.servico import Servico
from models.horario import Horario
from models.atendimento import Atendimento
from datetime import datetime, timedelta, date

class Service:
    @staticmethod
    def _email_validar(email, id_atual=None, tipo_atual=None):
        normalizado = email.strip().casefold()
        if not normalizado:
            raise ValueError('Informe um e-mail válido.')
        if normalizado == 'admin':
            atual = ClienteDAO().listar_id(id_atual) if tipo_atual == 'cliente' and id_atual is not None else None
            if not atual or atual.get_email().casefold() != 'admin':
                raise ValueError("O e-mail 'admin' é reservado para o administrador.")
        for tipo, pessoas in [('cliente', ClienteDAO().listar()), ('profissional', ProfissionalDAO().listar())]:
            for pessoa in pessoas:
                if tipo == tipo_atual and pessoa.get_id() == id_atual: continue
                if pessoa.get_email().strip().casefold() == normalizado:
                    raise ValueError('Já existe um cliente ou profissional com este e-mail.')

    @staticmethod
    def cliente_inserir(nome,email,fone,senha,foto=None):
        Service._email_validar(email)
        ClienteDAO().inserir(Cliente(0,nome,email,fone,senha,foto))
    @staticmethod
    def cliente_listar(): return sorted(ClienteDAO().listar(), key=lambda x:x.get_nome().casefold())
    @staticmethod
    def cliente_listar_id(id): return ClienteDAO().listar_id(id)
    @staticmethod
    def cliente_atualizar(id,nome,email,fone,senha,foto=None):
        Service._email_validar(email,id,'cliente')
        anterior=ClienteDAO().listar_id(id)
        if foto is None and anterior: foto=anterior.get_foto()
        ClienteDAO().atualizar(Cliente(id,nome,email,fone,senha,foto))
    @staticmethod
    def cliente_excluir(id): ClienteDAO().excluir(id)
    @staticmethod
    def cliente_criar_admin():
        if not any(c.get_email()=='admin' for c in ClienteDAO().listar()):
            ClienteDAO().inserir(Cliente(0,'admin','admin','-','1234'))
    @staticmethod
    def cliente_autenticar(email,senha):
        for c in ClienteDAO().listar():
            if c.get_email()==email and c.get_senha()==senha: return {'id':c.get_id(),'nome':c.get_nome()}
        return None

    @staticmethod
    def profissional_inserir(nome,email,especialidade,senha,foto=None):
        Service._email_validar(email)
        ProfissionalDAO().inserir(Profissional(0,nome,email,especialidade,senha,foto))
    @staticmethod
    def profissional_listar(): return sorted(ProfissionalDAO().listar(),key=lambda x:x.get_nome().casefold())
    @staticmethod
    def profissional_listar_id(id): return ProfissionalDAO().listar_id(id)
    @staticmethod
    def profissional_atualizar(id,nome,email,especialidade,senha,foto=None):
        Service._email_validar(email,id,'profissional')
        anterior=ProfissionalDAO().listar_id(id)
        if foto is None and anterior: foto=anterior.get_foto()
        ProfissionalDAO().atualizar(Profissional(id,nome,email,especialidade,senha,foto))
    @staticmethod
    def profissional_excluir(id):
        if any(h.get_id_profissional()==id for h in HorarioDAO().listar()): raise ValueError('Não é possível excluir profissional com horários cadastrados.')
        ProfissionalDAO().excluir(id)
    @staticmethod
    def profissional_autenticar(email,senha):
        for p in ProfissionalDAO().listar():
            if p.get_email()==email and p.get_senha()==senha: return {'id':p.get_id(),'nome':p.get_nome()}
        return None

    @staticmethod
    def servico_inserir(descricao,valor): ServicoDAO().inserir(Servico(0,descricao,valor))
    @staticmethod
    def servico_listar(): return sorted(ServicoDAO().listar(),key=lambda x:x.get_descricao().casefold())
    @staticmethod
    def servico_listar_id(id): return ServicoDAO().listar_id(id)
    @staticmethod
    def servico_atualizar(id,descricao,valor): ServicoDAO().atualizar(Servico(id,descricao,valor))
    @staticmethod
    def servico_excluir(id): ServicoDAO().excluir(id)

    @staticmethod
    def horario_inserir(data,confirmado,id_cliente,id_servico,id_profissional):
        obj=Horario(0,data,confirmado,id_cliente,id_servico,id_profissional); Service._horario_validar(obj); HorarioDAO().inserir(obj)
    @staticmethod
    def horario_listar(): return sorted(HorarioDAO().listar(),key=lambda x:x.get_data())
    @staticmethod
    def horario_listar_id(id): return HorarioDAO().listar_id(id)
    @staticmethod
    def horario_atualizar(id,data,confirmado,id_cliente,id_servico,id_profissional):
        obj=Horario(id,data,confirmado,id_cliente,id_servico,id_profissional); Service._horario_validar(obj); HorarioDAO().atualizar(obj)
    @staticmethod
    def horario_excluir(id):
        h=HorarioDAO().listar_id(id)
        if h and h.get_id_cliente() not in (None,0): raise ValueError('Não é possível excluir horário já agendado.')
        HorarioDAO().excluir(id)
    @staticmethod
    def _horario_validar(obj):
        for h in HorarioDAO().listar():
            if h.get_id()!=obj.get_id() and h.get_id_profissional()==obj.get_id_profissional() and h.get_data()==obj.get_data():
                raise ValueError('Este profissional já possui horário nessa data e hora.')
    @staticmethod
    def horario_listar_disponiveis(id_profissional):
        agora=datetime.now()
        return [h for h in Service.horario_listar() if h.get_data()>=agora and not h.get_confirmado() and h.get_id_cliente() is None and h.get_id_profissional()==id_profissional]
    @staticmethod
    def horario_abrir_agenda(data,hora_inicio,hora_fim,intervalo,id_profissional):
        x=datetime.strptime(data+' '+hora_inicio,'%d/%m/%Y %H:%M'); fim=datetime.strptime(data+' '+hora_fim,'%d/%m/%Y %H:%M')
        if intervalo<=0: raise ValueError('O intervalo deve ser maior que zero.')
        while x<=fim:
            Service.horario_inserir(x,False,None,None,id_profissional); x+=timedelta(minutes=intervalo)
    @staticmethod
    def horario_visualizar_minha_agenda(id_profissional): return [h for h in Service.horario_listar() if h.get_id_profissional()==id_profissional]
    @staticmethod
    def horario_visualizar_meus_servicos(id_cliente): return [h for h in Service.horario_listar() if h.get_id_cliente()==id_cliente]
    @staticmethod
    def horario_cancelar_agendamento(id_horario, id_cliente):
        horario = HorarioDAO().listar_id(id_horario)
        if not horario or horario.get_id_cliente() != id_cliente:
            raise ValueError('Agendamento não encontrado para este cliente.')
        if horario.get_confirmado():
            raise ValueError('Não é possível cancelar um serviço já confirmado.')
        if horario.get_data() < datetime.now():
            raise ValueError('Não é possível cancelar um horário que já passou.')
        horario.set_id_cliente(None)
        horario.set_id_servico(None)
        HorarioDAO().atualizar(horario)
    @staticmethod
    def horario_confirmar_servico(id_profissional): return [h for h in Service.horario_listar() if not h.get_confirmado() and h.get_id_cliente() is not None and h.get_id_profissional()==id_profissional]

    @staticmethod
    def atendimento_inserir(data,queixa_principal,historico_saude,avaliacao,prescricao,id_horario): AtendimentoDAO().inserir(Atendimento(0,data,queixa_principal,historico_saude,avaliacao,prescricao,id_horario))
    @staticmethod
    def atendimento_listar(): return sorted(AtendimentoDAO().listar(),key=lambda x:x.get_data())
    @staticmethod
    def atendimento_listar_id(id): return AtendimentoDAO().listar_id(id)
    @staticmethod
    def atendimento_atualizar(id,data,queixa_principal,historico_saude,avaliacao,prescricao,id_horario): AtendimentoDAO().atualizar(Atendimento(id,data,queixa_principal,historico_saude,avaliacao,prescricao,id_horario))
    @staticmethod
    def atendimento_excluir(id): AtendimentoDAO().excluir(id)

    @staticmethod
    def totalizar_atendimentos_profissionais(inicio,fim):
        contagem={p.get_id():{'Profissional':p.get_nome(),'Atendimentos':0} for p in Service.profissional_listar()}
        for a in Service.atendimento_listar():
            h=Service.horario_listar_id(a.get_id_horario())
            if h and inicio<=a.get_data().date()<=fim and h.get_id_profissional() in contagem: contagem[h.get_id_profissional()]['Atendimentos']+=1
        return list(contagem.values())
    @staticmethod
    def totalizar_meus_atendimentos(id_profissional,inicio,fim):
        contagem={s.get_id():{'Serviço':s.get_descricao(),'Quantidade':0} for s in Service.servico_listar()}
        for a in Service.atendimento_listar():
            h=Service.horario_listar_id(a.get_id_horario())
            if h and h.get_id_profissional()==id_profissional and inicio<=a.get_data().date()<=fim and h.get_id_servico() in contagem: contagem[h.get_id_servico()]['Quantidade']+=1
        return list(contagem.values())
    @staticmethod
    def horario_agenda_semana():
        hoje=date.today(); limite=hoje+timedelta(days=6); resultado=[]
        clientes={c.get_id():c.get_nome() for c in Service.cliente_listar()}; profissionais={p.get_id():p.get_nome() for p in Service.profissional_listar()}; servicos={s.get_id():s.get_descricao() for s in Service.servico_listar()}
        for h in Service.horario_listar():
            if hoje<=h.get_data().date()<=limite and h.get_id_cliente() is not None:
                resultado.append({'ID':h.get_id(),'Data':h.get_data().strftime('%d/%m/%Y'),'Hora':h.get_data().strftime('%H:%M'),'Cliente':clientes.get(h.get_id_cliente(),'—'),'Serviço':servicos.get(h.get_id_servico(),'—'),'Profissional':profissionais.get(h.get_id_profissional(),'—')})
        return resultado
