# ros_openeuler_tool/make_public.py

import os
import requests
import sys
import argparse
import logging
from urllib.parse import urljoin

# 配置日志
logging.basicConfig(
    filename='make_gitee_repos_public.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

GITEE_API_BASE = "https://gitee.com/api/v5/"
GITEE_TOKEN = os.getenv('GITEE_TOKEN')

if not GITEE_TOKEN:
    logging.error("请在环境变量 GITEE_TOKEN 中设置您的 Gitee 个人访问令牌。")
    print("错误: 请在环境变量 GITEE_TOKEN 中设置您的 Gitee 个人访问令牌。")
    sys.exit(1)

GITEE_ORG = os.getenv('GITEE_ORG')

def get_repos(page=1, per_page=100):
    if GITEE_ORG:
        url = urljoin(GITEE_API_BASE, f'orgs/{GITEE_ORG}/repos')
    else:
        url = urljoin(GITEE_API_BASE, 'user/repos')

    headers = {
        'Authorization': f'token {GITEE_TOKEN}'
    }

    params = {
        'page': page,
        'per_page': per_page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"获取仓库列表失败: {response.status_code} - {response.text}")
        print(f"获取仓库列表失败: {response.status_code} - {response.text}")
        sys.exit(1)

def make_repo_public(owner, repo):
    url = urljoin(GITEE_API_BASE, f'repos/{owner}/{repo}')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {GITEE_TOKEN}'
    }

    data = {
        'private': False
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        logging.info(f"已成功将仓库设为公开: {owner}/{repo}")
        print(f"已成功将仓库设为公开: {owner}/{repo}")
        return True
    else:
        logging.error(f"设置仓库公开失败: {owner}/{repo} - {response.status_code} - {response.text}")
        print(f"设置仓库公开失败: {owner}/{repo} - {response.status_code} - {response.text}")
        return False

def make_repos_public():
    parser = argparse.ArgumentParser(description="批量将 Gitee 私人仓库转换为公开仓库")
    parser.add_argument('--dry-run', action='store_true', help="仅列出将要转换的仓库，不执行转换操作")
    args = parser.parse_args()

    logging.info("开始获取仓库列表...")
    all_repos = []
    page = 1
    per_page = 100
    while True:
        repos = get_repos(page, per_page)
        if not repos:
            break
        all_repos.extend(repos)
        page += 1

    private_repos = [repo for repo in all_repos if repo.get('private')]

    if not private_repos:
        logging.info("没有找到任何私人仓库。")
        print("没有找到任何私人仓库。")
        sys.exit(0)

    logging.info(f"共找到 {len(private_repos)} 个私人仓库。")
    print(f"共找到 {len(private_repos)} 个私人仓库。")
    print("以下是私人仓库列表：")
    for repo in private_repos:
        print(f"- {repo['full_name']}")

    if args.dry_run:
        print("\n--dry-run 参数已启用，仅列出将要转换的仓库。")
        sys.exit(0)

    confirm = input("您确定要将以上所有私人仓库设为公开吗？此操作不可逆！请输入 'yes' 以继续：")
    if confirm.lower() != 'yes':
        print("操作已取消。")
        sys.exit(0)

    made_public = []
    for repo in private_repos:
        owner = repo['owner']['login']
        repo_name = repo['name']
        success = make_repo_public(owner, repo_name)
        if success:
            made_public.append(repo['html_url'])

    if made_public:
        logging.info("\n以下仓库已成功设为公开：")
        print("\n以下仓库已成功设为公开：")
        for repo_link in made_public:
            print(repo_link)
    else:
        logging.info("\n没有仓库被成功设为公开。")
        print("\n没有仓库被成功设为公开。")

    logging.info("\n所有操作完成。")
    print("\n所有操作完成。")
