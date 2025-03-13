import asyncio
import httpx
import json

"""
手动测试不同市场的股票搜索API功能
测试按代码和按名称搜索

使用方法:
python -m tests.manual_test_api
"""

# API基础URL
BASE_URL = "http://localhost:8888/api"

async def test_api():
    print("\n===== API搜索测试开始 =====\n")
    
    # 测试关键词
    a_stock_code = "600"     # A股代码搜索
    a_stock_name = "银行"     # A股名称搜索
    hk_stock_code = "00"     # 港股代码搜索
    hk_stock_name = "腾讯"     # 港股名称搜索
    us_stock_code = "A"      # 美股代码搜索
    us_stock_name = "GOOGL"  # 美股名称搜索
    
    # 创建异步HTTP客户端
    async with httpx.AsyncClient() as client:
        # A股API测试
        print("\n----- A股API搜索测试 -----")
        
        print(f"\n>> 按代码搜索 A股API: '{a_stock_code}'")
        a_code_response = await client.get(f"{BASE_URL}/search_a_stocks", params={"keyword": a_stock_code})
        print_api_results(a_code_response)
        
        print(f"\n>> 按名称搜索 A股API: '{a_stock_name}'")
        a_name_response = await client.get(f"{BASE_URL}/search_a_stocks", params={"keyword": a_stock_name})
        print_api_results(a_name_response)
        
        # 港股API测试
        print("\n----- 港股API搜索测试 -----")
        
        print(f"\n>> 按代码搜索 港股API: '{hk_stock_code}'")
        hk_code_response = await client.get(f"{BASE_URL}/search_hk_stocks", params={"keyword": hk_stock_code})
        print_api_results(hk_code_response)
        
        print(f"\n>> 按名称搜索 港股API: '{hk_stock_name}'")
        hk_name_response = await client.get(f"{BASE_URL}/search_hk_stocks", params={"keyword": hk_stock_name})
        print_api_results(hk_name_response)
        
        # 美股API测试
        print("\n----- 美股API搜索测试 -----")
        
        print(f"\n>> 按代码搜索 美股API: '{us_stock_code}'")
        us_code_response = await client.get(f"{BASE_URL}/search_us_stocks", params={"keyword": us_stock_code})
        print_api_results(us_code_response)
        
        print(f"\n>> 按名称搜索 美股API: '{us_stock_name}'")
        us_name_response = await client.get(f"{BASE_URL}/search_us_stocks", params={"keyword": us_stock_name})
        print_api_results(us_name_response)
    
    print("\n===== API搜索测试结束 =====\n")


def print_api_results(response):
    """格式化打印API响应结果"""
    print(f"  状态码: {response.status_code}")
    
    if response.status_code != 200:
        print(f"  错误: {response.text}")
        return
    
    data = response.json()
    results = data.get("results", [])
    
    if not results:
        print("  未找到结果")
        return
    
    # 只显示前5个结果
    results = results[:5]
    
    print(f"  找到 {len(results)} 条结果:")
    for i, stock in enumerate(results, 1):
        print(f"  {i}. 代码: {stock.get('symbol', 'N/A')} | 名称: {stock.get('name', 'N/A')} | 市场: {stock.get('market', 'N/A')} | 价格: {stock.get('price', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(test_api()) 