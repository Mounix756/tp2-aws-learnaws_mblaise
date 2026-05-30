# AWS Lambda S3 Trigger - TP2

Projet AWS permettant de déclencher automatiquement une fonction Lambda lors de l'ajout d'un fichier dans un bucket S3.

## Objectifs du TP

- Déployer une fonction AWS Lambda avec CloudFormation.
- Déclencher la fonction à partir d'un événement S3.
- Utiliser DynamoDB pour stocker les métadonnées des fichiers.
- Utiliser des variables d'environnement pour la configuration.
- Accepter uniquement les fichiers image.
- Empêcher l'ajout de fichiers en double.
- Journaliser les traitements dans CloudWatch Logs.

## Architecture

- **AWS Lambda** : traite les événements provenant de S3.
- **Amazon S3** : stockage des fichiers et déclenchement de Lambda.
- **Amazon DynamoDB** : stockage des informations des fichiers déjà traités.
- **IAM Role** : permissions CloudWatch Logs et DynamoDB.

## Structure du projet

```text
├── infrastructure/
│   └── template.yaml
├── src/
│   └── main.py
├── README.md
└── .gitignore
```

## Fonctionnement

1. Un fichier est envoyé dans le bucket S3.
2. S3 déclenche automatiquement la fonction Lambda.
3. Lambda vérifie que le fichier est une image :
   - `.jpg`
   - `.jpeg`
   - `.png`
   - `.webp`
4. Lambda vérifie dans DynamoDB si un fichier portant le même nom existe déjà.
5. Si le fichier existe :
   - rejet du fichier ;
   - écriture d'un log CloudWatch.
6. Sinon :
   - enregistrement dans DynamoDB ;
   - écriture d'un log CloudWatch.

## Variables d'environnement

| Variable | Description |
|-----------|-------------|
| TABLE_NAME | Nom de la table DynamoDB |

## Déploiement

### 1. Empaqueter le projet

```bash
aws cloudformation package \
  --template-file infrastructure/template.yaml \
  --s3-bucket iabd-sourcecode-management-bucket \
  --output-template-file infrastructure/packaged.yaml
```

### 2. Déployer la stack

```bash
aws cloudformation deploy \
  --template-file infrastructure/packaged.yaml \
  --stack-name mblaise-lambda-s3-trigger-stack \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
```

## Vérification des logs CloudWatch

Après avoir envoyé un fichier dans le bucket S3 :

1. Ouvrir la console AWS.
2. Accéder au service **CloudWatch**.
3. Aller dans **Logs > Log groups**.
4. Ouvrir le groupe de logs associé à la fonction Lambda.
5. Vérifier les messages générés.

### Exemple : image valide

```text
===== DEBUT EXECUTION LAMBDA =====
Fichier reçu : photo.jpg depuis le bucket
Validation image réussie pour : photo.jpg
Aucun doublon trouvé pour 'photo.jpg'
INSERTION REUSSIE - photo.jpg ajouté dans DynamoDB
===== FIN EXECUTION LAMBDA : SUCCES =====
```

### Exemple : fichier non image

```text
===== DEBUT EXECUTION LAMBDA =====
Fichier reçu : document.pdf depuis le bucket
REJET - Le fichier 'document.pdf' n'est pas une image autorisée
```

### Exemple : doublon

```text
===== DEBUT EXECUTION LAMBDA =====
Fichier reçu : photo.jpg depuis le bucket
DOUBLON DETECTE - Le fichier 'photo.jpg' existe déjà
```

## Tests réalisés

### Cas 1 : Image valide

Résultat :

- fichier accepté ;
- ajout dans DynamoDB ;
- log CloudWatch généré.

### Cas 2 : Fichier non image

Résultat :

- fichier rejeté ;
- log CloudWatch indiquant que le fichier n'est pas une image.

### Cas 3 : Doublon

Résultat :

- fichier rejeté ;
- log CloudWatch indiquant qu'un doublon a été détecté.

## Suppression de la stack

```bash
aws cloudformation delete-stack \
  --stack-name mblaise-lambda-s3-trigger-stack
```

## Technologies utilisées

- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch
- AWS CloudFormation
- Python 3.12

## Auteur

Projet réalisé dans le cadre du TP AWS Lambda - Master 1 IA & Big Data.