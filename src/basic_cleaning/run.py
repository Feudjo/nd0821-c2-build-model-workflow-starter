#!/usr/bin/env python
"""
Downloads the raw dataset from wandb and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info('Reading dataframe')
    df = pd.read_csv(artifact_local_path)

    logger.info('Starting data cleaning')
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])

    outfile =f"{args.output_artifact}"
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    df.to_csv("clean_sample.csv", index=False)

    logger.info("Upload clean data")
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
 )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="eda output",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="cleaned dataset",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="basic_cleaning",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Download raw dataset and apply basic data cleaning steps.",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="minimum price to consider.",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="maximum price to consider.",
        required=True
    )


    args = parser.parse_args()

    go(args)
