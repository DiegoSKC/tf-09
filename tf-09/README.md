# TF-09 — Atalhos na árvore de arquivos

**Encapsulamento:** o destino do Atalho é privado e pode ser consultado pela property `destino`.
**Herança:** o Atalho recebe de Item o nome, o pai, o caminho e a movimentação.
**Polimorfismo:** o Atalho implementa `tamanho()` e `mostrar()` de um jeito próprio.
**Interface:** quem usa `espaco_total()` só precisa saber que cada objeto oferece `tamanho()`.