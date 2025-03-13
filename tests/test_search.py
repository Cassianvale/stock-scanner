import pytest
import asyncio
from services.a_stock_service_async import AStockServiceAsync
from services.hk_stock_service_async import HkStockServiceAsync
from services.us_stock_service_async import USStockServiceAsync
import httpx

# 初始化测试服务
a_stock_service = AStockServiceAsync()
hk_stock_service = HkStockServiceAsync()
us_stock_service = USStockServiceAsync()

# API基础URL
BASE_URL = "http://localhost:8888/api"


# ============== 单元测试 ==============

@pytest.mark.asyncio
async def test_search_a_stock_by_code():
    """测试按代码搜索A股"""
    # 使用一个常见的股票代码前缀进行测试，如"600"(沪市)
    keyword = "600"
    results = await a_stock_service.search_a_stocks(keyword)
    
    assert len(results) > 0, "应该能找到以600开头的A股"
    
    # 验证返回的结果格式是否正确
    for stock in results:
        assert "symbol" in stock, "结果应包含股票代码"
        assert "name" in stock, "结果应包含股票名称"
        assert "market" in stock, "结果应包含市场信息"
        # 验证是否为A股(沪A)
        assert stock["symbol"].startswith("600"), "股票代码应以600开头"
        assert stock["market"] == "沪A", "市场应为沪A"


@pytest.mark.asyncio
async def test_search_a_stock_by_name():
    """测试按名称搜索A股"""
    # 使用一个常见的股票名称关键词进行测试，如"银行"
    keyword = "银行"
    results = await a_stock_service.search_a_stocks(keyword)
    
    assert len(results) > 0, "应该能找到名称包含'银行'的A股"
    
    # 验证返回的结果格式是否正确
    for stock in results:
        assert "symbol" in stock, "结果应包含股票代码"
        assert "name" in stock, "结果应包含股票名称"
        assert "market" in stock, "结果应包含市场信息"
        # 验证名称包含关键词
        assert keyword in stock["name"], f"股票名称应包含'{keyword}'"


@pytest.mark.asyncio
async def test_search_hk_stock_by_code():
    """测试按代码搜索港股"""
    # 使用一个常见的港股代码前缀进行测试，如"00"
    keyword = "00"
    results = await hk_stock_service.search_hk_stocks(keyword)
    
    assert len(results) > 0, "应该能找到代码包含'00'的港股"
    
    # 验证返回的结果格式是否正确
    for stock in results:
        assert "symbol" in stock, "结果应包含股票代码"
        assert "name" in stock, "结果应包含股票名称"
        assert "market" in stock, "结果应包含市场信息"
        assert stock["market"] == "港股", "市场应为港股"


@pytest.mark.asyncio
async def test_search_hk_stock_by_name():
    """测试按名称搜索港股"""
    # 使用一个常见的港股名称关键词进行测试，如"腾讯"
    keyword = "腾讯"
    results = await hk_stock_service.search_hk_stocks(keyword)
    
    assert len(results) > 0, "应该能找到名称包含'腾讯'的港股"
    
    # 验证返回的结果格式是否正确
    for stock in results:
        assert "symbol" in stock, "结果应包含股票代码"
        assert "name" in stock, "结果应包含股票名称"
        assert "market" in stock, "结果应包含市场信息"
        # 验证名称包含关键词
        assert keyword in stock["name"], f"股票名称应包含'{keyword}'"


@pytest.mark.asyncio
async def test_search_us_stock_by_code():
    """测试按代码搜索美股"""
    # 使用一个常见的美股代码前缀进行测试
    keyword = "A"
    results = await us_stock_service.search_us_stocks(keyword)
    
    assert len(results) > 0, "应该能找到代码包含'A'的美股"


@pytest.mark.asyncio
async def test_search_us_stock_by_name():
    """测试按名称搜索美股"""
    # 使用一个常见的美股名称关键词进行测试，如"Apple"
    keyword = "Apple"
    results = await us_stock_service.search_us_stocks(keyword)
    
    assert len(results) > 0, "应该能找到名称包含'Apple'的美股"


# ============== API测试 ==============

@pytest.mark.asyncio
async def test_api_search_a_stock():
    """测试A股搜索API"""
    async with httpx.AsyncClient() as client:
        # 使用代码搜索
        response = await client.get(f"{BASE_URL}/search_a_stocks", params={"keyword": "600"})
        assert response.status_code == 200, "API应返回200状态码"
        data = response.json()
        assert "results" in data, "返回数据应包含results字段"
        assert len(data["results"]) > 0, "应返回搜索结果"
        
        # 使用名称搜索
        response = await client.get(f"{BASE_URL}/search_a_stocks", params={"keyword": "银行"})
        assert response.status_code == 200, "API应返回200状态码"
        data = response.json()
        assert len(data["results"]) > 0, "应返回搜索结果"


@pytest.mark.asyncio
async def test_api_search_hk_stock():
    """测试港股搜索API"""
    async with httpx.AsyncClient() as client:
        # 使用代码搜索
        response = await client.get(f"{BASE_URL}/search_hk_stocks", params={"keyword": "00"})
        assert response.status_code == 200, "API应返回200状态码"
        data = response.json()
        assert "results" in data, "返回数据应包含results字段"
        assert len(data["results"]) > 0, "应返回搜索结果"
        
        # 使用名称搜索
        response = await client.get(f"{BASE_URL}/search_hk_stocks", params={"keyword": "腾讯"})
        assert response.status_code == 200, "API应返回200状态码"
        data = response.json()
        assert len(data["results"]) > 0, "应返回搜索结果"


@pytest.mark.asyncio
async def test_api_search_us_stock():
    """测试美股搜索API"""
    async with httpx.AsyncClient() as client:
        # 使用代码搜索
        response = await client.get(f"{BASE_URL}/search_us_stocks", params={"keyword": "A"})
        assert response.status_code == 200, "API应返回200状态码"
        data = response.json()
        assert "results" in data, "返回数据应包含results字段"
        assert len(data["results"]) > 0, "应返回搜索结果"
        
        # 使用名称搜索
        response = await client.get(f"{BASE_URL}/search_us_stocks", params={"keyword": "Apple"})
        assert response.status_code == 200, "API应返回200状态码"
        data = response.json()
        assert len(data["results"]) > 0, "应返回搜索结果"


# 运行测试
if __name__ == "__main__":
    asyncio.run(pytest.main(["-xvs", __file__]))
