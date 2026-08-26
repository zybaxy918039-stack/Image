import asyncio
import os
import aiohttp
import itertools

# ==================== 配置区域 ====================
# 1. 设置下载保存的根目录
SAVE_DIR = r"D:\sillytavern-image\独占配信"

# 2. 分开定义两个变量集合（在列表里填入你需要的内容）
#VAR1_LIST = ["红莲", "星极","奈雅丽","艾克莉西娅","法露特","奥契丝","吉普莉尔","亚丝娜","露露卡","白","卡提希娅"]
#VAR1_LIST = ["爱弥斯", "璐米欧儿","史蒂芬妮","达妮娅"]
#VAR1_LIST = ["亚里沙", "玛格","奈叶香","梅露露","诺亚","米莉亚","蕾雅","可可","汉娜","安安","雪莉","希罗","艾玛","月代雪"]
#VAR1_LIST = ["叶瞬光","莉贝尔"]
VAR1_LIST = ["东雪莲", "塔菲", "斯黛拉", "时雨羽衣", "沙花叉", "璃亚梦", "红蔷薇"]
VAR2_LIST = ["乳交", "事后口交", "亲吻", "传教士体位做爱", "做爱射精", "做爱高潮", "口交", "后入做爱", "吮吸乳头", "女上位做爱", "射外面事后", "打屁股后入", "抱着摸小穴", "抱腿站着后入", "抱起来做爱", "指交", "掰开小穴", "摸胸", "激烈站着后入", "站着后入", "素股", "背后坐位做爱", "脱衣服", "自己掰开小穴", "自慰", "舔小穴", "足交", "趴着口交", "躺着抬腿做爱"]
VAR3_LIST = ["1", "2", "3","4","5","6","7"]

# 3. 并发限制（防止同时发起太多请求被服务器封 IP）
CONCURRENT_LIMIT = 5
# ==================================================


async def download_file(semaphore, session, var1, var2, var3, save_dir, base_url_template):
    """单文件下载协程"""
    url = base_url_template.format(var1, var2, var3)
    file_name = f"{var2}{var3}.webp"
    
    # 自动按 $1 创建子文件夹
    target_dir = os.path.join(save_dir, var1)
    save_path = os.path.join(target_dir, file_name)

    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    os.makedirs(target_dir, exist_ok=True)
                    content = await response.read()
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    print(f"[成功] 已下载: {var1}/{file_name}")
                elif response.status == 404:
                    print(f"[跳过] 资源不存在 (404): {url}")
                else:
                    print(f"[失败] HTTP 状态码 {response.status}: {url}")
        except Exception as e:
            print(f"[报错] 下载出错 {url}: {e}")

async def main():
    #创世回廊
    #base_url_template = "http://rpg.bolt.qzz.io/NSFW/{}/{}{}.webp" 
    base_url_template = "http://anchor.bolt.qzz.io/NSFW/{}/{}{}.webp"
    #base_url_template = "http://r2-proxy.saugrodep.workers.dev/b/moshen/NSFW/{}/{}{}.webp"
    os.makedirs(SAVE_DIR, exist_ok=True)
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
    timeout = aiohttp.ClientTimeout(total=60)

    # 使用 itertools.product 自动将两个独立的集合进行交叉组合
    tasks_combinations = list(itertools.product(VAR1_LIST, VAR2_LIST,VAR3_LIST))
    
    print(f"开始下载任务，变量1共 {len(VAR1_LIST)} 个，变量2共 {len(VAR2_LIST)} 个，变量3: {len(VAR3_LIST)} 个, 组合后共计 {len(tasks_combinations)} 个文件...")

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            download_file(semaphore, session, var1, var2, var3, SAVE_DIR, base_url_template)
            for var1, var2, var3 in tasks_combinations
        ]
        await asyncio.gather(*tasks)

    print("所有下载任务已结束。")

if __name__ == "__main__":
    asyncio.run(main())
