from phidata.aws.config import AwsConfig
from phidata.aws.resource.group import (
    AwsResourceGroup,
    EcsCluster,
    EcsContainer,
    EcsService,
    EcsTaskDefinition,
    S3Bucket,
)

from workspace.prd.docker_config import prd_app_image
from workspace.settings import ws_settings

#
# -*- Production AWS Resources for running the AI App
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
wait_for_create: bool = True
# Wait for the resource to be deleted
wait_for_delete: bool = True

# -*- Define S3 bucket for dev data
prd_data_s3_bucket = S3Bucket(
    name=f"{ws_settings.prd_key}-data",
    acl="private",
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- Create ECS cluster for running containers
prd_ecs_cluster = EcsCluster(
    name=f"{ws_settings.prd_key}-cluster",
    ecs_cluster_name=ws_settings.prd_key,
    capacity_providers=[launch_type],
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- AI App Container running Streamlit on ECS
app_container_port = 9095
prd_app_container = EcsContainer(
    name=app_key,
    image=prd_app_image.get_image_str(),
    port_mappings=[{"containerPort": app_container_port}],
    command=["app start Home"],
    environment=[
        {"name": "RUNTIME", "value": "prd"},
    ],
    log_configuration={
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": ws_settings.prd_key,
            "awslogs-region": ws_settings.aws_region,
            "awslogs-create-group": "true",
            "awslogs-stream-prefix": "app",
        },
    },
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- AI App Task Definition
prd_app_task_definition = EcsTaskDefinition(
    name=f"{app_key}-td",
    family=app_key,
    network_mode="awsvpc",
    cpu="512",
    memory="1024",
    containers=[prd_app_container],
    requires_compatibilities=[launch_type],
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- AI App Service
prd_app_service = EcsService(
    name=f"{app_key}-service",
    desired_count=1,
    launch_type=launch_type,
    cluster=prd_ecs_cluster,
    task_definition=prd_app_task_definition,
    network_configuration={
        "awsvpcConfiguration": {
            "subnets": ws_settings.subnet_ids,
            # "securityGroups": ws_settings.security_groups,
            "assignPublicIp": "ENABLED",
        }
    },
    # Force delete the service.
    force_delete=True,
    # Force a new deployment of the service on update.
    force_new_deployment=True,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- AI App AwsResourceGroup
app_aws_rg = AwsResourceGroup(
    name=app_key,
    enabled=ws_settings.prd_app_enabled,
    ecs_clusters=[prd_ecs_cluster],
    ecs_task_definitions=[prd_app_task_definition],
    ecs_services=[prd_app_service],
)

# -*- Api Container running FastAPI on ECS
api_container_port = 9090
prd_api_container = EcsContainer(
    name=api_key,
    image=prd_app_image.get_image_str(),
    port_mappings=[{"containerPort": api_container_port}],
    command=["api start"],
    environment=[
        {"name": "RUNTIME", "value": "prd"},
    ],
    log_configuration={
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": ws_settings.prd_key,
            "awslogs-region": ws_settings.aws_region,
            "awslogs-create-group": "true",
            "awslogs-stream-prefix": "api",
        },
    },
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- Api Task Definition
prd_api_task_definition = EcsTaskDefinition(
    name=f"{api_key}-td",
    family=api_key,
    network_mode="awsvpc",
    cpu="512",
    memory="1024",
    containers=[prd_api_container],
    requires_compatibilities=[launch_type],
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- Api Service
prd_api_service = EcsService(
    name=f"{api_key}-service",
    desired_count=1,
    launch_type=launch_type,
    cluster=prd_ecs_cluster,
    task_definition=prd_api_task_definition,
    network_configuration={
        "awsvpcConfiguration": {
            "subnets": ws_settings.subnet_ids,
            # "securityGroups": ws_settings.security_groups,
            "assignPublicIp": "ENABLED",
        }
    },
    # Force delete the service.
    force_delete=True,
    # Force a new deployment of the service on update.
    force_new_deployment=True,
    skip_create=skip_create,
    skip_delete=skip_delete,
    wait_for_creation=wait_for_create,
    wait_for_deletion=wait_for_delete,
)

# -*- Api AwsResourceGroup
api_aws_rg = AwsResourceGroup(
    name=api_key,
    enabled=ws_settings.prd_api_enabled,
    ecs_clusters=[prd_ecs_cluster],
    ecs_task_definitions=[prd_api_task_definition],
    ecs_services=[prd_api_service],
)

#
# -*- Define production AWS resources using the AwsConfig
#
prd_aws_config = AwsConfig(
    env=ws_settings.prd_env,
    resources=[app_aws_rg, api_aws_rg],
)
