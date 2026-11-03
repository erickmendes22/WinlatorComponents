# VKD3D Gamesir 3.1.0

Coloque o pacote `.wcp` em `packages/vkd3d/`. O instalador Winlator requer um TAR/XZ com `profile.json` na raiz e entradas explícitas das pastas `system32/` e `syswow64/` antes das DLLs. Sem essas entradas, pode ocorrer `ERROR_BADTAR`.

As DLLs x64 são `system32/d3d12.dll` e `system32/d3d12core.dll`; x86 são as mesmas em `syswow64/`. O DXGI adicional não é recomendado, pois pode conflitar com DXVK.

Para empacotar o ZIP original:

```sh
python3 scripts/pack_vkd3d.py vkd3d-3.1.0-Gamesir.zip packages/vkd3d/VKD3D-3.1.0-Gamesir.wcp
```

Após enviar o WCP ao GitHub, gere e faça commit do catálogo com `python3 scripts/update_contents.py`.
