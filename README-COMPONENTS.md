# Winlator Components — branch `components` do WinlatorComponents

Branch pública de componentes Winlator, independente da `main`.

## Estrutura
- `packages/vkd3d/`: coloque aqui o `.wcp` de VKD3D (TAR/XZ contendo `profile.json`).
- `packages/turnip/`: coloque aqui o ZIP Adrenotools da Turnip GameHub (`meta.json` e bibliotecas ARM64 `.so`).
- `contents.json`: catálogo remoto para WCPs VKD3D. **Está vazio até a publicação do primeiro WCP.**
- `scripts/pack_vkd3d.py`: cria um WCP instalável a partir do ZIP de DLLs do VKD3D.
- `scripts/update_contents.py`: gera o catálogo com links para arquivos realmente presentes.

## VKD3D Gamesir 3.1.0
O pacote corrigido disponibilizado no chat é `VKD3D-3.1.0-Gamesir-FIX.wcp`; **não foi publicado na branch ainda**. Faça upload desse WCP em `packages/vkd3d/`.

Para recriar a partir do ZIP original, com o Python:

```sh
python3 scripts/pack_vkd3d.py vkd3d-3.1.0-Gamesir.zip packages/vkd3d/VKD3D-3.1.0-Gamesir.wcp
python3 scripts/update_contents.py
```

Ao fazer upload do WCP em `packages/vkd3d/`, o GitHub Actions da branch tentará atualizar o `contents.json` automaticamente. A URL para configurar como catálogo de componentes em Winlator que aceitem servidor customizado é:

```text
https://raw.githubusercontent.com/erickmendes22/WinlatorComponents/components/contents.json
```

O catálogo só disponibiliza versões indexadas e efetivamente publicadas; por enquanto retorna `[]`. Se o GitHub Actions não estiver habilitado, execute `python3 scripts/update_contents.py` localmente e faça commit do catálogo.

## Turnip GameHub
A Turnip não deve ser publicada como tipo VKD3D. Envie o **ZIP compatível com Adrenotools** para `packages/turnip/` e importe-o no gerenciador de drivers gráficos (ou configure um catálogo específico, caso seu fork suporte). Não está na branch ainda porque o ZIP não foi anexado nesta conversa.

A biblioteca do GameHub pode depender de componentes adicionais. A importação depende do driver e da compatibilidade com o Winlator; é preciso validar antes de chamar o ZIP de instalável.

A branch não modifica os fontes do Winlator nem a branch `main` do repositório.
