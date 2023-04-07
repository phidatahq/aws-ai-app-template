from os import getenv

from phidata.app.fastapi import FastApiServer
from phidata.app.streamlit import StreamlitApp
from phidata.aws.config import AwsConfig
from phidata.aws.resource.ecs.cluster import EcsCluster
from phidata.aws.resource.s3.bucket import S3Bucket

from workspace.prd.docker_config import prd_app_image
from workspace.settings import ws_settings

#
# -*- Production AWS Resources
#

# -*- Settings
launch_type = "FARGATE"
api_key = f"{ws_settings.prd_key}-api"
app_key = f"{ws_settings.prd_key}-app"
# Do not create the resource when running `phi ws up`
skip_create: bool = False
# Do not delete the resource when running `phi ws down`
# Set True in production to skip deletion when running `phi ws down`
skip_delete: bool = False
# Wait for the resource to be created
wait_for_creation: bool = False
# Wait for the resource to be deleted
wait_for_deletion: bool = False

# -*- Define S3 bucket for prd data
prd_data_s3_bucket = S3Bucket(
    name=f"{ws_settings.prd_key}-data",
    acl="private",
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_creation,
    wait_for_deletion=wait_for_deletion,
)

# -*- Define ECS cluster for running services
prd_ecs_cluster = EcsCluster(
    name=f"{ws_settings.prd_key}-cluster",
    ecs_cluster_name=ws_settings.prd_key,
    capacity_providers=[launch_type],
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_creation,
    wait_for_deletion=wait_for_deletion,
)

# -*- StreamlitApp running on ECS
prd_streamlit = StreamlitApp(
    name=app_key,
    enabled=ws_settings.prd_app_enabled,
    image=prd_app_image,
    command=["app", "start", "Home"],
    ecs_cluster=prd_ecs_cluster,
    aws_subnets=ws_settings.subnet_ids,
    # aws_security_groups=ws_settings.security_groups,
    # Get the OpenAI API key from the environment if available
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", "")},
    use_cache=ws_settings.use_cache,
    # Read secrets from a file
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/app_secrets.yml"),
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_creation,
    wait_for_deletion=wait_for_deletion,
)

# -*- FastApiServer running on ECS
prd_fastapi = FastApiServer(
    name=api_key,
    enabled=ws_settings.prd_api_enabled,
    image=prd_app_image,
    command=["api", "start"],
    ecs_cluster=prd_ecs_cluster,
    aws_subnets=ws_settings.subnet_ids,
    # aws_security_groups=ws_settings.security_groups,
    # Get the OpenAI API key from the environment if available
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", "")},
    use_cache=ws_settings.use_cache,
    # Read secrets from a file
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/api_secrets.yml"),
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_creation,
    wait_for_deletion=wait_for_deletion,
)

#
# -*- Define AWS resources using the AwsConfig
#
prd_aws_config = AwsConfig(
    env=ws_settings.prd_env,
    apps=[prd_streamlit, prd_fastapi],
)
