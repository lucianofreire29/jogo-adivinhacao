"""Jogo de adivinhação com interface gráfica em CustomTkinter."""

import random
import time
import tkinter as tk

import customtkinter as ctk

NUMERO_MINIMO = 1
NUMERO_MAXIMO = 100
TOTAL_TENTATIVAS = 3

COR_INICIAL = "#b1f7f3"
COR_JOGO = "#f0f8ff"
COR_VITORIA = "#90ee90"


class JogoAdivinhacao(ctk.CTk):
    """Janela principal e regras do jogo."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Jogo da Adivinhação")
        self.geometry("800x650")
        self.minsize(700, 600)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.frame_atual: ctk.CTkFrame | None = None
        self.cronometro_id: str | None = None
        self.jogo_ativo = False

        self.mostrar_tela_inicial()

    def limpar_tela(self) -> None:
        """Cancela tarefas pendentes e remove a tela atual."""
        if self.cronometro_id is not None:
            self.after_cancel(self.cronometro_id)
            self.cronometro_id = None

        if self.frame_atual is not None:
            self.frame_atual.destroy()

    def mostrar_tela_inicial(self) -> None:
        """Exibe as instruções antes do início da partida."""
        self.limpar_tela()
        self.jogo_ativo = False

        self.frame_atual = ctk.CTkFrame(self, fg_color=COR_INICIAL)
        self.frame_atual.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.frame_atual,
            text="⭐ Jogo da Adivinhação ⭐",
            font=("Helvetica", 26, "bold"),
            text_color="black",
            fg_color=COR_INICIAL,
        ).pack(pady=20)

        ctk.CTkLabel(
            self.frame_atual,
            text=(
                "Descubra o número secreto entre 1 e 100 em até 3 tentativas.\n"
                "Use as dicas estratégicas para reduzir as possibilidades.\n"
                "A cada erro, a temperatura mostra se você está perto ou longe."
            ),
            font=("Helvetica", 16),
            text_color="black",
            fg_color=COR_INICIAL,
        ).pack(pady=20)

        ctk.CTkButton(
            self.frame_atual,
            text="Iniciar",
            font=("Helvetica", 18, "bold"),
            text_color="black",
            fg_color="#0fbb0a",
            command=self.iniciar_jogo,
        ).pack(pady=30)

    def iniciar_jogo(self) -> None:
        """Cria uma nova partida e monta a interface do jogo."""
        self.limpar_tela()

        self.numero_secreto = random.randint(NUMERO_MINIMO, NUMERO_MAXIMO)
        self.tentativas = TOTAL_TENTATIVAS
        self.palpites_usados: set[str] = set()
        self.numeros_tentados: set[int] = set()
        self.dicas_usadas = 0
        self.inicio_tempo = time.monotonic()
        self.jogo_ativo = True

        self.frame_atual = ctk.CTkFrame(self, fg_color=COR_JOGO)
        self.frame_atual.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.frame_atual,
            text="Digite um número entre 1 e 100",
            font=("Helvetica", 20, "bold"),
            text_color="black",
            fg_color=COR_JOGO,
        ).pack(pady=10)

        self.label_tempo = ctk.CTkLabel(
            self.frame_atual,
            text="⏱ Tempo: 0 s",
            font=("Helvetica", 16, "bold"),
            text_color="black",
            fg_color=COR_JOGO,
        )
        self.label_tempo.pack()

        self.entry = ctk.CTkEntry(
            self.frame_atual,
            placeholder_text="Seu palpite",
            font=("Helvetica", 20),
            text_color="black",
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.verificar_palpite)
        self.entry.focus()

        ctk.CTkButton(
            self.frame_atual,
            text="Confirmar",
            font=("Helvetica", 18),
            text_color="black",
            command=self.verificar_palpite,
        ).pack(pady=10)

        self.label_resultado = self.criar_label("", 18, "bold")
        self.label_resultado.pack(pady=10)

        self.label_tentativas = self.criar_label(
            f"Tentativas restantes: {TOTAL_TENTATIVAS}", 16
        )
        self.label_tentativas.pack(pady=5)

        self.label_palpites = self.criar_label("Dicas:\n", 14)
        self.label_palpites.configure(justify="left")
        self.label_palpites.pack(pady=10)

        ctk.CTkButton(
            self.frame_atual,
            text="Dica",
            font=("Helvetica", 18, "bold"),
            text_color="black",
            fg_color="#0fbb0a",
            command=self.usar_dica,
        ).pack(pady=5)

        ctk.CTkButton(
            self.frame_atual,
            text="Reiniciar",
            font=("Helvetica", 14),
            text_color="black",
            fg_color="#ffcc00",
            command=self.iniciar_jogo,
        ).pack(pady=10)

        self.atualizar_cronometro()

    def criar_label(
        self, texto: str, tamanho: int, estilo: str = "normal"
    ) -> ctk.CTkLabel:
        """Cria um rótulo com o estilo padrão da tela de jogo."""
        return ctk.CTkLabel(
            self.frame_atual,
            text=texto,
            font=("Helvetica", tamanho, estilo),
            text_color="black",
            fg_color=COR_JOGO,
        )

    def atualizar_cronometro(self) -> None:
        """Atualiza o tempo enquanto a partida estiver ativa."""
        if not self.jogo_ativo:
            self.cronometro_id = None
            return

        tempo_atual = int(time.monotonic() - self.inicio_tempo)
        self.label_tempo.configure(text=f"⏱ Tempo: {tempo_atual} s")
        self.cronometro_id = self.after(1000, self.atualizar_cronometro)

    def atualizar_cor_da_tela(self, cor: str) -> None:
        """Aplica uma cor aos elementos que acompanham a temperatura."""
        self.frame_atual.configure(fg_color=cor)
        for componente in (
            self.label_resultado,
            self.label_tentativas,
            self.label_palpites,
            self.label_tempo,
        ):
            componente.configure(fg_color=cor)

    def atualizar_temperatura(self, diferenca: int) -> None:
        """Mostra se o palpite está perto ou longe do número secreto."""
        if diferenca <= 5:
            cor, texto = "#ff4d4d", "🔥 Muito quente!"
        elif diferenca <= 15:
            cor, texto = "#ff944d", "🔥 Quente!"
        elif diferenca <= 30:
            cor, texto = "#66b3ff", "❄ Morno..."
        else:
            cor, texto = "#3399ff", "❄ Frio!"

        self.atualizar_cor_da_tela(cor)
        self.label_resultado.configure(text=texto)

    def gerar_dica(self, tipo: str) -> str:
        """Retorna uma dica sobre o número secreto."""
        if tipo == "leve":
            return (
                "• O número está na metade inferior."
                if self.numero_secreto <= 50
                else "• O número está na metade superior."
            )

        if tipo == "medio":
            inicio = (self.numero_secreto // 10) * 10
            inicio = max(NUMERO_MINIMO, inicio)
            fim = min(NUMERO_MAXIMO, inicio + 9)
            return f"• O número está entre {inicio} e {fim}."

        return (
            "• O número é par."
            if self.numero_secreto % 2 == 0
            else "• O número é ímpar."
        )

    def usar_dica(self) -> None:
        """Exibe até três dicas progressivas durante a partida."""
        if not self.jogo_ativo:
            return

        tipos = ("leve", "medio", "forte")
        if self.dicas_usadas >= len(tipos):
            self.label_resultado.configure(text="Você já usou todas as dicas!")
            return

        dica = self.gerar_dica(tipos[self.dicas_usadas])
        self.dicas_usadas += 1

        if dica not in self.palpites_usados:
            self.palpites_usados.add(dica)
            texto_atual = self.label_palpites.cget("text")
            self.label_palpites.configure(text=f"{texto_atual}{dica}\n")

    def verificar_palpite(self, _evento: tk.Event | None = None) -> None:
        """Valida o valor informado e atualiza o estado da partida."""
        if not self.jogo_ativo:
            return

        try:
            palpite = int(self.entry.get().strip())
        except ValueError:
            self.label_resultado.configure(text="Digite um número inteiro válido!")
            self.entry.focus()
            return

        if not NUMERO_MINIMO <= palpite <= NUMERO_MAXIMO:
            self.label_resultado.configure(text="Digite um número entre 1 e 100!")
            self.limpar_entrada()
            return

        if palpite in self.numeros_tentados:
            self.label_resultado.configure(text="⚠️ Você já tentou esse número!")
            self.limpar_entrada()
            return

        self.numeros_tentados.add(palpite)

        if palpite == self.numero_secreto:
            self.finalizar_jogo(vitoria=True)
            return

        self.tentativas -= 1
        self.label_tentativas.configure(
            text=f"Tentativas restantes: {self.tentativas}"
        )
        self.atualizar_temperatura(abs(self.numero_secreto - palpite))

        if self.tentativas == 0:
            self.finalizar_jogo(vitoria=False)

        self.limpar_entrada()

    def limpar_entrada(self) -> None:
        """Limpa e devolve o foco ao campo de palpite."""
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def finalizar_jogo(self, vitoria: bool) -> None:
        """Encerra a partida e apresenta o resultado final."""
        self.jogo_ativo = False
        tempo_final = int(time.monotonic() - self.inicio_tempo)

        if vitoria:
            self.atualizar_cor_da_tela(COR_VITORIA)
            mensagem = f"🎉 Você acertou!\nTempo: {tempo_final} segundos"
        else:
            mensagem = (
                f"💀 Fim de jogo!\nO número era {self.numero_secreto}\n"
                f"Tempo: {tempo_final} segundos"
            )

        self.label_resultado.configure(text=mensagem)


def main() -> None:
    """Inicia a aplicação."""
    app = JogoAdivinhacao()
    app.mainloop()


if __name__ == "__main__":
    main()
