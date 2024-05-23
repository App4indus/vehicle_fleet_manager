# Module Open-prod : Gestion de Flotte Automobile

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0) [![Free](https://img.shields.io/badge/Free-Yes-green.svg)](https://github.com/votre-utilisateur/module-gestion-flotte) ![Open-prod: v9](https://img.shields.io/badge/Open--prod-v9-orange)
![Langues supportées: FR, EN](https://img.shields.io/badge/langage-FR%20%7C%20EN-yellow)

<img src="https://app4indus.com/wp-content/uploads/2024/01/icon.png" alt="Gestion de Flotte" width="200" />


## Vue d'ensemble

Bienvenue sur le repo **Module de Gestion de Flotte Automobile**. Ce module est conçu pour optimiser et simplifier la gestion de votre flotte de véhicules. Que vous gériez une petite flotte de voitures ou une grande flotte de camions, ce module vous fournit les outils nécessaires pour assurer des opérations de flotte efficaces.


## Fonctionnalités

- **Suivi des Véhicules** : Gérez vos véhicules et tout ce qui en découle :iInterventions, documents, contrats, contraventions, coûts,...
- **Planification de la Maintenance** : Planifiez et suivez les activités de maintenance pour garder vos véhicules en bon état.
- **Localisation** : Avec la vue carte, géolocalisez vos véhicules (nécessite le développement d'un connecteur selon plateforme de géolocalisation)
- **Gestion des Conducteurs** : Gérez les affectations des conducteurs, leurs dossiers et les demandes d'utilsiations.
- **Analyses** : Analysez les statistiques : coûts, sinistres, contraventions,...

## Dépendances

Ce module dépend du module **Administrative Contract**, qui est inclus dans le package. Le module Administrative Contract fournit la base pour gérer les contrats liés à votre flotte.

## Installation

1. **Téléchargez le Module** : Clonez le dépôt ou téléchargez le fichier ZIP.
    ```bash
    git clone https://github.com/App4indus/vehicle_fleet_manager.git
    ```

2. **Ajoutez à Open-prod** : Copiez le module dans votre répertoire d'addons custom d'Open-prod.
    ```bash
    cp -r vehicle_fleet_manager /chemin/vers/openprod/custom-addons/
    ```

3. **Configuration ficher openpord-server.conf** : Ajoutez le dossier custom-addons au ficher openprod-server.conf
   Vérifiez que le path vers 'custom-addons' est dans le fichier openprod-server.conf, champ "addons_path ="

4. **Mettez à jour la Liste des Applications** : Dans Open-prod, mettez à jour la liste des applications pour inclure le nouveau module : Configuration > Applications > Mettre à jour la liste des applications


5. **Installer le Module** : Dans Open-prod, installez le module : Configuration > Applications > Toutes les applications > recheercher 'vehicle_fleet_manager' > Insaller

## Utilisation

Une fois installé, affectez les droits requis dans la configuration d'Open-prod. Puis, rendez-vous dans le menu 'Flotte automobile'.
Consultez la notice d'utilisation : 

[Notice d'utilisation](docs/user_manual_fr.md)


## Screens 

![Fiche véhicule](https://app4indus.com/wp-content/uploads/2024/01/form-view-vehicle.png)

![Suivi contrat](https://app4indus.com/wp-content/uploads/2024/03/contrats-2048x988.png)

![Planning utilisations](https://app4indus.com/wp-content/uploads/2024/01/planning-view-uses.png)

![Gestion sinistre](https://app4indus.com/wp-content/uploads/2024/01/form-view-accident.png)


## Contribution

Les pull requests sont les bienvenues - Si vous souhaitez contribuer au développement de ce module, suivez ces étapes :

1. Forkez le dépôt.
2. Créez une nouvelle branche (`git checkout -b feature/votre-fonctionnalité`).
3. Commitez vos modifications (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez sur la branche (`git push origin feature/votre-fonctionnalité`).
5. Ouvrez une pull request.

## Licence

Ce projet est licencié sous la licence LGPL-3.0 - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Tarif

Ce projet open-source est gratuit et libre d'utilisation.

## Absence de Garantie

Ce logiciel est distribué en l'état, sans aucune garantie. En aucun cas, les auteurs ou les titulaires du droit d'auteur ne peuvent être tenus responsables de toute réclamation, de tout dommage ou de toute autre responsabilité, qu'il s'agisse d'une action contractuelle, délictuelle ou autre, découlant de, hors de ou en relation avec le logiciel ou l'utilisation ou d'autres actions dans le logiciel.

## Contact

Pour toute questions, suggestions, customisation ou support, veuillez contacter [info@app4indus.com](mailto:info@app4indus.com).

---
