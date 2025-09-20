# PUC - Pontifícia Universidade Católica do Rio de Janeiro

<p align="center">
  <img src="https://images.squarespace-cdn.com/content/v1/59a8480fccc5c52fff14d38a/1529026153457-7W1EX1C6VUVUNIQN0CE1/image-asset.png" alt="PUC logo" border="0" width="100px">
</p>

# MVP desenvolvido para a Sprint: Desenvolvimento Full Stack Básico do curso de Pós Graduação em Engenharia de Software da PUC-RIO

### 🚀 Desenvolvedor
- <a href="https://www.linkedin.com/in/daniel-vcosta/">Daniel Vibranovski Costa</a> - daniel.vc7@gmail.com

## 🔍 Sumário

| Tópicos|
|---|
| [Definição do Problema](#-definição-do-problema)|
| [Estrutura do Repositório](#-estrutura-do-repositório)|
| [Tecnologias Utilizadas](#-tecnologias-utilizadas)|
| [Licença/License](#-licençalicense)|
| [Referências](#-referências)|
| [Agradecimentos](#-agradecimentos)|


## 📜 Definição do Problema

A proposta deste MVP surge da necessidade de melhorar a organização de tarefas dentro de equipes em uma empresa. Atualmente, a falta de centralização e transparência pode dificultar o acompanhamento do que cada membro está executando. Com a solução, cada usuário poderá visualizar não apenas suas próprias tarefas, mas também as dos demais integrantes do time, promovendo colaboração, alinhamento de prioridades e maior eficiência no fluxo de trabalho.

O presente MVP tem como meta desenvolver um Kanban funcional, estruturado por meio da criação de uma API que fará a integração entre o back-end e o front-end. Essa API será responsável por garantir a comunicação eficiente entre as camadas da aplicação, permitindo que os dados sejam processados, armazenados e exibidos de forma clara e organizada. O resultado esperado é uma ferramenta prática e escalável para gerenciamento de tarefas, que possa evoluir conforme novas necessidades e funcionalidades forem sendo incorporadas.

Este repositório refere-se ao Projeto MVP (Minimum Viable Product) desenvolvido para a Sprint: Desenvolvimento Full Stack Básico do curso de Pós Graduação em Engenharia de Software da PUC-RIO.


## 📁 Estrutura do Repositório

- O **Back-end** do projeto está disponível em: [Back-end_MVP_1_Eng_Software](https://github.com/Vibranovski/Back-end_MVP_1_Eng_Software)  
- O **Front-end** do projeto está disponível em: [Front-end_MVP_1_Eng_Software](https://github.com/Vibranovski/Front-end_MVP_1_Eng_Software)  

```
├── 📁 Back-end_MVP_1_Eng_Software
│   ├── 🐍 back_end.py
│   └── 🗄️ database.db
│
├── 📁 Front-end_MVP_1_Eng_Software
│   ├── 🌐 index.html
│   ├── 🎨 style.css
│   └── ⚡ script.js
```

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:  

- **README.md**: Arquivo que serve como guia e explicação geral sobre o projeto (arquivo atual).
- **Back-end_MVP_1_Eng_Software**: Diretório responsável pela lógica do servidor e banco de dados.  
  - **back_end.py**: Arquivo Python que implementa a API do back-end.  
  - **database.db**: Banco de dados SQLite utilizado pelo projeto.  
- **Front-end_MVP_1_Eng_Software**: Diretório responsável pela interface do usuário.  
  - **index.html**: Estrutura principal da aplicação web.  
  - **style.css**: Estilos e layout da aplicação.  
  - **script.js**: Lógica de interação e comunicação com a API.  



## 👨‍💻 Tecnologias Utilizadas

Bibliotecas:  

- [Flasgger](https://pypi.org/project/flasgger/0.5.4/): Utilizada para gerar automaticamente a documentação da API no formato Swagger, facilitando testes e visualização dos endpoints.  
- [Flask](https://flask.palletsprojects.com/en/stable/): Framework leve e flexível para criação do back-end da aplicação e definição das rotas da API.  
- [Flask-CORS](https://pypi.org/project/flask-cors/): Responsável por habilitar o compartilhamento de recursos entre diferentes origens (CORS), permitindo que o front-end acesse a API sem bloqueios.  

Linguagens:

- [HTML5](https://pt.wikipedia.org/wiki/HTML5): Linguagem de marcação usada para estruturar o conteúdo e os elementos da interface do usuário.  
- [CSS3](https://www.w3schools.com/css/): Linguagem de estilo utilizada para definir o design, layout e aparência visual da aplicação.  
- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript): Linguagem de programação responsável por implementar a lógica do front-end e interações dinâmicas.  
- [Python3](https://www.python.org/): Linguagem de programação utilizada no back-end para construir a API, conectar ao banco de dados e processar as regras de negócio.  


## ⬇️ Instruções para Execução do Projeto

### 1️⃣ Executando o Back-end

1. Acesse a pasta do back-end:

   ```bash
   cd .\Back-end_MVP_1_Eng_Software\
   ```

Inicie o servidor executando o arquivo principal:

   ```bash
   python back_end.py
   ```

### 2️⃣ Executando o Front-end

O front-end pode ser aberto diretamente no navegador.

Caso utilize a opção "Go Live" (recurso do VS Code), o sistema será iniciado automaticamente no link:
👉 [http://127.0.0.1:5500/Front-end_MVP_1_Eng_Software/](http://127.0.0.1:5500/Front-end_MVP_1_Eng_Software/)

Observação: A extensão Go Live não é obrigatória; está sendo utilizada apenas por conveniência.

### 3️⃣ Acessando a API via Swagger

Após executar o back-end, a documentação interativa da API poderá ser acessada em:
👉 [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)


## 📋 Licença/License

</a> is 
licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>


## 🎓 Referências



## 🙏 Agradecimentos

Agradeço à PUC-RIO e aos meus professores pela oportunidade de fazer esse MVP a partir da Sprint: Desenvolvimento Full Stack Básico do curso de Pós Graduação em Engenharia de Software da PUC-RIO
