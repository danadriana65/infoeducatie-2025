import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_weekly_progress():
    # Zilele săptămânii
    zile = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă', 'Duminică']
    
    # Date simulate (le poți înlocui cu valorile reale din user_progress + timp)
    intrebari_corecte = np.array([3, 5, 2, 4, 6, 3, 7])
    timp_alocat = np.array([30, 45, 20, 35, 60, 25, 50])  # în minute

    # DataFrame pentru organizare
    df = pd.DataFrame({
        'Ziua': zile,
        'Întrebări Corecte': intrebari_corecte,
        'Timp Alocat (min)': timp_alocat
    })

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Ziua'], df['Întrebări Corecte'], marker='o', label='✅ Întrebări Corecte', color='#6A0DAD')
    plt.plot(df['Ziua'], df['Timp Alocat (min)'], marker='s', label='🕒 Timp Alocat (min)', color='#1E90FF')
    
    plt.title('Progresul săptămânal al utilizatorului', fontsize=14)
    plt.xlabel('Ziua')
    plt.ylabel('Valoare')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Salvăm graficul
    plt.savefig('weekly_progress_time_allocation.png')
    plt.show()
