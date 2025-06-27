#!/bin/bash

# Script de instalação automática para Kali Linux
# Patrimônio Consultor Brasil v2.0

echo "=============================================="
echo "PATRIMÔNIO CONSULTOR BRASIL - INSTALAÇÃO"
echo "=============================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logs coloridos
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se está rodando no Kali Linux
check_kali() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ $ID == "kali" ]]; then
            log_success "Kali Linux detectado: $PRETTY_NAME"
            return 0
        else
            log_warning "Sistema detectado: $PRETTY_NAME (não é Kali Linux)"
            read -p "Deseja continuar mesmo assim? (y/N): " choice
            case "$choice" in 
                y|Y ) return 0;;
                * ) exit 1;;
            esac
        fi
    else
        log_error "Não foi possível detectar o sistema operacional"
        exit 1
    fi
}

# Atualizar sistema
update_system() {
    log_info "Atualizando repositórios do sistema..."
    sudo apt update > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        log_success "Repositórios atualizados com sucesso"
    else
        log_error "Erro ao atualizar repositórios"
        exit 1
    fi
}

# Instalar dependências
install_dependencies() {
    log_info "Instalando dependências do sistema..."
    
    packages=("python3" "python3-pip" "git" "curl" "wget")
    
    for package in "${packages[@]}"; do
        if ! dpkg -l | grep -q "^ii  $package "; then
            log_info "Instalando $package..."
            sudo apt install -y $package > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                log_success "$package instalado com sucesso"
            else
                log_error "Erro ao instalar $package"
                exit 1
            fi
        else
            log_success "$package já está instalado"
        fi
    done
}

# Instalar dependências Python
install_python_deps() {
    log_info "Instalando dependências Python..."
    
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            log_success "Dependências Python instaladas com sucesso"
        else
            log_error "Erro ao instalar dependências Python"
            exit 1
        fi
    else
        log_info "Arquivo requirements.txt não encontrado, instalando requests..."
        pip3 install requests > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            log_success "Requests instalado com sucesso"
        else
            log_error "Erro ao instalar requests"
            exit 1
        fi
    fi
}

# Configurar permissões
setup_permissions() {
    log_info "Configurando permissões..."
    
    if [ -f "patrimonio_consultor.py" ]; then
        chmod +x patrimonio_consultor.py
        log_success "Permissões configuradas para patrimonio_consultor.py"
    else
        log_error "Arquivo patrimonio_consultor.py não encontrado"
        exit 1
    fi
}

# Criar link simbólico global (opcional)
create_global_link() {
    read -p "Deseja instalar globalmente? (permite usar 'patrimonio-consultor' de qualquer lugar) (y/N): " choice
    case "$choice" in 
        y|Y )
            log_info "Criando link simbólico global..."
            sudo ln -sf "$(pwd)/patrimonio_consultor.py" /usr/local/bin/patrimonio-consultor
            if [ $? -eq 0 ]; then
                log_success "Link global criado: patrimonio-consultor"
                echo -e "${GREEN}Agora você pode usar: ${YELLOW}patrimonio-consultor --help${NC}"
            else
                log_error "Erro ao criar link global"
            fi
            ;;
        * )
            log_info "Instalação local apenas"
            ;;
    esac
}

# Testar instalação
test_installation() {
    log_info "Testando instalação..."
    
    python3 patrimonio_consultor.py --help > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        log_success "Instalação testada com sucesso!"
    else
        log_error "Erro no teste da instalação"
        exit 1
    fi
}

# Exibir informações finais
show_usage_info() {
    echo ""
    echo "=============================================="
    echo -e "${GREEN}INSTALAÇÃO CONCLUÍDA COM SUCESSO!${NC}"
    echo "=============================================="
    echo ""
    echo -e "${YELLOW}EXEMPLOS DE USO:${NC}"
    echo ""
    echo -e "${BLUE}# Consultar CNPJ:${NC}"
    echo "python3 patrimonio_consultor.py 11222333000181 --tipo cnpj"
    echo ""
    echo -e "${BLUE}# Consultar CPF:${NC}"
    echo "python3 patrimonio_consultor.py 12345678901 --tipo cpf"
    echo ""
    echo -e "${BLUE}# Consultar com relatório personalizado:${NC}"
    echo "python3 patrimonio_consultor.py 11222333000181 --tipo cnpj -o relatorio.json"
    echo ""
    echo -e "${BLUE}# Modo verbose:${NC}"
    echo "python3 patrimonio_consultor.py 11222333000181 --tipo cnpj -v"
    echo ""
    echo -e "${BLUE}# Listar todas as fontes:${NC}"
    echo "python3 patrimonio_consultor.py dummy --tipo cnpj --listar-fontes"
    echo ""
    
    if [ -L "/usr/local/bin/patrimonio-consultor" ]; then
        echo -e "${YELLOW}COMANDO GLOBAL DISPONÍVEL:${NC}"
        echo "patrimonio-consultor --help"
        echo ""
    fi
    
    echo -e "${YELLOW}DOCUMENTAÇÃO COMPLETA:${NC}"
    echo "https://github.com/SEU_USUARIO/patrimonio-consultor-brasil"
    echo ""
    echo -e "${GREEN}Bom uso da ferramenta!${NC}"
}

# Função principal
main() {
    check_kali
    update_system
    install_dependencies
    install_python_deps
    setup_permissions
    create_global_link
    test_installation
    show_usage_info
}

# Executar instalação
main
