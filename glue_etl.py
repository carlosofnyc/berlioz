import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1710183885875 = glueContext.create_dynamic_frame.from_catalog(
    database="classical-music-db",
    table_name="spotify_classical_music",
    transformation_ctx="AWSGlueDataCatalog_node1710183885875",
)

# Script generated for node Change Schema
ChangeSchema_node1710183944958 = ApplyMapping.apply(
    frame=AWSGlueDataCatalog_node1710183885875,
    mappings=[
        ("albums.href", "string", "albums.href", "string"),
        ("albums.items", "array", "albums.items", "array"),
        ("albums.limit", "int", "albums.limit", "int"),
        ("albums.next", "string", "albums.next", "string"),
        ("albums.offset", "int", "albums.offset", "int"),
        ("albums.previous", "string", "albums.previous", "null"),
        ("albums.total", "int", "albums.total", "int"),
        ("tracks.href", "string", "tracks.href", "string"),
        ("tracks.items", "array", "tracks.items", "array"),
        ("tracks.limit", "int", "tracks.limit", "int"),
        ("tracks.next", "string", "tracks.next", "string"),
        ("tracks.offset", "int", "tracks.offset", "int"),
        ("tracks.previous", "string", "tracks.previous", "null"),
        ("tracks.total", "int", "tracks.total", "int"),
        ("playlists.href", "string", "playlists.href", "string"),
        ("playlists.items", "array", "playlists.items", "array"),
        ("playlists.limit", "int", "playlists.limit", "int"),
        ("playlists.next", "string", "playlists.next", "string"),
        ("playlists.offset", "int", "playlists.offset", "int"),
        ("playlists.previous", "string", "playlists.previous", "null"),
        ("playlists.total", "int", "playlists.total", "int"),
    ],
    transformation_ctx="ChangeSchema_node1710183944958",
)

# Script generated for node Amazon S3
AmazonS3_node1710184069983 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node1710183944958,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://cleaned-classical-music", "partitionKeys": []},
    format_options={"compression": "gzip"},
    transformation_ctx="AmazonS3_node1710184069983",
)

job.commit()
