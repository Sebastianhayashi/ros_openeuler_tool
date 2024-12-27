# ros_openeuler_tool/process_packages.py

import os
import subprocess
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SPECS_DIR = os.path.expanduser('~/rpmbuild/SPECS')
SOURCES_DIR = os.path.expanduser('~/rpmbuild/SOURCES')
BASE_DIR = os.getcwd()

def setup_directories():
    for directory in [SPECS_DIR, SOURCES_DIR]:
        if not os.path.exists(directory):
            logging.info(f"创建目录: {directory}")
            os.makedirs(directory, exist_ok=True)
        else:
            logging.info(f"目录已存在: {directory}")

def process_package(pkg_dir):
    pkg_name = os.path.basename(pkg_dir.rstrip('/'))
    logging.info(f"处理包: {pkg_name}")
    os.chdir(pkg_dir)
    try:
        subprocess.run(['bloom-generate', 'rosrpm', '--os-name', 'openeuler', '--os-version', '24.03', '--ros-distro', 'jazzy'], check=True)
    except subprocess.CalledProcessError:
        logging.error(f"bloom-generate 失败，跳过包 {pkg_name}")
        os.chdir(BASE_DIR)
        return

    rpm_dir = os.path.join(pkg_dir, 'rpm')
    if not os.path.isdir(rpm_dir):
        logging.warning(f"rpm 目录不存在，跳过包 {pkg_name}")
        os.chdir(BASE_DIR)
        return

    template_spec = os.path.join(rpm_dir, 'template.spec')
    if not os.path.isfile(template_spec):
        logging.warning(f"template.spec 文件不存在，跳过包 {pkg_name}")
        os.chdir(BASE_DIR)
        return

    # 提取 Name 和 Version
    with open(template_spec, 'r', encoding='utf-8') as f:
        spec_content = f.read()

    name_match = re.search(r'^Name:\s+(\S+)', spec_content, re.MULTILINE)
    version_match = re.search(r'^Version:\s+(\S+)', spec_content, re.MULTILINE)

    if not name_match or not version_match:
        logging.warning(f"无法提取 Name 或 Version，跳过包 {pkg_name}")
        os.chdir(BASE_DIR)
        return

    name = name_match.group(1)
    version = version_match.group(1)
    logging.info(f"包名: {name}, 版本: {version}")

    # 重命名 template.spec
    spec_name = f"{name}.spec"
    new_spec_path = os.path.join(rpm_dir, spec_name)
    os.rename(template_spec, new_spec_path)

    # 复制 spec 文件到 SPECS 目录
    subprocess.run(['cp', new_spec_path, SPECS_DIR], check=True)

    # 定义新的目录名称
    new_dir_name = f"{name}-{version}"
    target_dir = os.path.join(BASE_DIR, new_dir_name)

    # 检查目标目录是否已存在
    if os.path.isdir(target_dir):
        logging.info(f"目标目录 {target_dir} 已存在，删除旧目录。")
        subprocess.run(['rm', '-rf', target_dir], check=True)

    # 复制包目录到新的目标目录
    subprocess.run(['cp', '-r', pkg_dir, target_dir], check=True)

    # 压缩重命名后的目录
    tar_file = f"{new_dir_name}.tar.gz"
    subprocess.run(['tar', '-czvf', tar_file, '-C', BASE_DIR, new_dir_name], check=True)

    # 复制压缩文件到 SOURCES 目录
    subprocess.run(['cp', tar_file, SOURCES_DIR], check=True)

    # 清理临时文件
    subprocess.run(['rm', '-f', tar_file])
    subprocess.run(['rm', '-rf', target_dir])

    logging.info(f"包 {pkg_name} 处理完成。")

def process_ros_packages():
    setup_directories()
    for item in os.listdir(BASE_DIR):
        pkg_dir = os.path.join(BASE_DIR, item)
        if os.path.isdir(pkg_dir):
            process_package(pkg_dir)
    logging.info("所有包处理完毕。")
