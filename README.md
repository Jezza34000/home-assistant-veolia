![veolialogo][veolialogoimg]

[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]

[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]

> ### UNIQUEMENT compatible avec le nouveau site de Veolia : https://www.eau.veolia.fr/
> #### (N'est pas compatible avec la version IDF de Veolia https://espace-client.vedif.eau.veolia.fr)

## Informations disponibles

**Cette intégration configurera les plateformes suivantes.**

| Plateforme      | Description                                         |
|-----------------|-----------------------------------------------------|
| `sensor`        | Affiche les informations de l'API Veolia            |
| `switch`        | Switch d'activation/désactivation des alertes conso |
| `text`          | Saisie des valeurs de réglages des alertes          |
| `binary_sensor` | Affiche l'états des alertes conso                   |

### Données disponibles

- Consommation d'eau (journalière, mensuelle)
- Index de consommation d'eau
- Seuils d'alertes de consommation d'eau
- Etat des alertes de consommation d'eau

![sensors][sensorsimg]

### Configuration des alertes

L'intégration Veolia permet de configurer des alertes de consommation d'eau pour surveiller votre utilisation 
quotidienne et mensuelle, et même pour détecter une fuite si vous n'êtes pas chez vous.

Les alertes sont activées ou désactivées, en renseignant les champs seuils d'alertes (0 = désactivé, >0 = activé)


Il existe 3 types d'alertes :
- Alerte journalière
  - L'alerte journalière est une alerte qui se déclenche si votre consommation d'eau quotidienne dépasse un certain seuil **cette valeur est en litre, le minimum est de 100 litres.**
- Alerte mensuelle
  - L'alerte mensuelle est une alerte qui se déclenche si votre consommation d'eau mensuelle dépasse un certain seuil **cette valeur est en metre cubes, le minimum est de 1m3**.
- Alerte logement "vide"
  - L'alerte logement vide est une alerte qui se déclenche si une consommation d'eau est détectée alors que vous n'êtes pas chez vous.

Informations supplémentaires :
> Les notifications d'alerte sont envoyées par Veolia directement par email et par SMS (aux coordonnées de contact renseigné dans votre compte Veolia).

> Il n'est pas possible de désactiver les notifications d'alerte par email, mais vous pouvez configurer les notifications par SMS, uniquement si l'alerte est activée.

## Installation

### Via [HACS](https://hacs.xyz/) (recommandé)

**Cliquez ici:**

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Jezza34000&repository=home-assistant-veolia&category=integration)

**ou suivez ces étapes:**

1. Ouvrez HACS (Home Assistant Community Store)
2. Cliquez sur `Intégrations`
3. Cliquez sur les trois points en haut à droite
4. Cliquez sur `Intégrations personnalisées`
5. Recherchez `Veolia`
6. Cliquez sur `Installer`
7. Redémarrez Home Assistant
8. Suivez les instructions de configuration

### Manuellement

1. Copiez le dossier `custom_components/veolia` dans le dossier `custom_components` de votre configuration Home Assistant.
2. Redémarrez Home Assistant

## API Veolia

Cette intégration utilise mon client API Veolia disponible ici : [veolia-api](https://github.com/Jezza34000/veolia-api).

## Les contributions sont les bienvenues !

## Troubleshooting

Activer la journalisation du débogage

Pour activer la journalisation du débogage, accédez à `Paramètres` -> `Appareils et services`, ouvrez l'intégration "Veolia" et cliquez sur `Activer l'enregistrement des journaux`.
Reproduiez le problème, puis envoyez-moi les journaux.

## Credits

Le modèle de code de cette intégration à principalement été tiré du blueprint de @Ludeeus. Merci à lui pour son travail.

---

<!---->

[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hacs]: https://hacs.xyz
[releases-shield]: https://img.shields.io/github/v/release/Jezza34000/home-assistant-veolia.svg?style=for-the-badge
[releases]: https://github.com/Jezza34000/home-assistant-veolia/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/ludeeus/integration_blueprint.svg?style=for-the-badge
[commits]: https://github.com/Jezza34000/home-assistant-veolia/commits/main
[license-shield]: https://img.shields.io/github/license/ludeeus/integration_blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%20%40Jezza34000-blue.svg?style=for-the-badge
[veolialogoimg]: images/veolialogo.png
[sensorsimg]: images/entities.png
