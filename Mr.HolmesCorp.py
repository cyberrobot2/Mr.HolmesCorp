#!/usr/bin/env python3
"""
Ferramenta para consulta de informações patrimoniais em fontes públicas
Desenvolvido para uso em Kali Linux
Autor: Claude Assistant
Versão: 2.0 - Integração com múltiplas fontes governamentais
"""

import requests
import json
import time
import argparse
import sys
from datetime import datetime
import csv
from typing import Dict, List, Optional
import re
from urllib.parse import urlencode


class PatrimonioConsultor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # URLs das fontes de dados
        self.urls = {
            'caixa_programas': 'https://www.caixa.gov.br/programas-sociais/Paginas/default.aspx',
            'caixa_beneficios': 'https://www.beneficiossociais.caixa.gov.br/consulta/beneficio/04.01.00-00_00.asp',
            'auxilio_emergencial': 'https://consultaauxilio.cidadania.gov.br/consulta/#/',
            'receita_cnpj': 'http://www.receita.fazenda.gov.br/PessoaJuridica/CNPJ/cnpjreva/Cnpjreva_Solicitacao.asp',
            'bcb_valores': 'https://valoresareceber.bcb.gov.br/publico/',
            'bcb_api': 'https://valoresareceber.bcb.gov.br/publico/rest/valoresAReceber/',
            'omnisci_demo': 'https://www.omnisci.com/demos/tweetmap',
            'scan_user_repo': 'https://github.com/faciltech/scan-user',
            'osint_brasil_repo': 'https://github.com/felipeluan20/OSINTKit-Brasil',
            'dados_gov': 'https://dados.gov.br/home',
            'brasil_io': 'https://brasil.io/datasets/',
            'ibict_dados': 'https://dados.ibict.br/dataset',
            'bcb_dados': 'https://dadosabertos.bcb.gov.br/dataset',
            'turismo_dados': 'https://dados.turismo.gov.br/dataset/',
            'mj_dados': 'https://dados.mj.gov.br/dataset',
            'sc_dados': 'https://dados.sc.gov.br/',
            'sp_policia_rg': 'https://www.policiacivil.sp.gov.br/portal/faces/pages_home/servicos/consultaSituacaoRG',
            'sp_transparencia': 'https://www.transparencia.sp.gov.br/home/servidor',
            'receita_cnpj_oficial': 'https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp',
            'receita_cpf': 'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp',
            'sinesp_cidadao': 'https://www.gov.br/pt-br/apps/sinesp-cidadao',
            'falecidos_brasil': 'https://www.falecidosnobrasil.org.br/index.php',
            'pessoa_desaparecida': 'https://www.gov.br/pt-br/servicos/consultar-pessoa-desaparecida',
            'portal_transparencia': 'https://portaldatransparencia.gov.br/',
            'juntas_comerciais': 'https://www.gov.br/empresas-e-negocios/pt-br/drei/juntas-comerciais',
            'bcb_oficial': 'https://www.bcb.gov.br/',
            'detran_pr': 'https://www.detran.pr.gov.br/',
            'procon_pr': 'https://www.procon.pr.gov.br/'
        }

    def consultar_cnpj_receitaws(self, cnpj: str) -> Dict:
        """
        Consulta informações de empresa via CNPJ na ReceitaWS (API pública)
        """
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj_limpo) != 14:
            return {"erro": "CNPJ deve ter 14 dígitos"}

        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"

        try:
            response = self.session.get(url, timeout=30)
            data = response.json()

            if response.status_code == 200 and data.get('status') == 'OK':
                return {
                    "fonte": "ReceitaWS",
                    "cnpj": data.get('cnpj'),
                    "razao_social": data.get('nome'),
                    "nome_fantasia": data.get('fantasia'),
                    "situacao": data.get('situacao'),
                    "capital_social": data.get('capital_social'),
                    "endereco": {
                        "logradouro": data.get('logradouro'),
                        "numero": data.get('numero'),
                        "bairro": data.get('bairro'),
                        "municipio": data.get('municipio'),
                        "uf": data.get('uf'),
                        "cep": data.get('cep')
                    },
                    "atividade_principal": data.get('atividade_principal', []),
                    "atividades_secundarias": data.get('atividades_secundarias', []),
                    "socios": data.get('qsa', []),
                    "url_fonte": url
                }
            else:
                return {"erro": data.get('message', 'Erro na consulta'), "url_fonte": url}

        except Exception as e:
            return {"erro": f"Erro na requisição: {str(e)}", "url_fonte": url}

    def consultar_valores_receber_bcb(self, cpf_cnpj: str) -> Dict:
        """
        Consulta valores a receber no Banco Central
        """
        documento_limpo = ''.join(filter(str.isdigit, cpf_cnpj))

        # Formato da API do BCB para valores a receber
        url = f"{self.urls['bcb_api']}{documento_limpo}/1960-12-01"

        try:
            response = self.session.get(url, timeout=30)

            if response.status_code == 200:
                try:
                    data = response.json()
                    return {
                        "fonte": "Banco Central - Valores a Receber",
                        "documento": documento_limpo,
                        "valores": data,
                        "url_fonte": url,
                        "url_portal": self.urls['bcb_valores']
                    }
                except:
                    return {
                        "fonte": "Banco Central - Valores a Receber",
                        "documento": documento_limpo,
                        "status": "Resposta recebida mas não é JSON válido",
                        "url_fonte": url,
                        "url_portal": self.urls['bcb_valores']
                    }
            else:
                return {
                    "erro": f"Status HTTP: {response.status_code}",
                    "url_fonte": url,
                    "url_portal": self.urls['bcb_valores']
                }

        except Exception as e:
            return {
                "erro": f"Erro na requisição: {str(e)}",
                "url_fonte": url,
                "url_portal": self.urls['bcb_valores']
            }

    def consultar_portal_transparencia(self, termo: str, tipo: str = "pessoa") -> Dict:
        """
        Consulta no Portal da Transparência
        """
        try:
            # Simulação de consulta - implementar com APIs reais quando disponíveis
            return {
                "fonte": "Portal da Transparência",
                "termo_busca": termo,
                "tipo": tipo,
                "status": "Consulta estruturada - implementar com API oficial",
                "url_portal": self.urls['portal_transparencia'],
                "observacao": "Acessar manualmente o portal para consultas específicas"
            }
        except Exception as e:
            return {
                "erro": f"Erro na consulta: {str(e)}",
                "url_portal": self.urls['portal_transparencia']
            }

    def consultar_caixa_beneficios(self, cpf: str) -> Dict:
        """
        Estrutura para consulta de benefícios sociais da Caixa
        """
        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        return {
            "fonte": "Caixa Econômica Federal - Benefícios Sociais",
            "cpf": cpf_limpo,
            "status": "Consulta manual necessária",
            "url_programas": self.urls['caixa_programas'],
            "url_beneficios": self.urls['caixa_beneficios'],
            "observacao": "Acessar os portais da Caixa para consulta manual"
        }

    def consultar_auxilio_emergencial(self, cpf: str) -> Dict:
        """
        Estrutura para consulta do auxílio emergencial
        """
        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        return {
            "fonte": "Auxílio Emergencial - Ministério da Cidadania",
            "cpf": cpf_limpo,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['auxilio_emergencial'],
            "observacao": "Acessar o portal para consulta manual do auxílio"
        }

    def consultar_receita_federal(self, documento: str, tipo: str) -> Dict:
        """
        Estrutura para consultas na Receita Federal
        """
        documento_limpo = ''.join(filter(str.isdigit, documento))

        if tipo == "cnpj":
            url_consulta = self.urls['receita_cnpj_oficial']
        else:
            url_consulta = self.urls['receita_cpf']

        return {
            "fonte": "Receita Federal do Brasil",
            "documento": documento_limpo,
            "tipo": tipo,
            "status": "Consulta manual necessária",
            "url_consulta": url_consulta,
            "observacao": "Acessar o portal da Receita Federal para consulta oficial"
        }

    def consultar_sp_policia_rg(self, rg: str) -> Dict:
        """
        Estrutura para consulta de RG na Polícia Civil de SP
        """
        return {
            "fonte": "Polícia Civil de São Paulo",
            "rg": rg,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['sp_policia_rg'],
            "observacao": "Acessar o portal da Polícia Civil de SP para consulta do RG"
        }

    def consultar_sp_transparencia(self, nome: str) -> Dict:
        """
        Estrutura para consulta de servidores públicos de SP
        """
        return {
            "fonte": "Transparência São Paulo - Servidores",
            "nome": nome,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['sp_transparencia'],
            "observacao": "Acessar o portal para consulta de servidores públicos de SP"
        }

    def consultar_sinesp_cidadao(self, placa: str = None) -> Dict:
        """
        Estrutura para consulta no SINESP Cidadão
        """
        return {
            "fonte": "SINESP Cidadão",
            "placa": placa,
            "status": "Aplicativo necessário",
            "url_info": self.urls['sinesp_cidadao'],
            "observacao": "Baixar o aplicativo SINESP Cidadão para consultas"
        }

    def consultar_falecidos_brasil(self, nome: str) -> Dict:
        """
        Estrutura para consulta de falecidos no Brasil
        """
        return {
            "fonte": "Falecidos no Brasil",
            "nome": nome,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['falecidos_brasil'],
            "observacao": "Acessar o site para consulta de registros de óbito"
        }

    def consultar_pessoa_desaparecida(self, nome: str) -> Dict:
        """
        Estrutura para consulta de pessoas desaparecidas
        """
        return {
            "fonte": "Consulta Pessoa Desaparecida - Gov.br",
            "nome": nome,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['pessoa_desaparecida'],
            "observacao": "Acessar o portal gov.br para consulta de pessoas desaparecidas"
        }

    def consultar_detran_pr(self, info: str) -> Dict:
        """
        Estrutura para consultas no DETRAN-PR
        """
        return {
            "fonte": "DETRAN Paraná",
            "info": info,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['detran_pr'],
            "observacao": "Acessar o portal do DETRAN-PR para consultas veiculares"
        }

    def consultar_procon_pr(self, empresa: str) -> Dict:
        """
        Estrutura para consultas no PROCON-PR
        """
        return {
            "fonte": "PROCON Paraná",
            "empresa": empresa,
            "status": "Consulta manual necessária",
            "url_consulta": self.urls['procon_pr'],
            "observacao": "Acessar o portal do PROCON-PR para consultas sobre reclamações"
        }

    def listar_fontes_dados_abertos(self) -> Dict:
        """
        Lista todas as fontes de dados abertos disponíveis
        """
        fontes_dados = {
            "dados_gov": {
                "nome": "Dados.gov.br",
                "url": self.urls['dados_gov'],
                "descricao": "Portal oficial de dados abertos do governo federal"
            },
            "brasil_io": {
                "nome": "Brasil.io",
                "url": self.urls['brasil_io'],
                "descricao": "Datasets organizados sobre o Brasil"
            },
            "ibict_dados": {
                "nome": "IBICT Dados",
                "url": self.urls['ibict_dados'],
                "descricao": "Instituto Brasileiro de Informação em Ciência e Tecnologia"
            },
            "bcb_dados": {
                "nome": "BCB Dados Abertos",
                "url": self.urls['bcb_dados'],
                "descricao": "Dados abertos do Banco Central do Brasil"
            },
            "turismo_dados": {
                "nome": "Dados Turismo",
                "url": self.urls['turismo_dados'],
                "descricao": "Dados do Ministério do Turismo"
            },
            "mj_dados": {
                "nome": "Dados MJ",
                "url": self.urls['mj_dados'],
                "descricao": "Dados do Ministério da Justiça"
            },
            "sc_dados": {
                "nome": "Dados SC",
                "url": self.urls['sc_dados'],
                "descricao": "Dados abertos do estado de Santa Catarina"
            }
        }

        return {
            "fonte": "Repositórios de Dados Abertos",
            "fontes_disponiveis": fontes_dados,
            "total_fontes": len(fontes_dados)
        }

    def listar_ferramentas_osint(self) -> Dict:
        """
        Lista ferramentas OSINT disponíveis
        """
        ferramentas = {
            "scan_user": {
                "nome": "Scan User",
                "url": self.urls['scan_user_repo'],
                "descricao": "Ferramenta para scan de usuários"
            },
            "osint_brasil": {
                "nome": "OSINT Kit Brasil",
                "url": self.urls['osint_brasil_repo'],
                "descricao": "Kit de ferramentas OSINT focado no Brasil"
            },
            "omnisci_demo": {
                "nome": "OmniSci Tweet Map",
                "url": self.urls['omnisci_demo'],
                "descricao": "Demo de visualização de dados de tweets"
            }
        }

        return {
            "fonte": "Ferramentas OSINT",
            "ferramentas_disponiveis": ferramentas,
            "total_ferramentas": len(ferramentas)
        }

    def gerar_relatorio(self, dados: Dict, arquivo: str = None) -> None:
        """
        Gera relatório das consultas realizadas
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if not arquivo:
            arquivo = f"relatorio_patrimonio_{timestamp}.json"

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        print(f"[INFO] Relatório salvo em: {arquivo}")

    def buscar_completa(self, identificador: str, tipo: str) -> Dict:
        """
        Realiza busca completa em todas as fontes disponíveis
        """
        resultados = {
            "identificador": identificador,
            "tipo": tipo,
            "timestamp": datetime.now().isoformat(),
            "fontes": {},
            "urls_referencias": self.urls
        }

        print(f"[INFO] Iniciando busca completa para {tipo}: {identificador}")

        if tipo == "cnpj":
            print("[INFO] Consultando CNPJ via ReceitaWS...")
            resultados["fontes"]["receitaws"] = self.consultar_cnpj_receitaws(identificador)

            print("[INFO] Consultando Receita Federal oficial...")
            resultados["fontes"]["receita_federal"] = self.consultar_receita_federal(identificador, "cnpj")

            print("[INFO] Consultando valores a receber BCB...")
            resultados["fontes"]["bcb_valores"] = self.consultar_valores_receber_bcb(identificador)

            print("[INFO] Consultando Portal da Transparência...")
            resultados["fontes"]["transparencia"] = self.consultar_portal_transparencia(identificador, "empresa")

        elif tipo == "cpf":
            print("[INFO] Consultando Receita Federal...")
            resultados["fontes"]["receita_federal"] = self.consultar_receita_federal(identificador, "cpf")

            print("[INFO] Consultando valores a receber BCB...")
            resultados["fontes"]["bcb_valores"] = self.consultar_valores_receber_bcb(identificador)

            print("[INFO] Consultando benefícios Caixa...")
            resultados["fontes"]["caixa_beneficios"] = self.consultar_caixa_beneficios(identificador)

            print("[INFO] Consultando auxílio emergencial...")
            resultados["fontes"]["auxilio_emergencial"] = self.consultar_auxilio_emergencial(identificador)

            print("[INFO] Consultando Portal da Transparência...")
            resultados["fontes"]["transparencia"] = self.consultar_portal_transparencia(identificador, "pessoa")

        elif tipo == "nome":
            print("[INFO] Consultando transparência SP...")
            resultados["fontes"]["sp_transparencia"] = self.consultar_sp_transparencia(identificador)

            print("[INFO] Consultando falecidos Brasil...")
            resultados["fontes"]["falecidos"] = self.consultar_falecidos_brasil(identificador)

            print("[INFO] Consultando pessoa desaparecida...")
            resultados["fontes"]["pessoa_desaparecida"] = self.consultar_pessoa_desaparecida(identificador)

        elif tipo == "rg":
            print("[INFO] Consultando RG SP...")
            resultados["fontes"]["sp_policia_rg"] = self.consultar_sp_policia_rg(identificador)

        elif tipo == "placa":
            print("[INFO] Consultando SINESP...")
            resultados["fontes"]["sinesp"] = self.consultar_sinesp_cidadao(identificador)

            print("[INFO] Consultando DETRAN-PR...")
            resultados["fontes"]["detran_pr"] = self.consultar_detran_pr(identificador)

        # Adicionar informações sobre fontes de dados abertos
        print("[INFO] Listando fontes de dados abertos...")
        resultados["fontes"]["dados_abertos"] = self.listar_fontes_dados_abertos()

        print("[INFO] Listando ferramentas OSINT...")
        resultados["fontes"]["ferramentas_osint"] = self.listar_ferramentas_osint()

        return resultados


def main():
    parser = argparse.ArgumentParser(description='Consultor de Patrimônios em Fontes Públicas v2.0')
    parser.add_argument('identificador', help='CNPJ, CPF, Nome, RG ou Placa para consulta')
    parser.add_argument('--tipo', choices=['cnpj', 'cpf', 'nome', 'rg', 'placa'], required=True,
                        help='Tipo de consulta (cnpj, cpf, nome, rg, placa)')
    parser.add_argument('--output', '-o', help='Arquivo de saída para o relatório')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    parser.add_argument('--listar-fontes', action='store_true', help='Listar todas as fontes disponíveis')

    args = parser.parse_args()

    consultor = PatrimonioConsultor()

    print("=" * 80)
    print("CONSULTOR DE PATRIMÔNIOS PÚBLICOS v2.0")
    print("Integração com múltiplas fontes governamentais")
    print("=" * 80)

    if args.listar_fontes:
        print("\n[FONTES DISPONÍVEIS]")
        for nome, url in consultor.urls.items():
            print(f"- {nome}: {url}")
        return

    try:
        resultados = consultor.buscar_completa(args.identificador, args.tipo)

        if args.verbose:
            print("\n[RESULTADOS DETALHADOS]")
            print(json.dumps(resultados, ensure_ascii=False, indent=2))
        else:
            print("\n[RESUMO DOS RESULTADOS]")
            for fonte, dados in resultados["fontes"].items():
                print(f"- {fonte}: {dados.get('status', 'Consultado')}")

        # Salvar relatório
        consultor.gerar_relatorio(resultados, args.output)

        print(f"\n[CONCLUÍDO] Consulta finalizada com sucesso!")
        print(f"Total de fontes consultadas: {len(resultados['fontes'])}")

    except KeyboardInterrupt:
        print("\n[INTERROMPIDO] Consulta cancelada pelo usuário")
    except Exception as e:
        print(f"\n[ERRO] Erro durante a execução: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()