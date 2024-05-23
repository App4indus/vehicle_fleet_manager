<img src="img/logo.png" width="100">  

# Documentation utilisateur module Gestionnaire de flotte automobile

## **Version du document**

| **Version** | **Auteur** | **Date** | **Motif** |
| --- | --- | --- | --- |
| **1** | Jérôme Botreau | 20/05/2024 | Création |

## **Généralités**

Ce module permet de suivre une flotte automobile : véhicules, contrats associés, PV, sinistres, coûts,...

## **Prérequis**

Se rendre sur la page du module via le menu principal > Flotte automobile

## **Configuration initiale**

### **Droits**

Rendez-vous dans la configuration d'Open-prod > Utilisateurs et sécurité > Utilisateurs. Affectez les droits selon les utilisateurs souhaités.
Niveaux de droits standards :

![Droits](img/droits.png)

- Utilisateur : Permet l'utilisation générale, la consultation des éléments.
- Fonctionnel : En plus du profil utilisateur, la modification des éléments.
- Responsable : En plus du profil utilisateur, permet la création des fiches : véhicules, contrats, interventions,...
- Administrateur : En plus du profil responsable, permet d'accéder à la configuration du modules : modèles, fabricants,...

Il existe également un droit spécifique pour les demandes de réservations de véhicules : Droits supplémentaires > Peut réserver un véhicule

![Droits](img/droits-resa.png)

### **Fabricants**

Les fabricants automobiles sont imoortés à l'installation du module, mais peuvent être modifiés / ajoutés via le menu Configuration > Fabricants automobiles (Niveau droit admin du module requis)

![Config fabricants](img/config-fabricants.png)

### **Modèles**

Dans le cas où vous utilisez plusieurs véhicules du même modèle, il est interessant de créer un modèle. De cette manière, lorsque vous devrez créer un nouveau véhicule, la sélection propagera la plupart des champs, renseignés dans le modèle.
Pour se rendre sur les modèles :  Flotte automobile > Configuration > Modèles

![Config fabricants](img/config-models.png)

Renseigner les informations liées au modèle de véhicule.


### Véhicules

Accéder via le menu Flotte automobile > Véhicules : 

![Véhicules](img/vehicules.png)

#### Création

Pour ajouter un véhicule, cliquer sur le bouton "Créer".

Commencer par renseigner :

- Le fabricant (obligatoire)
- Le modèle (facultatif) : recommandé : permet de propager les information pré-définies du modèle dans le véhicule
- Le reste des informations : immatriculation, date, statut,...
- Eventuellement les documents liés

![Créaton véhicule](img/creation-vehicule.png)


#### Vues

4 types de vues existent :

- Arbre (liste)
- Formulaire
- Kanban (cartes)
- Map (carte) (Nécessite une API d'interconnexion)

![Vues véhicule](img/vues-vehicules.png)


### Contrats

Pour ajouter un contrat ou tout autre document

### Interventions

### Infractions

Pour ajouter un contrat ou tout autre document

### Statistiques

### Autres
