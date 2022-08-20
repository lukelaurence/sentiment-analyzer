import requests
import os
import sys
from twittercredentials import set_credentials

set_credentials()
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/counts/all"
query_params = {'granularity':'hour','start_time':'2006-04-01T00:00:00Z'}

query_params['query'] = '(的 OR 是 OR 不 OR 我 OR 一 OR 有 OR 大 OR 在 OR 人 OR 了 OR 中 OR 到 OR 資 OR 要 OR 可 OR 以 OR 這 OR 個 OR 你 OR 會 OR 好 OR 為 OR 上 OR 來 OR 就 OR 學 OR 交 OR 也 OR 用 OR 能 OR 如 OR 文 OR 時 OR 沒 OR 說 OR 他 OR 看 OR 提 OR 那 OR 問 OR 生 OR 過 OR 下 OR 請 OR 天 OR 們 OR 所 OR 多 OR 麼 OR 小 OR 想 OR 得 OR 之 OR 還 OR 電 OR 出 OR 工 OR 對 OR 都 OR 機 OR 自 OR 後 OR 子 OR 而 OR 訊 OR 站 OR 去 OR 心 OR 只 OR 家 OR 知 OR 國 OR 台 OR 很 OR 信 OR 成 OR 章 OR 何 OR 同 OR 道 OR 地 OR 發 OR 法 OR 無 OR 然 OR 但 OR 嗎 OR 當 OR 於 OR 本 OR 現 OR 年 OR 前 OR 真 OR 最 OR 和 OR 新 OR 因 OR 果 OR 定 OR 意 OR 情 OR 點 OR 題 OR 其 OR 事 OR 方 OR 清 OR 科 OR 樣 OR 些 OR 吧 OR 三 OR 此 OR 位 OR 理 OR 行 OR 作 OR 經 OR 者 OR 什 OR 謝 OR 名 OR 日 OR 正 OR 華 OR 話 OR 開 OR 實 OR 再 OR 城 OR 愛 OR 與 OR 二 OR 動 OR 比 OR 高 OR 面 OR 又 OR 車 OR 力 OR 或 OR 種 OR 像 OR 應 OR 女 OR 教 OR 分 OR 手 OR 打 OR 已 OR 次 OR 長 OR 太 OR 明 OR 己 OR 路 OR 起 OR 相 OR 主 OR 關 OR 鳳 OR 間 OR 呢 OR 覺 OR 該 OR 十 OR 外 OR 凰 OR 友 OR 才 OR 民 OR 系 OR 進 OR 使 OR 她 OR 著 OR 各 OR 少 OR 全 OR 兩 OR 回 OR 加 OR 將 OR 感 OR 第 OR 性 OR 球 OR 式 OR 把 OR 被 OR 老 OR 公 OR 龍 OR 程 OR 論 OR 及 OR 別 OR 給) lang:zh-TW -is:retweet'
name = 'traditionalcounts.txt'

# query_params['query'] = '(的 OR 是 OR 不 OR 我 OR 一 OR 有 OR 大 OR 在 OR 人 OR 了 OR 中 OR 到 OR 资 OR 要 OR 可 OR 以 OR 这 OR 个 OR 你 OR 会 OR 好 OR 为 OR 上 OR 来 OR 就 OR 学 OR 交 OR 也 OR 用 OR 能 OR 如 OR 文 OR 时 OR 没 OR 说 OR 他 OR 看 OR 提 OR 那 OR 问 OR 生 OR 过 OR 下 OR 请 OR 天 OR 们 OR 所 OR 多 OR 麽 OR 小 OR 想 OR 得 OR 之 OR 还 OR 电 OR 出 OR 工 OR 对 OR 都 OR 机 OR 自 OR 后 OR 子 OR 而 OR 讯 OR 站 OR 去 OR 心 OR 只 OR 家 OR 知 OR 国 OR 台 OR 很 OR 信 OR 成 OR 章 OR 何 OR 同 OR 道 OR 地 OR 发 OR 法 OR 无 OR 然 OR 但 OR 吗 OR 当 OR 于 OR 本 OR 现 OR 年 OR 前 OR 真 OR 最 OR 和 OR 新 OR 因 OR 果 OR 定 OR 意 OR 情 OR 点 OR 题 OR 其 OR 事 OR 方 OR 清 OR 科 OR 样 OR 些 OR 吧 OR 三 OR 此 OR 位 OR 理 OR 行 OR 作 OR 经 OR 者 OR 什 OR 谢 OR 名 OR 日 OR 正 OR 华 OR 话 OR 开 OR 实 OR 再 OR 城 OR 爱 OR 与 OR 二 OR 动 OR 比 OR 高 OR 面 OR 又 OR 车 OR 力 OR 或 OR 种 OR 像 OR 应 OR 女 OR 教 OR 分 OR 手 OR 打 OR 已 OR 次 OR 长 OR 太 OR 明 OR 己 OR 路 OR 起 OR 相 OR 主 OR 关 OR 凤 OR 间 OR 呢 OR 觉 OR 该 OR 十 OR 外 OR 凰 OR 友 OR 才 OR 民 OR 系 OR 进 OR 使 OR 她 OR 着 OR 各 OR 少 OR 全 OR 两 OR 回 OR 加 OR 将 OR 感 OR 第 OR 性 OR 球 OR 式 OR 把 OR 被 OR 老 OR 公 OR 龙 OR 程 OR 论 OR 及 OR 别 OR 给) lang:zh-CN -is:retweet'
# name = 'simplifiedcounts.txt'

def bearer_oauth(r):
	"""
	Method required by bearer token authentication.
	"""

	r.headers["Authorization"] = f"Bearer {bearer_token}"
	r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
	return r

def connect_to_endpoint(params):
	response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
	if response.status_code != 200:
		raise Exception(response.status_code, response.text)
	return response.json()

with open(name,'a') as f:
	sys.stdout = f
	json_response = connect_to_endpoint(query_params)
	while True:
		try:
			query_params['next_token'] = json_response['meta']['next_token']
			json_response = connect_to_endpoint(query_params)
			for x in json_response['data']:
				print(x)
		except:
			break