import asyncio
import json
from services.a_stock_service_async import AStockServiceAsync
from services.hk_stock_service_async import HkStockServiceAsync
from services.us_stock_service_async import USStockServiceAsync

"""
手动测试不同市场的股票搜索功能
测试按代码和按名称搜索

使用方法:
python -m tests.manual_test_search
"""

async def test_search():
    print("\n===== 搜索测试开始 =====\n")
    
    # 初始化服务
    a_stock_service = AStockServiceAsync()
    hk_stock_service = HkStockServiceAsync()
    us_stock_service = USStockServiceAsync()
    
    # 测试关键词
    a_stock_code = "600"     # A股代码搜索
    a_stock_name = "银行"     # A股名称搜索
    hk_stock_code = "00"     # 港股代码搜索
    hk_stock_name = "腾讯"     # 港股名称搜索
    us_stock_code = "A"      # 美股代码搜索
    us_stock_name = "Apple"  # 美股名称搜索
    
    # A股测试
    print("\n----- A股搜索测试 -----")
    print(f"\n>> 按代码搜索 A股: '{a_stock_code}'")
    a_stock_results_by_code = await a_stock_service.search_a_stocks(a_stock_code)
    print_results(a_stock_results_by_code[:5])  # 只显示前5个结果
    
    print(f"\n>> 按名称搜索 A股: '{a_stock_name}'")
    a_stock_results_by_name = await a_stock_service.search_a_stocks(a_stock_name)
    print_results(a_stock_results_by_name[:5])  # 只显示前5个结果
    
    # 港股测试
    print("\n----- 港股搜索测试 -----")
    print(f"\n>> 按代码搜索 港股: '{hk_stock_code}'")
    hk_stock_results_by_code = await hk_stock_service.search_hk_stocks(hk_stock_code)
    print_results(hk_stock_results_by_code[:5])  # 只显示前5个结果
    
    print(f"\n>> 按名称搜索 港股: '{hk_stock_name}'")
    hk_stock_results_by_name = await hk_stock_service.search_hk_stocks(hk_stock_name)
    print_results(hk_stock_results_by_name[:5])  # 只显示前5个结果
    
    # 美股测试
    print("\n----- 美股搜索测试 -----")
    print(f"\n>> 按代码搜索 美股: '{us_stock_code}'")
    us_stock_results_by_code = await us_stock_service.search_us_stocks(us_stock_code)
    print_results(us_stock_results_by_code[:5])  # 只显示前5个结果
    
    print(f"\n>> 按名称搜索 美股: '{us_stock_name}'")
    us_stock_results_by_name = await us_stock_service.search_us_stocks(us_stock_name)
    print_results(us_stock_results_by_name[:5])  # 只显示前5个结果
    
    print("\n===== 搜索测试结束 =====\n")


def print_results(results):
    """格式化打印搜索结果"""
    if not results:
        print("  未找到结果")
        return
        
    print(f"  找到 {len(results)} 条结果:")
    for i, stock in enumerate(results, 1):
        print(f"  {i}. 代码: {stock.get('symbol', 'N/A')} | 名称: {stock.get('name', 'N/A')} | 市场: {stock.get('market', 'N/A')} | 价格: {stock.get('price', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(test_search()) 