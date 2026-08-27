import asyncio
import os
import aiohttp
import itertools

# ==================== 配置区域 ====================
# 1. 设置下载保存的根目录
SAVE_DIR = r"D:\Image\猫狗日记"

# 2. 分开定义两个变量集合（在列表里填入你需要的内容）
#VAR1_LIST = ["红莲", "星极","奈雅丽","艾克莉西娅","法露特","奥契丝","吉普莉尔","亚丝娜","露露卡","白","卡提希娅"]
#VAR1_LIST = ["爱弥斯", "璐米欧儿","史蒂芬妮","达妮娅"]
#VAR1_LIST = ["亚里沙", "玛格","奈叶香","梅露露","诺亚","米莉亚","蕾雅","可可","汉娜","安安","雪莉","希罗","艾玛","月代雪"]
#VAR1_LIST = ["叶瞬光","莉贝尔"]
#VAR1_LIST = ["东雪莲", "塔菲", "斯黛拉", "时雨羽衣", "沙花叉", "璃亚梦", "红蔷薇"]
VAR1_LIST = ["夏目", "姜涵", "孟凡雨", "安梓静", "林熙照", "水月", "温婉清", "温念", "白团", "苏小小"]
VAR2_LIST = ["乳交", "从背后摸胸", "仰姿暴露小穴", "做爱事后", "做爱预备", "发情自慰", "口交", "后入肛交做爱", "女上位做爱", "女上位揉胸做爱", "委屈", "宠物式吃精液", "宠物式撒尿", "宠物式漏精", "宠物式牵绳散步", "展示胸部", "惩罚不听话做爱", "惩罚不听话开始", "惩罚不听话掰穴", "惩罚不听话肉棒插入", "惩罚不听话舔脚", "手机壁纸", "打招呼", "托臀正面站立位做爱", "抱腿站姿做爱", "接吻", "正面传教士做爱", "正面摸胸", "正面肉棒准备插入", "正面肛交做爱", "火车便当做爱", "环抱做爱", "生气", "疯狂做爱", "站姿后入做爱", "背后视角暴露小穴", "舔主人的脚", "足交", "跪姿后入做爱", "逆向小狗式激烈做爱", "默认", "做爱高潮", "抱腿做爱", "摸胸", "自慰", "正面自抱腿做爱", "裸体乘车", "车里做爱", "性爱情趣", "舔小穴", "读书做爱", "正太站姿抱腿后入做爱", "给正太口交", "给正太授乳手交", "被小正太侧入做爱", "被小正太内射", "被正太后入做爱", "被正太后入做爱高潮", "被正太吸奶", "被正太埋胸做爱", "被正太舔穴", "跟正太一起洗澡", "跟正太一起睡觉", "跟正太拥吻做爱", "跟正太接吻", "辅导正太做作业", "发情", "宠物式栓绳散步", "惩罚不听话舔小穴", "正面位肛交做爱", "正面揉胸", "炸毛愤怒", "自我清洁", "露出胸部"]
VAR3_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

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
    #base_url_template = "http://anchor.bolt.qzz.io/NSFW/{}/{}{}.webp"
    #base_url_template = "http://r2-proxy.saugrodep.workers.dev/b/moshen/NSFW/{}/{}{}.webp"
    base_url_template = "https://r2-proxy.saugrodep.workers.dev/b/catdog/NSFW/{}/{}{}.webp"
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
