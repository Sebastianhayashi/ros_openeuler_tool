import click
from ros_openeuler_tool.clone_repos import clone_repositories
from ros_openeuler_tool.process_packages import process_ros_packages
from ros_openeuler_tool.batch_process import batch_process_packages
from ros_openeuler_tool.sync_gitee import sync_to_gitee
from ros_openeuler_tool.make_public import make_repos_public
from ros_openeuler_tool.map_yum_rosdep import map_yum_to_rosdep_yaml
from ros_openeuler_tool.update_yum_mapping import update_yum_and_mapping
from ros_openeuler_tool.analyze_dependencies import analyze_dependencies
from ros_openeuler_tool.list_missing import list_missing_packages

@click.group()
def cli():
    """ROS OpenEuler 移植与管理工具"""
    pass

@cli.command()
def clone_repos():
    """克隆所有 ROS Jazzy 仓库"""
    clone_repositories()

@cli.command()
def process_packages():
    """生成 RPM 规范文件并打包源码"""
    process_ros_packages()

@cli.command()
def batch_process():
    """批量处理 ROS 包，记录缺失依赖和跳过的包"""
    batch_process_packages()

@cli.command()
def sync_gitee():
    """将源码同步到 Gitee 仓库"""
    sync_to_gitee()

@cli.command()
def make_public():
    """将 Gitee 仓库设为公开"""
    make_repos_public()

@cli.command()
def map_yum_to_rosdep():
    """将 YUM 仓库映射到 rosdep 的 YAML 文件中"""
    map_yum_to_rosdep_yaml()

@cli.command()
def update_yum_and_mapping():
    """自动更新 YUM 并同步 rosdep 映射文件"""
    update_yum_and_mapping()

@cli.command()
def analyze_dependencies():
    """分析依赖关系并生成构建顺序"""
    analyze_dependencies()

@cli.command()
def list_missing():
    """列出缺失的包和依赖"""
    list_missing_packages()

if __name__ == '__main__':
    cli()
