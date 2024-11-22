from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import DeplacementForm, ActionForm
from .models import Lieu, Personnage, Cycle

def liste_personnages(request):
    personnages = Personnage.objects.all()
    cycle, created = Cycle.objects.get_or_create(id=1, defaults={'periode': 'jour'})
    return render(request, 'jeu/liste_personnages.html', {'personnages': personnages, 'cycle': cycle})

def aide(request) :
    return render(request,'jeu/aide.html')

def basculer_cycle(request):
    cycle = Cycle.objects.first()  # Assurez-vous qu'il existe une instance unique
    cycle.basculer_cycle()
    messages.success(request, f"Le cycle a été basculé en {cycle.periode}.")
    return redirect('liste_personnages')  # Redirigez vers une page appropriée

def detail_personnage(request, id_personnage):
    personnage = get_object_or_404(Personnage, id_personnage=id_personnage)
    ancien_lieu = personnage.lieu
    personnages_dans_lieu = Personnage.objects.filter(lieu=ancien_lieu)

    # Récupérer l'état actuel du cycle (jour ou nuit)
    cycle = Cycle.objects.first()  # Assurez-vous d'avoir un moyen d'obtenir l'état actuel du cycle
    if cycle and cycle.periode == 'nuit':
        periode_actuelle = 'nuit'
    else:
        periode_actuelle = 'jour'

    if request.method == "POST":
        # Vérification si le personnage est mort
        if personnage.etat == 'mort':
            messages.error(request, "Un personnage mort ne peut pas effectuer d'actions.")
            return redirect('detail_personnage', id_personnage=id_personnage)

        form_deplacement = DeplacementForm(request.POST, instance=personnage)
        form_action = ActionForm(request.POST)

        if form_deplacement.is_valid():
            nouveau_lieu = form_deplacement.cleaned_data['lieu']

            # Vérification de la disponibilité du lieu
            if nouveau_lieu.disponibilite == "libre":
                nombre_occupants = Personnage.objects.filter(lieu=nouveau_lieu).count()

                if nombre_occupants >= nouveau_lieu.taille_max:
                    messages.error(request, f"Le lieu {nouveau_lieu.nom} est déjà plein.")
                    return redirect('detail_personnage', id_personnage=id_personnage)

                # Si tout est ok, déplacer le personnage
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()

                # Libérer l'ancien lieu
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

                # Enregistrer le nouveau lieu du personnage
                form_deplacement.save()

            return redirect('detail_personnage', id_personnage=id_personnage)

        if form_action.is_valid():
            action = form_action.cleaned_data['action']
            cible = form_action.cleaned_data['cible']

            if action and cible:
                # Si le loup-garou essaie de soigner
                if personnage.role == 'loup_garou' and action == 'soigner':
                    messages.error(request, "Un loup-garou ne peut pas soigner quelqu'un.")
                    return redirect('detail_personnage', id_personnage=id_personnage)
                
                if personnage.role == 'loup_garou' and action == 'proteger':
                    messages.error(request, "Un loup-garou ne peut pas proteger quelqu'un.")
                    return redirect('detail_personnage', id_personnage=id_personnage)

                # Si le personnage est un loup-garou et veut tuer
                if personnage.role == 'loup_garou' and action == 'tuer':
                    if cible.etat != 'vivant':
                        messages.error(request, "Vous ne pouvez pas tuer un personnage déjà mort.")
                    elif cible.lieu != personnage.lieu:
                        messages.error(request, "Vous ne pouvez tuer que des personnages dans le même lieu.")
                    elif periode_actuelle == 'jour' :
                        messages.error(request, "Le loup-garou ne peut tuer que la nuit")
                    elif cible.est_protege:
                        cible.casser_bouclier()
                        messages.error(request, "Le bouclier du garde a été brisé, la victime est maintenant vulnérable.")
                    else:
                        cible.etat = 'mort'
                        cible.save()
                        messages.success(request, "Le personnage a été tué.")

                # Si le personnage est une sorcière et veut soigner
                elif personnage.role == 'sorciere':
                    if action == 'soigner':
                        if cible.etat == 'vivant' :
                            messages.error(request, "Vous ne pouvez soigner qu'un personnage mort.")
                        elif periode_actuelle == 'jour' :
                            messages.error(request, "La sorcière ne peut soigner que la nuit") 
                        else :
                            cible.etat = 'vivant'
                            cible.save()
                            messages.success(request, "La sorcière a ramené ce personnage à la vie.")
                    else:
                        messages.error(request, "La sorcière ne peut que soigner.")

                # Si le personnage est un garde et veut protéger
                elif personnage.role == 'garde' and action != 'proteger':
                    messages.error(request, "Le garde ne peut que protéger.")
                elif personnage.role == 'garde' and action == 'proteger':
                    if periode_actuelle == 'jour':
                        if cible.etat == 'mort':
                            messages.error(request, "Vous ne pouvez pas protéger un personnage mort.")
                        elif cible.est_protege:
                            messages.error(request, "Ce personnage est déjà protégé.")
                        else:
                            cible.est_protege = True
                            cible.save()
                            messages.success(request, "Le garde a protégé ce personnage.")
                    else:
                        messages.error(request, "Le garde ne peut protéger que pendant la journée.")


    else:
        form_deplacement = DeplacementForm()
        form_action = ActionForm()

    return render(request, 'jeu/detail_personnage.html', {
        'personnage': personnage,
        'lieu': personnage.lieu,
        'form_deplacement': form_deplacement,
        'form_action': form_action,
        'personnages_dans_lieu': personnages_dans_lieu,
        'cycle': cycle,
    })

