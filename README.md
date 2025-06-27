# Mr.HolmesCorp

**Ferramenta OSINT para consulta de informações patrimoniais em fontes públicas brasileiras**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Kali Linux](https://img.shields.io/badge/platform-Kali%20Linux-red.svg)](https://kali.org)

## 📋 Descrição

A **Mr.HolmesCorp** é uma ferramenta desenvolvida especificamente para profissionais de segurança, investigadores e pesquisadores que necessitam consultar informações patrimoniais e pessoais em fontes públicas governamentais brasileiras.

A ferramenta automatiza consultas em múltiplas bases de dados oficiais, fornecendo um relatório consolidado das informações encontradas.

## 🎯 Características

- ✅ **Consultas Automatizadas** em múltiplas fontes governamentais
- ✅ **API do Banco Central** integrada para valores a receber
- ✅ **Receita Federal** via ReceitaWS para dados empresariais
- ✅ **Portal da Transparência** para informações governamentais
- ✅ **Múltiplos Estados** (SP, PR, SC) com fontes específicas
- ✅ **Relatórios em JSON** para análise posterior
- ✅ **Interface de linha de comando** intuitiva
- ✅ **Tratamento robusto de erros** e timeouts

## 🗂️ Fontes de Dados Integradas

### 🏛️ **Federais**
- Receita Federal (CNPJ/CPF)
- Banco Central (Valores a Receber)
- Portal da Transparência
- Caixa Econômica Federal (Benefícios)
- Ministério da Cidadania (Auxílio Emergencial)
- SINESP Cidadão
- Dados Abertos Governamentais

### 🏢 **Estaduais**
- **São Paulo**: Polícia Civil (RG), Transparência
- **Paraná**: DETRAN, PROCON
- **Santa Catarina**: Dados Abertos

### 📊 **Repositórios de Dados**
- dados.gov.br
- brasil.io
- IBICT
- Dados abertos de ministérios

## 🚀 Instalação no Kali Linux

### Pré-requisitos
```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

### Instalação
```bash
# Clonar o repositório
git clone https://github.com/cyberrobot2/Mr.HolmesCorp.git
cd Mr.HolmesCorp.git

# Instalar dependências
pip3 install -r requirements.txt

# Tornar o script executável
chmod +x Mr.HolmesCorp.py
```

### Instalação Global (Opcional)
```bash
# Criar link simbólico para uso global
sudo ln -s $(pwd)/patrimonio_consultor.py /usr/local/bin/patrimonio-consultor

# Agora você pode usar de qualquer lugar:
patrimonio-consultor --help
```

## 💻 Como Usar

### Sintaxe Básica
```bash
python3 Mr.HolmesCorp.py <IDENTIFICADOR> --tipo <TIPO> [OPÇÕES]
```

### Exemplos Práticos

#### 🏢 Consultar CNPJ
```bash
# Consulta básica de CNPJ
python3 Mr.HolmesCorp.py 11222333000181 --tipo cnpj

# Consulta com relatório personalizado
python3 Mr.HolmesCorp.py 11222333000181 --tipo cnpj -o empresa_relatorio.json

# Consulta verbose (detalhada)
python3 Mr.HolmesCorp.py 11222333000181 --tipo cnpj -v
```

#### 👤 Consultar CPF
```bash
# Consulta de CPF (benefícios, valores a receber, etc.)
python3 Mr.HolmesCorp.py 12345678901 --tipo cpf

# Salvar em arquivo específico
python3 Mr.HolmesCorp.py 12345678901 --tipo cpf -o pessoa_relatorio.json
```

#### 🔍 Consultar por Nome
```bash
# Busca por nome em registros públicos
python3 Mr.HolmesCorp.py "João Silva Santos" --tipo nome
```

#### 🆔 Consultar RG (São Paulo)
```bash
python3 Mr.HolmesCorp.py 123456789 --tipo rg
```

#### 🚗 Consultar Placa Veicular
```bash
python3 Mr.HolmesCorp.py ABC1234 --tipo placa
```

#### 📋 Listar Todas as Fontes
```bash
python3 Mr.HolmesCorp.py dummy --tipo cnpj --listar-fontes
```

## 📁 Estrutura dos Relatórios

Os relatórios são gerados em formato JSON com a seguinte estrutura:

```json
{
  "identificador": "11222333000181",
  "tipo": "cnpj",
  "timestamp": "2025-06-27T10:30:00",
  "fontes": {
    "receitaws": {
      "fonte": "ReceitaWS",
      "cnpj": "11.222.333/0001-81",
      "razao_social": "Empresa Exemplo LTDA",
      "situacao": "ATIVA"
    },
    "bcb_valores": {
      "fonte": "Banco Central - Valores a Receber",
      "valores": [...]
    }
  },
  "urls_referencias": {
    "portal_transparencia": "https://portaldatransparencia.gov.br/",
    "bcb_valores": "https://valoresareceber.bcb.gov.br/publico/"
  }
}
```

## ⚙️ Opções da Linha de Comando

| Opção | Descrição |
|-------|-----------|
| `identificador` | CNPJ, CPF, Nome, RG ou Placa para consulta |
| `--tipo` | Tipo de consulta: `cnpj`, `cpf`, `nome`, `rg`, `placa` |
| `--output`, `-o` | Arquivo de saída personalizado |
| `--verbose`, `-v` | Modo detalhado com saída completa |
| `--listar-fontes` | Lista todas as fontes de dados disponíveis |
| `--help` | Exibe ajuda completa |

## 🔧 Configuração Avançada

### Personalizar Timeouts
Edite o arquivo `Mr.HolmesCorp.py.py` e modifique:
```python
response = self.session.get(url, timeout=30)  # Alterar valor conforme necessário
```

### Adicionar Novas Fontes
1. Adicione a URL no dicionário `self.urls`
2. Crie uma nova função `consultar_nova_fonte()`
3. Integre na função `buscar_completa()`

## 🛡️ Considerações de Segurança

- ⚠️ **Use apenas para fins legítimos** e em conformidade com a legislação
- ⚠️ **Respeite os termos de uso** de cada fonte de dados
- ⚠️ **Não abuse das APIs** - implemente delays entre consultas se necessário
- ⚠️ **Dados sensíveis** devem ser tratados com cuidado e responsabilidade

## 🐛 Troubleshooting

### Problemas Comuns

#### Erro de Dependências
```bash
# Instalar pip se necessário
sudo apt install python3-pip

# Atualizar pip
pip3 install --upgrade pip

# Reinstalar requests
pip3 install --force-reinstall requests
```

#### Timeout nas Consultas
```bash
# Verificar conectividade
ping google.com

# Testar com verbose para debug
python3 Mr.HolmesCorp.py 11222333000181 --tipo cnpj -v
```

#### Permissões Negadas
```bash
# Verificar permissões do arquivo
ls -la Mr.HolmesCorp.py

# Corrigir permissões
chmod +x Mr.HolmesCorp.py
```

## 📝 Logs e Debug

Para debug avançado, modifique o código para incluir logs:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFonte`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova fonte XYZ'`)
4. Push para a branch (`git push origin feature/NovaFonte`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚖️ Disclaimer Legal

Esta ferramenta é destinada apenas para consultas em fontes públicas e deve ser usada em conformidade com todas as leis aplicáveis. Os desenvolvedores não se responsabilizam pelo uso inadequado da ferramenta.

## 📞 Suporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/SEU_USUARIO/patrimonio-consultor-brasil/issues)
- 📧 **Email**: seu.email@exemplo.com
- 💬 **Discussões**: [GitHub Discussions](https://github.com/SEU_USUARIO/patrimonio-consultor-brasil/discussions)

## 🙏 Agradecimentos

- Receita Federal do Brasil
- Banco Central do Brasil  
- Portal da Transparência
- Comunidade OSINT Brasil

---

**⭐ Se esta ferramenta foi útil, não esqueça de dar uma estrela no projeto!**
