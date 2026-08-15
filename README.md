# Jogo da Adivinhação

Jogo desktop desenvolvido em Python no qual o jogador precisa descobrir um número secreto entre 1 e 100. A partida oferece três tentativas, dicas progressivas, indicação de temperatura e cronômetro.

## Funcionalidades

- número secreto gerado aleatoriamente;
- três tentativas por partida;
- validação de números entre 1 e 100;
- bloqueio de palpites repetidos;
- dicas sobre faixa numérica e paridade;
- indicação de temperatura: frio, morno, quente ou muito quente;
- cronômetro da partida;
- confirmação pelo botão ou pela tecla `Enter`;
- reinício sem precisar fechar a aplicação.

## Tecnologias

- Python 3.10 ou superior;
- Tkinter;
- CustomTkinter.

## Instalação

Clone o repositório e acesse sua pasta:

```bash
git clone https://github.com/lucianofreire29/jogo-adivinhacao.git
cd jogo-adivinhacao
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale a dependência:

```bash
pip install -r requirements.txt
```

## Execução

```bash
python jogo_adivinhacao.py
```

## Como jogar

1. Clique em **Iniciar**.
2. Digite um número entre 1 e 100.
3. Confirme o palpite pelo botão ou pressione `Enter`.
4. Use as dicas e a temperatura para encontrar o número secreto.
5. Clique em **Reiniciar** para começar uma nova partida.

## Autor

**Luciano Freire**

- GitHub: [@lucianofreire29](https://github.com/lucianofreire29)
