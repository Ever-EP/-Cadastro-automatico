from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoPreenchimento:
    def __init__(self):
        self.dados_pessoais = {
            'nome': 'Seu Nome',
            'email': 'seu.email@exemplo.com',
            'telefone': '(11) 99999-9999',
            'cpf': '123.456.789-00',
            'endereco': 'Sua Rua, 123',
            'cidade': 'Sua Cidade',
            'estado': 'SP',
            'cep': '12345-678'
        }
        
        # Inicializa o navegador Chrome
        self.driver = webdriver.Chrome()
        
    def preencher_formulario(self, url):
        self.driver.get(url)
        
        # Dicionário com mapeamento comum de IDs/names de campos
        campos_comuns = {
            'nome': ['nome', 'name', 'fullname', 'full-name'],
            'email': ['email', 'e-mail', 'mail'],
            'telefone': ['telefone', 'phone', 'tel', 'celular'],
            'cpf': ['cpf', 'document', 'documento'],
            'endereco': ['endereco', 'address', 'street'],
            'cidade': ['cidade', 'city'],
            'estado': ['estado', 'state', 'uf'],
            'cep': ['cep', 'zip', 'postal-code']
        }
        
        # Tenta encontrar e preencher cada campo
        for campo, valores in self.dados_pessoais.items():
            for identificador in campos_comuns[campo]:
                try:
                    # Tenta encontrar por ID
                    elemento = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.ID, identificador))
                    )
                    elemento.send_keys(valores)
                    break
                except:
                    try:
                        # Tenta encontrar por name
                        elemento = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.NAME, identificador))
                        )
                        elemento.send_keys(valores)
                        break
                    except:
                        continue
    
    def fechar(self):
        self.driver.quit()

# Exemplo de uso
if __name__ == "__main__":
    auto = AutoPreenchimento()
    
    # Lista de sites para preencher
    sites = [
        "https://exemplo1.com/cadastro",
        "https://exemplo2.com/registro"
    ]
    
    # Preenche formulários em cada site
    for site in sites:
        try:
            auto.preencher_formulario(site)
            print(f"Formulário preenchido com sucesso: {site}")
        except Exception as e:
            print(f"Erro ao preencher formulário em {site}: {str(e)}")
    
    auto.fechar() 