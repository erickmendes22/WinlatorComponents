# Turnip GameHub para Winlator

Destino dos drivers Turnip GameHub: `packages/turnip/`.

O pacote deve ser um **ZIP Adrenotools** válido, tipicamente com `meta.json` na raiz e bibliotecas `.so` ARM64. Não é o mesmo formato de um WCP de VKD3D; não adicione a Turnip a `contents.json` como se fosse VKD3D.

Antes de publicar, confira `meta.json`, arquitetura ARM64, bibliotecas, símbolos, dependências do loader e compatibilidade com o Winlator. O fato de funcionar no GameHub não garante a mesma compatibilidade fora dele.

O ZIP específico da Turnip GameHub ainda não foi publicado nesta branch. Após o upload para `packages/turnip/`, importe-o pelo gerenciador de drivers gráficos/AdrenoTools do Winlator. Alguns forks usam um catálogo de drivers separado.
