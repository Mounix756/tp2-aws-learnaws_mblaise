# AWS Lambda S3 Trigger - TP2

Projet d'une fonction Lambda déclenchée par des événements S3 utilisant CloudFormation.

## Architecture

- **Fonction Lambda** : Gère les événements de création d'objets S3
- **S3 Bucket** : Déclenche la fonction Lambda lors de l'upload de fichiers
- **IAM Role** : Rôle d'exécution pour la Lambda avec permissions CloudWatch Logs

## Prérequis

- AWS CLI configuré avec des credentials valides
- Python 3.12
- S3 bucket pour stocker le code source : `iabd-sourcecode-management-bucket`

## Structure du projet

```
├── infrastructure/
│   └── template.yaml          # Template CloudFormation SAM
├── src/
│   └── main.py               # Code de la fonction Lambda
├── README.md
└── .gitignore
```

## Déploiement

### 1. Préparer et empaqueter le template

```bash
aws cloudformation package \
  --template-file infrastructure/template.yaml \
  --s3-bucket iabd-sourcecode-management-bucket \
  --output-template-file infrastructure/packaged.yaml
```

### 2. Déployer la stack CloudFormation

```bash
aws cloudformation deploy \
  --template-file infrastructure/packaged.yaml \
  --stack-name mblaise-lambda-s3-trigger-stack \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
```

## Paramètres disponibles

- `Environment` : Nom de l'environnement (défaut : `mblaise`)
- `BucketName` : Nom du bucket S3 (défaut : `iabd-sourcecode-management-bucket`)

## Fonction Lambda

La fonction est définie dans `src/main.py` et doit exporter un handler :

```python
def lambda_handler(event, context):
    # Traiter les événements S3
    pass
```

## Suppression de la stack

```bash
aws cloudformation delete-stack --stack-name mblaise-lambda-s3-trigger-stack
```

## Notes

- La version CloudFormation utilisée est `2010-09-09`
- Runtime Lambda : Python 3.12
- La fonction a accès aux logs CloudWatch via le rôle IAM
