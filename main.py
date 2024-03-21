import tkinter as tk
from tkinter import ttk

# Définition des SLA/OLA
sla_ola = {
    "silver": {"prise_en_charge": 24, "delai_reponse": 48, "niveau": "niveau1"},
    "gold": {"prise_en_charge": 12, "delai_reponse": 24, "niveau": "niveau2"},
    "platinum": {"prise_en_charge": 2, "delai_reponse": 12, "niveau": "niveau3"}
}

# Définition des files d'attente et techniciens par niveau
files_attente = {
    "niveau1": ["file1", "file2", "file3"],
    "niveau2": ["file4", "file5"],
    "niveau3": ["file6"]
}

techniciens = {
    "niveau1": ["tech1", "tech2", "tech3"],
    "niveau2": ["tech4", "tech5", "tech6"],
    "niveau3": ["tech7", "tech8"]
}

# Matrice de priorisation
matrice = [
    {"Priorité": "1", "Impact sur l'utilisateur": "Élevé", "Urgence": "Élevée", "Complexité de la résolution": "Complexes", "Impact sur les opérations": "Majeur"},
    {"Priorité": "2", "Impact sur l'utilisateur": "Moyen", "Urgence": "Moyenne", "Complexité de la résolution": "Moyenne", "Impact sur les opérations": "Modéré"},
    {"Priorité": "3", "Impact sur l'utilisateur": "Faible", "Urgence": "Faible", "Complexité de la résolution": "Simple", "Impact sur les opérations": "Mineur"}
]

# Fonction pour déterminer la priorité, la file d'attente et le technicien
def gerer_incident(impact_utilisateur, urgence, complexite, impact_operations):
    priorite = None
    meilleure_correspondance = {}
    meilleure_correspondance_score = 0

    for ligne in matrice:
        score_correspondance = 0
        if ligne['Impact sur l\'utilisateur'] == impact_utilisateur:
            score_correspondance += 1
        if ligne['Urgence'] == urgence:
            score_correspondance += 1
        if ligne['Complexité de la résolution'] == complexite:
            score_correspondance += 1
        if ligne['Impact sur les opérations'] == impact_operations:
            score_correspondance += 1

        if score_correspondance > meilleure_correspondance_score:
            meilleure_correspondance = ligne
            meilleure_correspondance_score = score_correspondance

    priorite = meilleure_correspondance.get('Priorité', None)

    if priorite == "1":
        sla = sla_ola["platinum"]   
        file_attente = files_attente["niveau3"][0]
        technicien = techniciens["niveau3"][0]
    elif priorite == "2":
        sla = sla_ola["gold"]
        file_attente = files_attente["niveau2"][0]
        technicien = techniciens["niveau2"][0]
    elif priorite == "3":
        sla = sla_ola["silver"]
        file_attente = files_attente["niveau1"][0]
        technicien = techniciens["niveau1"][0]
    else:
        sla = None
        file_attente = None
        technicien = None

    return priorite, sla, file_attente, technicien

# Interface graphique
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion d'incidents")

        # Création des widgets
        label_impact_utilisateur = ttk.Label(self, text="Impact sur l'utilisateur :")
        label_impact_utilisateur.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.impact_utilisateur_var = tk.StringVar()
        impact_utilisateur_combobox = ttk.Combobox(self, textvariable=self.impact_utilisateur_var, values=["Faible", "Moyen", "Élevé"])
        impact_utilisateur_combobox.grid(row=0, column=1, padx=10, pady=10)

        label_urgence = ttk.Label(self, text="Urgence :")
        label_urgence.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.urgence_var = tk.StringVar()
        urgence_combobox = ttk.Combobox(self, textvariable=self.urgence_var, values=["Faible", "Moyenne", "Élevée"])
        urgence_combobox.grid(row=1, column=1, padx=10, pady=10)

        label_complexite = ttk.Label(self, text="Complexité de la résolution :")
        label_complexite.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.complexite_var = tk.StringVar()
        complexite_combobox = ttk.Combobox(self, textvariable=self.complexite_var, values=["Simple", "Moyenne", "Complexes"])
        complexite_combobox.grid(row=2, column=1, padx=10, pady=10)

        label_impact_operations = ttk.Label(self, text="Impact sur les opérations :")
        label_impact_operations.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.impact_operations_var = tk.StringVar()
        impact_operations_combobox = ttk.Combobox(self, textvariable=self.impact_operations_var, values=["Mineur", "Modéré", "Majeur"])
        impact_operations_combobox.grid(row=3, column=1, padx=10, pady=10)

        bouton_valider = ttk.Button(self, text="Valider", command=self.afficher_resultat)
        bouton_valider.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.label_resultat = ttk.Label(self, text="")
        self.label_resultat.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def afficher_resultat(self):
        impact_utilisateur = self.impact_utilisateur_var.get()
        urgence = self.urgence_var.get()
        complexite = self.complexite_var.get()
        impact_operations = self.impact_operations_var.get()

        priorite, sla, file_attente, technicien = gerer_incident(impact_utilisateur, urgence, complexite, impact_operations)

        if sla is None:
            resultat = f"Priorité : {priorite}"
        else:
            resultat = f"Priorité : {priorite}\n"
            resultat += f"SLA : {sla['niveau']} (Prise en charge dans {sla['prise_en_charge']} heures, Délai de réponse dans {sla['delai_reponse']} heures)\n"
            resultat += f"File d'attente : {file_attente}\n"
            resultat += f"Technicien assigné : {technicien} (Niveau {sla['niveau']})"

        self.label_resultat.configure(text=resultat)

if __name__ == "__main__":
    app = Application()
    app.mainloop()