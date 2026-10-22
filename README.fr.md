<div align="center">

<picture>
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/hero-light.svg">
  <img src="docs/assets/hero.svg" width="100%" alt="MeshLive en app Mac : l'onglet Live avec les directs à proximité, les appels récents avec un appel manqué en rouge, un appel entrant avec Refuser, Voix et Accepter, un appel vocal en cours et la feuille Go live">
</picture>

**MeshLive pour iPhone et Mac.** Appels chiffrés et vidéo en direct entre appareils Apple et téléphones Android proches, par Bluetooth, sans internet, sans compte, sans serveur.

<a href="#compiler"><img src="docs/assets/btn-build-fr.svg" alt="Compiler" height="48"></a>&nbsp;
<a href="#ce-que-ce-fork-ajoute"><img src="docs/assets/btn-adds-fr.svg" alt="Ce qu'il ajoute" height="48"></a>&nbsp;
<a href="#état"><img src="docs/assets/btn-status-fr.svg" alt="État" height="48"></a>&nbsp;
<a href="https://github.com/MeshLive/meshlive-ios"><img src="docs/assets/btn-upstream-fr.svg" alt="Projet d'origine" height="48"></a>

<br>

![iOS 16+](https://img.shields.io/badge/iOS-16%2B-ffffff?style=flat-square&labelColor=0d1117&logo=apple&logoColor=ffffff)
![Mac : Apple silicon](https://img.shields.io/badge/Mac-Apple%20silicon%20(Catalyst)-ffffff?style=flat-square&labelColor=0d1117&logo=apple&logoColor=ffffff)
![Internet : aucun](https://img.shields.io/badge/internet-aucun-ffffff?style=flat-square&labelColor=0d1117)
![Licence GPL-3.0-or-later](https://img.shields.io/badge/licence-GPL--3.0--or--later-ffffff?style=flat-square&labelColor=0d1117)
![État : débutant](https://img.shields.io/badge/%C3%A9tat-d%C3%A9butant-E5484D?style=flat-square&labelColor=0d1117)

Pas de version compilée : vous la compilez sur votre Mac et la signez avec votre propre équipe Apple · logiciel libre, GPL

[English](README.md) · Français

</div>

---

[MeshLive](https://github.com/MeshLive) envoie la vidéo de la caméra et le son du micro directement entre téléphones proches, en Bluetooth LE, chiffrés, sans rien entre les deux. Ce dépôt est un fork de [MeshLive pour iPhone](https://github.com/MeshLive/meshlive-ios) qui ajoute **une vraie app Mac** construite à partir du même code, et quelques changements sur iPhone. Le protocole ne change pas : il parle toujours aux apps [iPhone](https://github.com/MeshLive/meshlive-ios) et [Android](https://github.com/MeshLive/meshlive-android).

> **Logiciel débutant, non audité.** Les appels et les directs entre un Mac et un iPhone ont été essayés à la main. Rien ici n'a été essayé face à un téléphone Android, et le protocole n'a eu aucune revue de sécurité indépendante. Ne vous y fiez pas si votre sécurité en dépend. Lisez d'abord [Ce que les appareils proches voient](#ce-que-les-appareils-proches-voient).

## Ce qu'il fait

<table>
  <tr>
    <td><img src="docs/assets/card-mac.svg" alt="L'onglet Live de l'app Mac, avec la barre latérale : Live, Calls, Contacts, Settings" width="100%"></td>
    <td><img src="docs/assets/card-calls.svg" alt="Un appel entrant avec Refuser, Voix et un Accepter vert, puis l'appel en cours" width="100%"></td>
    <td><img src="docs/assets/card-missed.svg" alt="Les appels récents, l'appel manqué en rouge" width="100%"></td>
  </tr>
  <tr>
    <td><img src="docs/assets/card-golive.svg" alt="La feuille Go live : vidéo et son, ou son seul avec Voice, Low data et Music" width="100%"></td>
    <td><img src="docs/assets/card-background.svg" alt="Réglages, Experiments : l'interrupteur Reachable in the background qui s'allume" width="100%"></td>
    <td><img src="docs/assets/card-people.svg" alt="Les contacts avec boutons appel vidéo, appel vocal et infos" width="100%"></td>
  </tr>
</table>

## Ce que ce fork ajoute

**Une app Mac (Mac Catalyst, Apple silicon)**

- Toute l'app sur le Mac : appels, directs, visionnage, contacts, vérification d'identité, réglages.
- Une mise en page Mac : barre latérale au lieu de la barre d'onglets, pas de barre de titre, colonnes à la largeur d'un téléphone dans une grande fenêtre, plein écran sans barre sur l'appel.
- Utilise la caméra intégrée du Mac (ignore les caméras virtuelles), envoie une vidéo paysage 426×240.
- Reste joignable fenêtre masquée ou réduite : macOS ne suspend pas les apps, donc un appel entrant sonne quand même.
- S'appelle `MeshLive.app` dans le Finder, la barre de menus et les demandes d'autorisation, avec une icône pleine taille sur macOS 26 et suivants.
- Deux plantages corrigés, trouvés sur le Mac : l'écran d'appel et la feuille Go live perdaient le modèle de l'app.

**Sur l'iPhone**

- L'interface passe en paysage. La caméra suit le téléphone, et le flux envoyé garde la même taille portrait (recadrage centré, aucun changement de protocole).
- Appels manqués : une pastille sur Calls, Recent s'ouvre tout seul, lignes manquées en rouge comme dans l'app Téléphone.
- Renommer un contact vérifié (un nom local seulement).
- Un bouton Accepter vert, et un pictogramme de personne au lieu d'un chiffre pour les correspondants sans nom.
- **Expérimental, désactivé par défaut :** « Reachable in the background » (Settings › Experiments). Un iPhone en arrière-plan garde une balise Bluetooth fixe, et les iPhone et Mac proches lisent son annonce en GATT : ils peuvent encore l'appeler, et l'appel sonne en notification. Android ne voit pas un iPhone en arrière-plan, et une app fermée ne peut pas sonner. Pas encore essayé sur appareil.

## État

| | Mac ↔ iPhone | Apple ↔ Android |
| --- | --- | --- |
| Appels voix et vidéo | essayés à la main, un Mac, un iPhone | pas essayés ici (voir [l'état du projet d'origine](https://github.com/MeshLive/meshlive-ios#status)) |
| Go live et visionnage | essayés à la main | pas essayés ici |
| Joignable en arrière-plan | construit, tests unitaires verts, pas essayé sur appareil | impossible : iOS cache à Android un iPhone en arrière-plan |

- Les 175 tests du cœur, des médias et du protocole passent (`bash Scripts/test.sh`).
- L'app Mac demande Apple silicon : les codecs n'ont pas de tranche Catalyst Intel.
- Tout ce que l'app d'origine liste comme non testé l'est encore ici.

## Compiler

Il faut un Mac avec Xcode 26 ou plus récent, Python 3, et internet pour la première compilation (les scripts récupèrent les sources épinglées de libopus et libvpx). Aucun binaire tiers dans le dépôt.

```sh
bash Scripts/prepare-opus.sh      # libopus 1.6.1 -> Vendor/Opus.xcframework (tranches iPhone, simulateur, Mac)
bash Scripts/prepare-libvpx.sh    # libvpx 1.15.2 -> Vendor/VPX.xcframework
python3 Scripts/project.py        # régénère NearbyIntercom.xcodeproj (aucune donnée de signature)
bash Scripts/test.sh              # tests du cœur, des médias et du protocole
```

**App Mac.** Signée ad hoc, pour votre propre Mac. Elle arrive dans `.build/catalyst/Build/Products/Debug-maccatalyst/MeshLive.app`.

```sh
xcodebuild -project NearbyIntercom.xcodeproj -scheme NearbyIntercom \
  -destination 'platform=macOS,variant=Mac Catalyst,arch=arm64' -configuration Debug \
  -derivedDataPath .build/catalyst CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM= build
```

**iPhone.** Signée avec votre équipe, sur un téléphone en iOS 16 ou plus récent. Gardez-le déverrouillé :

```sh
TEAM=<votre team id> BUNDLE=<un bundle id unique> bash Scripts/run-device.sh
```

Autorisez Bluetooth, Caméra et Micro quand c'est demandé. Pour régénérer les images de ce README, lancez `python3 docs/assets/make_svgs.py`. Les captures de `docs/assets/readme-src/` viennent de l'app Mac lancée avec `-NearbyFixture populated`, qui n'affiche que des personnes inventées.

## Ce que les appareils proches voient

N'importe qui avec un scanner Bluetooth à portée peut voir qu'un appareil MeshLive est là. Les appels et les directs sont chiffrés, leur présence ne l'est pas.

- **Un préfixe d'identifiant stable.** Tant que l'app est ouverte et propose un appel ou un direct, elle diffuse un préfixe de 48 bits de son identifiant de nœud, qui ne change pas. Un scanner peut s'en servir pour relier les adresses Bluetooth changeantes de l'appareil sur plusieurs jours. Les identifiants tournants existent mais restent expérimentaux.
- **Qui vous êtes, à la connexion.** La poignée de main qui ouvre chaque connexion transporte la clé publique en clair : une tentative de connexion révèle l'identité.
- **La balise d'arrière-plan** (seulement si vous activez l'expérience) : la balise fixe dit « un iPhone MeshLive est là » aux appareils Apple, et tout appareil qui se connecte peut lire l'annonce que le téléphone affiche au premier plan.

Pour réduire l'exposition : fermez l'app ou coupez le Bluetooth quand vous n'en avez pas besoin, laissez les noms et titres désactivés, et donnez à votre téléphone un nom neutre. Le [README d'origine](https://github.com/MeshLive/meshlive-ios#what-nearby-phones-can-see) donne tous les détails.

## Projet d'origine

[MeshLive/meshlive-ios](https://github.com/MeshLive/meshlive-ios) porte l'app iPhone, et [meshlive-android](https://github.com/MeshLive/meshlive-android) porte le protocole. Les corrections de ce fork repartent vers l'origine en pull requests : [la CI et la vérification du décodeur AV1](https://github.com/MeshLive/meshlive-ios/pull/2) est la première. Chaque commit est signé (`git commit -s`), comme le demande [CONTRIBUTING.md](CONTRIBUTING.md). Les problèmes de sécurité passent par [SECURITY.md](SECURITY.md), jamais par une issue publique.

## Licence

GPL-3.0-or-later, comme l'origine : vous pouvez l'utiliser, la modifier et la partager, et les versions modifiées que vous distribuez restent sous la même licence. Copyright (C) 2026 The MeshLive Authors (voir [AUTHORS](AUTHORS)), texte complet dans [LICENSE](LICENSE). libopus et libvpx gardent leur licence BSD-3-Clause ; voir [Vendor/README.md](Vendor/README.md).

<sub>Un fork indépendant, pas une version officielle de MeshLive. Apple, iPhone, Mac et macOS sont des marques d'Apple Inc.</sub>
