# Publicar a branch sem alterar diretamente a main

O repositório remoto foi apenas lido nesta sessão. A conexão retornou `pull=true` e `push=false`. Nenhuma tentativa de contornar permissões foi feita. O histórico local deriva do commit oficial `0b75aabbb866bcfeb8a565665c643164e2ed6a51` e está na branch `codex/pessoa2-validacao`.

O pacote de entrega inclui `tgb_pessoa2_validado.bundle`, com os commits locais e a referência da main inspecionada. Para importar em um clone do repositório oficial:

```bash
git fetch /caminho/tgb_pessoa2_validado.bundle codex/pessoa2-validacao:codex/pessoa2-validacao
git switch codex/pessoa2-validacao
git log --oneline -3
git diff main...codex/pessoa2-validacao --stat
git push origin codex/pessoa2-validacao
```

Revisar as mudanças antes de abrir o pull request. Não há force push nem alteração direta de main nesses comandos. Se já existir uma branch com esse nome, inspecionar sua origem antes de atualizar. Não sobrescrever o trabalho de outra pessoa.

Alternativamente, copiar o conteúdo da pasta do projeto no ZIP para uma nova branch local do clone oficial. Preservar README anterior e docs/baselines. O JAR em tools é ignorado pelo Git, mas está incluído no ZIP para execução imediata e pode ser recuperado pelo script de download com conferência de hash.

Após o push, executar o workflow na aba Actions e guardar o link do run/artifact; a execução do GitHub Actions não foi feita nesta sessão. Conferir também o devcontainer no Codespaces. O funcionamento do motor e dos scripts headless foi validado no ambiente online da sessão, conforme docs/VALIDACAO.md.
