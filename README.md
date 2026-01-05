# ASSISTENTE GIT

O assistente GIT tem o objetivo de facilitar e automatizar a publicação de projetos no GIT.

---
## Tecnologias Usadas

Estilização: PyQT5 e QSS (https://pypi.org/project/PyQt5/)
Resources_rc: Para incluir o ícone no favicon (veja na sessão como utilizar)

---
## Como utilizar

*Para criar*
1. Abrir o aplicativo e selecionar a pasta do projeto.
2. Clique em Criar GIT. Será necessário informar a URL criada no GIT e o texto para o primeiro commit
*Para alterar*
1. Abrir o aplicativo e selecionar a pasta do projeto.
2. Clique em Atualizar GIT. Insira o texto do commit para registro da atualização.
*Utilização do resources*
1. Necessário criar um arquivo resources.qrc e editá-lo, incluindo o caminho onde estão as imagens dentro de RCC:
**exemplo:**

```xml 
<RCC> 
	<qresource prefix="/"> 
		<file>img/favicon.png</file> 
	</qresource> 
</RCC>
```

2. No terminal, navegar até a pasta onde está o arquivo resources.qrc e executar o comando: **pyrcc5 resources.qrc -o resources_rc.py**

3. Adicionar no código python o import resources_rc

---
## Desenvolvido por:
**Daniel Boechat dos Santos**

