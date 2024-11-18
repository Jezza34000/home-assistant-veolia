![veolialogo][veolialogoimg]

[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]


[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]


> ## Compatible avec le nouveau site de Veolia : https://www.eau.veolia.fr/


## Informations disponibles
**Cette intégration configurera les plateformes suivantes.**

| Plateforme | Description                               |
| ---------- |-------------------------------------------|
| `sensor`   | Affiche les informations de l'API Veolia  |

- Consommation d'eau (journalière, mensuelle)
- Index de consommation d'eau


![sensors][sensorsimg]

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

Le modèle de code a principalement été tiré du modèle de blueprint de @Ludeeus.

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
[sensorsimg]: images/sensors.png