import asyncio
from services.hk_stock_service_async import HkStockServiceAsync
from services.a_stock_service_async import AStockServiceAsync

"""
快速测试港股和A股搜索功能是否修复
"""

async def test_stock_search():
    print("\n===== 快速搜索测试 =====\n")
    
    # 初始化服务
    hk_service = HkStockServiceAsync()
    # a_service = AStockServiceAsync()
    
    # 港股测试
    print("\n----- 测试港股搜索 -----")
    try:
        # 使用较短的关键词
        hk_results = await hk_service.search_hk_stocks("00")
        print(f"找到 {len(hk_results)} 条港股结果")
        
        # 打印第一条结果的所有字段
        if len(hk_results) > 0:
            print("第一条港股结果字段:")
            for key, value in hk_results[0].items():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"港股搜索失败: {str(e)}")
    
    # # A股测试
    # print("\n----- 测试A股搜索 -----")
    # try:
    #     # 使用较短的关键词
    #     a_results = await a_service.search_a_stocks("60")
    #     print(f"找到 {len(a_results)} 条A股结果")
        
    #     # 打印第一条结果的所有字段
    #     if len(a_results) > 0:
    #         print("第一条A股结果字段:")
    #         for key, value in a_results[0].items():
    #             print(f"  {key}: {value}")
    # except Exception as e:
    #     print(f"A股搜索失败: {str(e)}")
    
    # print("\n===== 测试完成 =====")

if __name__ == "__main__":
    asyncio.run(test_stock_search()) 