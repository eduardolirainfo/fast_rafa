# Diagrama de Caso de Uso

```mermaid
    graph TD
        A[Início] --> B{Tipo de Usuário}
        B -->|Empresa| C[Cadastro Empresa]
        B -->|ONG| D[Cadastro ONG]

        C --> E[Cadastrar Produtos]
        E --> F[Produto Disponível para Doação]

        D --> G[Visualizar Produtos]
        G --> H[Curtir Produtos]
        G --> I[Solicitar Produtos]

        I --> J[Chat com Empresa]
        J --> K{Definir Entrega}

        K -->|Retirada| L[ONG retira na empresa]
        K -->|Delivery| M[Empresa entrega produto]

        L --> N[Doação Concluída]
        M --> N
