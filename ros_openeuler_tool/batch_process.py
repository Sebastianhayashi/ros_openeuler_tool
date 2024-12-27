import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_parent_process_script(pkg_path):
    parent_dir = os.path.dirname(pkg_path)
    pkg_basename = os.path.basename(pkg_path)

    # 生成唯一脚本名称，避免和其他线程冲突
    tmp_script_name = f"process_ros_packages_{uuid.uuid4().hex}.sh"
    tmp_script_path = os.path.join(parent_dir, tmp_script_name)

    # 拷贝脚本到 parent_dir
    try:
        subprocess.run(['cp', '-f', PROCESS_SCRIPT, tmp_script_path], check=True)
        os.chmod(tmp_script_path, 0o755)
    except subprocess.CalledProcessError as e:
        logging.error(f"无法复制脚本到 {parent_dir}: {e}")
        return

    # 执行脚本
    try:
        result = subprocess.run([tmp_script_path, pkg_basename],
                                cwd=parent_dir,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = (e.stdout or "") + (e.stderr or "")
        logging.error(f"执行脚本失败: {pkg_basename}\n{output}")
    finally:
        # 删除临时脚本
        if os.path.exists(tmp_script_path):
            os.remove(tmp_script_path)

    # 后续解析 output，记录跳过包、缺失依赖等...

def batch_process_packages():
    setup_logging()
    search_root = os.getcwd()
    all_packages = collect_ros_packages(search_root)
    logging.info(f"共收集到 {len(all_packages)} 个 ROS 包，准备并行执行...")

    with ThreadPoolExecutor(max_workers=PARALLEL_JOBS) as executor:
        futures = [executor.submit(run_parent_process_script, pkg) for pkg in all_packages]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"批量处理时发生错误: {e}")

    logging.info("所有包批量处理完成。")