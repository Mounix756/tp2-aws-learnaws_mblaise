import json
import os
import urllib.parse
import logging
from datetime import datetime

import boto3

# Configuration des logs CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)

ALLOWED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)


def lambda_handler(event, context):

    logger.info("===== DEBUT EXECUTION LAMBDA =====")
    logger.info(f"Event reçu : {json.dumps(event)}")

    try:

        for record in event.get("Records", []):

            bucket_name = record["s3"]["bucket"]["name"]

            file_name = urllib.parse.unquote_plus(
                record["s3"]["object"]["key"]
            )

            logger.info(
                f"Fichier reçu : {file_name} depuis le bucket : {bucket_name}"
            )

            # Vérification du type de fichier
            if not file_name.lower().endswith(ALLOWED_EXTENSIONS):

                logger.warning(
                    f"REJET - Le fichier '{file_name}' n'est pas une image autorisée"
                )

                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        "Seules les images sont autorisées"
                    )
                }

            logger.info(
                f"Validation image réussie pour : {file_name}"
            )

            # Recherche dans DynamoDB
            logger.info(
                f"Recherche du fichier '{file_name}' dans DynamoDB"
            )

            response = table.get_item(
                Key={
                    "file_name": file_name
                }
            )

            # Vérification doublon
            if "Item" in response:

                logger.warning(
                    f"DOUBLON DETECTE - Le fichier '{file_name}' existe déjà"
                )

                return {
                    "statusCode": 409,
                    "body": json.dumps(
                        f"{file_name} existe déjà dans la base"
                    )
                }

            logger.info(
                f"Aucun doublon trouvé pour '{file_name}'"
            )

            # Insertion DynamoDB
            item = {
                "file_name": file_name,
                "bucket": bucket_name,
                "created_at": datetime.utcnow().isoformat()
            }

            table.put_item(Item=item)

            logger.info(
                f"INSERTION REUSSIE - {file_name} ajouté dans DynamoDB"
            )

        logger.info("===== FIN EXECUTION LAMBDA : SUCCES =====")

        return {
            "statusCode": 200,
            "body": json.dumps(
                "Traitement terminé avec succès"
            )
        }

    except Exception as e:

        logger.error(
            f"ERREUR LAMBDA : {str(e)}",
            exc_info=True
        )

        return {
            "statusCode": 500,
            "body": json.dumps(
                f"Erreur interne : {str(e)}"
            )
        }