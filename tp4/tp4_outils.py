"""Chargement et affichage ; les calculs des exercices restent dans leurs scripts."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

DOSSIER_SCRIPTS = Path(__file__).resolve().parent
DOSSIER_RESSOURCES = DOSSIER_SCRIPTS.parent / 'tp4' / 'ressources-tp4'
if not DOSSIER_RESSOURCES.exists():
    DOSSIER_RESSOURCES = DOSSIER_SCRIPTS.parent / 'ressources'
DOSSIER_RESULTATS = DOSSIER_SCRIPTS / 'resultats'


def charger_image(nom):
    with Image.open(DOSSIER_RESSOURCES / nom) as source:
        return np.asarray(source.convert('L'), dtype=float) / 255


def verifier(valeur):
    if valeur is None:
        raise NotImplementedError('Complétez les calculs TODO avant de lancer le script.')
    return valeur


def afficher_spectre(image, module_centre, titre, nom):
    figure, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].imshow(image, cmap='gray', vmin=0, vmax=1)
    axes[0].set_title(titre)
    axes[0].axis('off')
    frequences_x = np.fft.fftshift(np.fft.fftfreq(image.shape[1]))
    frequences_y = np.fft.fftshift(np.fft.fftfreq(image.shape[0]))
    for axe in axes[1:]:
        axe.pcolormesh(frequences_x, frequences_y, np.log1p(module_centre),
                       cmap='magma', shading='nearest')
        axe.set_xlabel('Fréquence selon les colonnes (cycles/pixel)')
        axe.set_ylabel('Fréquence selon les lignes (cycles/pixel)')
        axe.set_aspect('equal')
    axes[1].set_title('Module centré, affichage logarithmique')
    axes[2].set_title('Agrandissement autour de zéro')
    axes[2].set_xlim(-0.08, 0.08)
    axes[2].set_ylim(-0.08, 0.08)
    graduations = [-1/16, -1/32, 0, 1/32, 1/16]
    etiquettes = ['-1/16', '-1/32', '0', '1/32', '1/16']
    axes[2].set_xticks(graduations, etiquettes, rotation=45)
    axes[2].set_yticks(graduations, etiquettes)
    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    figure.tight_layout(h_pad=2.5)
    figure.savefig(DOSSIER_RESULTATS / nom, dpi=160, bbox_inches='tight')
    print('Figure enregistrée :', DOSSIER_RESULTATS / nom)
    plt.show()
    plt.close(figure)


def afficher_translation(image, deplacee, spectre, spectre_deplace,
                         reconstruite, reconstruite_deplacee, titre, nom):
    figure, axes = plt.subplots(2, 3, figsize=(12, 8))
    modules = [np.log1p(np.abs(np.fft.fftshift(s)))
               for s in (spectre, spectre_deplace)]
    maximum = max(float(m.max()) for m in modules)
    fx = np.fft.fftshift(np.fft.fftfreq(image.shape[1]))
    fy = np.fft.fftshift(np.fft.fftfreq(image.shape[0]))
    for ligne, (entree, reconstruction, module, etiquette) in enumerate([
        (image, reconstruite, modules[0], 'Initiale'),
        (deplacee, reconstruite_deplacee, modules[1], 'Déplacée'),
    ]):
        for colonne, tableau, legende in [
            (0, entree, etiquette), (1, reconstruction, 'Reconstruction'),
        ]:
            axes[ligne, colonne].imshow(tableau, cmap='gray', vmin=0, vmax=1)
            axes[ligne, colonne].set_title(legende)
            axes[ligne, colonne].axis('off')
        axe = axes[ligne, 2]
        axe.pcolormesh(fx, fy, module, shading='nearest', cmap='magma',
                       vmin=0, vmax=maximum)
        axe.set_title('Module centré\nÉchelle logarithmique commune')
        axe.set_xlabel('Fréquence selon les colonnes (cycles/pixel)')
        axe.set_ylabel('Fréquence selon les lignes (cycles/pixel)')
        axe.set_aspect('equal')
    figure.suptitle(titre)
    figure.tight_layout(h_pad=2.5)
    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    figure.savefig(DOSSIER_RESULTATS / nom, dpi=160, bbox_inches='tight')
    print('Figure enregistrée :', DOSSIER_RESULTATS / nom)
    plt.show()
    plt.close(figure)


def enregistrer(figure, nom):
    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    figure.tight_layout(h_pad=2.5)
    figure.savefig(DOSSIER_RESULTATS / nom, dpi=160, bbox_inches='tight')
    print('Figure enregistrée :', DOSSIER_RESULTATS / nom)
    plt.show()
    plt.close(figure)


def afficher_passe_bas(image, resultats, titre, nom, fx, fy, ligne_profil=None):
    figure, axes = plt.subplots(2, 3, figsize=(12, 8))
    for ligne in range(2):
        axes[ligne, 0].imshow(image, cmap='gray', vmin=0, vmax=1)
        axes[ligne, 0].set_title('Originale')
        axes[ligne, 0].axis('off')
        for colonne in range(2):
            methode, frequence, masque, filtree = resultats[2*ligne+colonne]
            axe = axes[ligne, colonne+1]
            axe.imshow(filtree, cmap='gray', vmin=0, vmax=1)
            axe.set_title(f'{methode} : f0={frequence:.2f} cycle/pixel')
            axe.axis('off')
    figure.suptitle(titre + " : mêmes limites d'affichage [0, 1]")
    enregistrer(figure, '03-images-' + nom)

    figure, axes = plt.subplots(2, 2, figsize=(9, 8))
    for axe, (methode, frequence, masque, filtree) in zip(axes.flat, resultats):
        trace = axe.pcolormesh(fx, fy, masque, shading='nearest',
                               cmap='gray', vmin=0, vmax=1)
        axe.set_title(f'{methode} : f0={frequence:.2f} cycle/pixel')
        axe.set_xlabel('Fréquence selon les colonnes (cycles/pixel)')
        axe.set_ylabel('Fréquence selon les lignes (cycles/pixel)')
        axe.set_aspect('equal')
        figure.colorbar(trace, ax=axe, label='Facteur H')
    enregistrer(figure, '03-masques-' + nom)

    if ligne_profil is not None:
        figure, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
        for indice, axe in enumerate(axes):
            axe.plot(image[ligne_profil], color='black', linestyle='--',
                     label='Originale')
            for methode, frequence, masque, filtree in resultats[2*indice:2*indice+2]:
                axe.plot(filtree[ligne_profil], label=methode)
            axe.set_xlim(30, 90)
            axe.set_title(f'f0={resultats[2*indice][1]:.2f} cycle/pixel')
            axe.set_xlabel('Colonne x')
            axe.set_ylabel('Intensité calculée, sans écrêtage')
            axe.grid(alpha=0.25)
            axe.legend()
        figure.suptitle(f'{titre} : profil de la ligne {ligne_profil}, frontière gauche')
        enregistrer(figure, '03-profils-' + nom)


def afficher_rejection(cas, masque, spectre_filtre, fx, fy, rayon,
                       prefixe='04', region=(160, 100, 160, 160)):
    x, y, largeur, hauteur = region
    figure, axes = plt.subplots(2, len(cas), figsize=(15, 8))
    for colonne, (titre, tableau) in enumerate(cas):
        axes[0, colonne].imshow(tableau, cmap='gray', vmin=0, vmax=1)
        axes[0, colonne].set_title(titre)
        axes[1, colonne].imshow(tableau[y:y+hauteur, x:x+largeur], cmap='gray',
                                vmin=0, vmax=1, interpolation='nearest')
        axes[1, colonne].set_title('Même région agrandie')
        axes[0, colonne].add_patch(plt.Rectangle((x, y), largeur, hauteur,
                                                fill=False, edgecolor='orange'))
        axes[0, colonne].axis('off')
        axes[1, colonne].axis('off')
    figure.suptitle(f'Comparaison des traitements, rayon {rayon:.3f} cycle/pixel')
    enregistrer(figure, f'{prefixe}-comparaison-{rayon:.3f}.png')

    figure, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    trace = axes[0].pcolormesh(fx, fy, masque, shading='nearest',
                              cmap='gray', vmin=0, vmax=1)
    figure.colorbar(trace, ax=axes[0], label='Facteur H')
    axes[0].set_title('Masque\nNoir : rejet ; blanc : conservation')
    axes[1].pcolormesh(fx, fy, np.log1p(np.abs(spectre_filtre)),
                       shading='nearest', cmap='magma')
    axes[1].set_title('Module filtré, affichage logarithmique')
    for axe in axes:
        axe.set_xlim(-0.08, 0.08)
        axe.set_ylim(-0.08, 0.08)
        axe.set_aspect('equal')
        axe.set_xlabel('Fréquence selon les colonnes (cycles/pixel)')
        axe.set_ylabel('Fréquence selon les lignes (cycles/pixel)')
        axe.set_xticks([-1/16, -1/32, 0, 1/32, 1/16],
                      ['-1/16', '-1/32', '0', '1/32', '1/16'], rotation=45)
        axe.set_yticks([-1/16, -1/32, 0, 1/32, 1/16],
                      ['-1/16', '-1/32', '0', '1/32', '1/16'])
    enregistrer(figure, f'{prefixe}-masque-{rayon:.3f}.png')


def afficher_hybrides(facade, circuit, hybride_1, hybride_2):
    images = [facade, circuit, hybride_1, hybride_2]
    minimum = min(float(image.min()) for image in images)
    maximum = max(float(image.max()) for image in images)
    figure, axes = plt.subplots(2, 2, figsize=(10, 10))
    titres = ['Façade', 'Circuit', 'Module façade\nPhase circuit',
              'Module circuit\nPhase façade']
    for axe, image, titre in zip(axes.flat, images, titres):
        axe.imshow(image, cmap='gray', vmin=minimum, vmax=maximum)
        axe.set_title(titre)
        axe.axis('off')
    figure.suptitle(f'Échelle commune : [{minimum:.3f}, {maximum:.3f}]\n'
                    'Valeurs conservées, sans écrêtage ni normalisation séparée')
    enregistrer(figure, '06-module-phase.png')
