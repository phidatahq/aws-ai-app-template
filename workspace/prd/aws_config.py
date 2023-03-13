from phidata.aws.config import AwsConfig
from phidata.aws.resource.group import (
    AwsResourceGroup,
    EcsCluster,
    EcsContainer,
    EcsService,
    EcsTaskDefinition,
)

from workspace.prd.docker_config import prd_app_image
from workspace.settings import ws_settings

#
# -*- Production AWS resources
#

# -*- Create ECS cluster for running containers
launch_type = "FARGATE"
prd_ecs_cluster = EcsCluster(
    name=f"{ws_settings.prd_key}-cluster",
    ecs_cluster_name=ws_settings.prd_key,
    capacity_providers=[launch_type],
)

#
# -*- AWS Resources for App Server running Streamlit
#
# -*- App Container running Streamlit on ECS
app_container_port = 9095
prd_app_container = EcsContainer(
    name=f"{ws_settings.ws_name}-app",
    image=prd_app_image.get_image_str(),
    port_mappings=[{"containerPort": app_container_port}],
    command=["app start"],
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
)
# -*- App Task Definition
prd_app_task_definition = EcsTaskDefinition(
    name=f"{ws_settings.prd_key}-td",
    family=ws_settings.prd_key,
    network_mode="awsvpc",
    cpu="512",
    memory="1024",
    containers=[prd_app_container],
    requires_compatibilities=[launch_type],
)
# -*- App Service
prd_app_service = EcsService(
    name=f"{ws_settings.prd_key}-service",
    ecs_service_name=ws_settings.prd_key,
    desired_count=1,
    launch_type=launch_type,
    cluster=prd_ecs_cluster,
    task_definition=prd_app_task_definition,
    network_configuration={
        "awsvpcConfiguration": {
            # "subnets": ws_settings.subnet_ids,
            # "securityGroups": ws_settings.security_groups,
            "assignPublicIp": "ENABLED",
        }
    },
)
# -*- AwsResourceGroup
app_aws_rg = AwsResourceGroup(
    name=f"{ws_settings.ws_name}-app",
    enabled=ws_settings.prd_app_enabled,
    ecs_clusters=[prd_ecs_cluster],
    ecs_task_definitions=[prd_app_task_definition],
    ecs_services=[prd_app_service],
)

#
# -*- AWS Resources for Api Server running FastAPI
#
# -*- Api Container running FastAPI on ECS
api_container_port = 9090
prd_api_container = EcsContainer(
    name=f"{ws_settings.ws_name}-api",
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
)
# -*- Api Task Definition
prd_api_task_definition = EcsTaskDefinition(
    name=f"{ws_settings.prd_key}-td",
    family=ws_settings.prd_key,
    network_mode="awsvpc",
    cpu="512",
    memory="1024",
    containers=[prd_api_container],
    requires_compatibilities=[launch_type],
)
# -*- Api Service
prd_api_service = EcsService(
    name=f"{ws_settings.prd_key}-service",
    ecs_service_name=ws_settings.prd_key,
    desired_count=1,
    launch_type=launch_type,
    cluster=prd_ecs_cluster,
    task_definition=prd_api_task_definition,
    network_configuration={
        "awsvpcConfiguration": {
            # "subnets": ws_settings.subnet_ids,
            # "securityGroups": ws_settings.security_groups,
            "assignPublicIp": "ENABLED",
        }
    },
)
# -*- AwsResourceGroup
api_aws_rg = AwsResourceGroup(
    name=f"{ws_settings.ws_name}-api",
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
