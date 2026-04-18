# TDD Snake Game 🐍

Um jogo de Snake clássico desenvolvido seguindo rigorosamente as práticas de **TDD (Test Driven Development)** e **Clean Architecture**.

## ✨ Funcionalidades

- **Movimentação Clássica**: Controle a cobra usando as teclas `W`, `A`, `S`, `D`.
- **Modo Wrap-Around**: A cobra pode atravessar as bordas da tela e reaparecer no lado oposto.
- **Dificuldade Progressiva**: A cada 10 pontos (segmentos do corpo), a quantidade de frutas simultâneas no mapa aumenta.
- **Detecção de Auto-Colisão**: O jogo termina se a cobra colidir com o próprio corpo (exceto o segmento da cauda que está saindo no mesmo frame).
- **Interface Estável**: Renderização otimizada para terminal usando sequências de escape ANSI (sem "flicker").

## 🏗️ Estrutura do Projeto

O código foi refatorado para separar as responsabilidades:

- `snake.py`: Entidade de domínio que gerencia o corpo e movimento da cobra.
- `game_engine.py`: Motor do jogo que gerencia frutas, score e regras de negócio.
- `snake_screen.py`: Infraestrutura de IO (Input/Output) e loop principal.
- `teste_snake.py`: Suíte de testes automatizados com Pytest.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior.
- Pytest (para rodar os testes).

### No Linux / macOS (Nativo)
O jogo utiliza os módulos `termios` e `tty` para leitura instantânea do teclado.
```bash
python3 snake_screen.py
```

### No Windows
O suporte nativo para `termios` não está disponível no Windows. Você tem duas opções:
1. **WSL (Recomendado)**: Execute o programa dentro do Windows Subsystem for Linux.
2. **Git Bash / Cygwin**: Pode funcionar dependendo da emulação de terminal.
3. **PowerShell/CMD**: O jogo precisará de uma adaptação no `io_handler` para usar a biblioteca `msvcrt` (não implementado nesta versão modular).

## 🧪 Rodando os Testes

Para garantir que todas as regras de negócio estão funcionando corretamente:
```bash
pytest teste_snake.py
```

## 🎮 Comandos
- `W`: Cima
- `A`: Esquerda
- `S`: Baixo
- `D`: Direita
- `ESC`: Sair do jogo
