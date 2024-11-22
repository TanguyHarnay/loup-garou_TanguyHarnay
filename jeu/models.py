from django.db import models

class Lieu(models.Model):
    id_lieu = models.CharField(max_length=100, primary_key=True)
    nom = models.CharField(max_length=100)
    disponibilite = models.CharField(max_length=20, default='libre')
    taille_max = models.IntegerField(default=1)

    def __str__(self):
        return self.nom

class Personnage(models.Model):
    ROLES = [
        ('villageois', 'Villageois'),
        ('loup_garou', 'Loup-Garou'),
        ('sorciere', 'Sorcière'),
        ('garde', 'Garde'),
    ]

    ETATS = [
        ('vivant', 'Vivant'),
        ('mort', 'Mort'),
        ('endormi', 'Endormi'),
    ]

    id_personnage = models.CharField(max_length=100, primary_key=True)
    role = models.CharField(max_length=20, choices=ROLES)
    etat = models.CharField(max_length=20, choices=ETATS, default='vivant')
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    est_protege = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id_personnage} ({self.role})"
    
    def casser_bouclier(self):
        """ Casse la protection, rendant la personne vulnérable """
        self.est_protege = False
        self.save()

class Cycle(models.Model):
    periode = models.CharField(max_length=10, choices=[('jour', 'Jour'), ('nuit', 'Nuit')], default='jour')

    def __str__(self):
        return self.get_periode_display()
    def basculer_cycle(self):
        """Bascule entre jour et nuit."""
        self.periode = 'nuit' if self.periode == 'jour' else 'jour'
        self.save()