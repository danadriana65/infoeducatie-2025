import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_language_usage():
    # Stil vizual
    sns.set(style="whitegrid")

    # Date simulate — înlocuiește cu date reale din user_progress dacă vrei
    languages = ['C++', 'JavaScript', 'Python']
    correct_answers = [42, 58, 75]  # Exemplu: număr de întrebări corecte

    # Creăm DataFrame
    data = pd.DataFrame({
        'Limbaj': languages,
        'Întrebări Corecte': correct_answers
    })

    # Dimensiune și stil grafic
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Limbaj', y='Întrebări Corecte', data=data, palette='viridis')

    plt.title('Utilizarea limbajelor de programare învățate', fontsize=16)
    plt.xlabel('Limbaj de programare', fontsize=14)
    plt.ylabel('Întrebări corecte', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    # Salvăm imaginea
    output_path = "language_usage_bar_chart.png"
    plt.savefig(output_path)
    plt.close()

    print(f"✅ Grafic salvat ca '{output_path}'")
