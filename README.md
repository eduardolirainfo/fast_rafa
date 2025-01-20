# Criar a imagem

```bash
    docker build -t "fast_rafa" .
```
# Verificar se a imagem foi criada

```bash
    docker images
```

# Rodar o container

```bash
    docker run -it --name fast_rafa -p 8000:8000 fast_rafa:latest
```
# Parar o container

```bash
    docker stop fast_rafa
```

# Usando docker-compose

```bash
    docker-compose up
```


# Diagrama de Caso de Uso

```mermaid
    graph TD
    A[Início] --> B{Tipo de Usuário}
    B -->|Empresa| C[Cadastro Empresa]
    B -->|ONG| D[Cadastro ONG]

    %% Fluxo da Empresa
    C --> E[Configurar Perfil]
    E --> F[Definir Horários]
    F --> G[Cadastrar Usuários]

    G --> H[Área da Empresa]
    H --> I[Cadastrar Produtos]
    H --> J[Criar Eventos]
    H --> K[Gerenciar Entregas]

    I --> L[Escolher Categoria]
    L --> M[Produto Disponível]

    %% Fluxo da ONG
    D --> N[Configurar Perfil ONG]
    N --> O[Definir Horários]
    O --> P[Cadastrar Voluntários]

    P --> Q[Área da ONG]
    Q --> R[Buscar Produtos]
    Q --> S[Participar Eventos]
    Q --> T[Gerenciar Watchlist]

    %% Interação com Produtos
    R --> U[Filtrar por Categoria]
    U --> V[Visualizar Produtos]
    V --> W[Favoritar]
    V --> X[Solicitar Doação]

    %% Sistema de Chat
    X --> Y[Iniciar Chat]
    Y --> Z[Negociar Detalhes]

    %% Sistema de Entrega
    Z --> AA{Definir Entrega}
    AA -->|Retirada| AB[Agendar Retirada]
    AA -->|Delivery| AC[Agendar Entrega]

    %% Confirmação
    AB --> AD[Confirmar Horário]
    AC --> AD

    %% Finalização
    AD --> AE{Entrega Realizada?}
    AE -->|Sim| AF[Doação Concluída]
    AE -->|Não| AG[Registrar Cancelamento]
    AG --> AH[Motivo Cancelamento]

    %% Monitoramento
    AF --> AI[Atualizar Watchlist]
    AF --> AJ[Histórico de Doações]

    %% Subprocessos
    J --> AK[Definir Data/Hora]
    J --> AL[Adicionar Detalhes]

    T --> AM[Monitorar Produtos]
    T --> AN[Receber Notificações]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style AF fill:#9f9,stroke:#333,stroke-width:2px
    style AG fill:#ff9,stroke:#333,stroke-width:2px


```

# Diagrama de Entidade-Relacionamento (ER) ( Esquema Resumido )

```mermaid
erDiagram
    organizations ||--o{ users : has
    organizations ||--o{ posts : publishes
    organizations ||--o{ events : organizes
    organizations ||--o{ calendars : has
    organizations ||--o{ deliveries : handles
    organizations ||--o{ watchlists : monitors

    users ||--o{ posts : creates
    users ||--o{ events : creates
    users ||--o{ deliveries : manages
    users ||--o{ favorites : has
    users ||--o{ messages : sends
    users ||--o{ watchlists : tracked_in
    users ||--o{ message_its : participates

    categories_main ||--o{ categories : contains
    categories ||--o{ posts : categorizes

    posts ||--o{ favorites : receives
    posts ||--o{ deliveries : has
    posts ||--o{ messages : referenced_in

    message_its ||--o{ messages : contains

    organizations {
        int id PK
        string id_federal UK
        bool nao_governamental
        string url_logo UK
        string url_imagem UK
        string nome UK
        string email UK
        string telefone UK
        datetime criado_em
    }

    users {
        int id PK
        string email UK
        string username UK
        string senha_hash
        int id_organizacao FK
        bool eh_voluntario
        bool eh_gerente
        datetime criado_em
    }

    posts {
        int id PK
        bool item
        int id_organizacao FK
        int id_usuario FK
        string titulo
        int id_categoria FK
        date data_validade
        datetime criado_em
    }

    categories {
        int id PK
        int id_categoria_principal FK
        string categoria UK
        string slug UK
        datetime criado_em
    }

    deliveries {
        int id PK
        int id_postagem FK "UK"
        int id_usuario FK
        int id_organizacao FK
        int id_ong FK
        date data
        datetime criado_em
    }
```


# Diagrama de Entidade-Relacionamento (ER) ( Esquema Completo )

```mermaid
erDiagram
    organizations ||--o{ users : has
    organizations ||--o{ posts : publishes
    organizations ||--o{ events : organizes
    organizations ||--o{ calendars : has
    organizations ||--o{ deliveries : handles
    organizations ||--o{ watchlists : monitors

    users ||--o{ posts : creates
    users ||--o{ events : creates
    users ||--o{ deliveries : manages
    users ||--o{ favorites : has
    users ||--o{ messages : sends
    users ||--o{ watchlists : tracked_in
    users ||--o{ message_its : participates

    categories_main ||--o{ categories : contains
    categories ||--o{ posts : categorizes

    posts ||--o{ favorites : receives
    posts ||--o{ deliveries : has
    posts ||--o{ messages : referenced_in

    message_its ||--o{ messages : contains

    organizations {
        int id PK
        string id_federal UK
        bool nao_governamental
        string url_logo UK
        string url_imagem UK
        string nome UK
        string email UK
        string telefone UK
        datetime criado_em
    }

    users {
        int id PK
        string email UK
        string username UK
        string senha_hash
        int id_organizacao FK
        bool eh_voluntario
        bool eh_gerente
        datetime criado_em
    }

    posts {
        int id PK
        bool item
        int id_organizacao FK
        int id_usuario FK
        string titulo
        int id_categoria FK
        date data_validade
        datetime criado_em
    }

    categories {
        int id PK
        int id_categoria_principal FK
        string categoria UK
        string slug UK
        datetime criado_em
    }

    categories_main {
        int id PK
        string categoria UK
        string slug UK
        datetime criado_em
    }

    deliveries {
        int id PK
        int id_postagem FK "UK"
        int id_usuario FK
        int id_organizacao FK
        int id_ong FK
        date data
        datetime criado_em
    }

    events {
        int id PK
        int id_organizacao FK
        int id_usuario FK
        string titulo
        string slug
        datetime data
        datetime criado_em
    }

    calendars {
        int id PK
        int id_organizacao FK "UK"
        datetime abertura
        datetime fechamento
        datetime criado_em
    }

    watchlists {
        int id PK
        int id_organizacao FK
        int id_usuario FK
        string endereco_ip
        int quantidade
        datetime criado_em
    }

    message_its {
        int id PK
        int usuario_um FK
        int usuario_dois FK
        datetime criado_em
    }

    messages {
        int id PK
        int id_mensagem_it FK
        int id_remetente FK
        int id_postagem FK
        string conteudo
        datetime criado_em
    }

    favorites {
        int id PK
        int id_postagem FK
        int id_usuario FK
        datetime criado_em
    }
```
