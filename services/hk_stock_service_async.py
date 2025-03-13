import asyncio
import pandas as pd
from typing import List, Dict, Any, Optional
from utils.logger import get_logger

# 获取日志器
logger = get_logger()

class HkStockServiceAsync:
    """
    港股服务
    提供港股数据的搜索和获取功能
    """
    
    def __init__(self):
        """初始化港股服务"""
        logger.debug("初始化HkStockServiceAsync")
        
        # 可选：添加缓存以减少频繁请求
        self._cache = None
        self._cache_timestamp = None
    
    async def search_hk_stocks(self, keyword: str) -> List[Dict[str, Any]]:
        """
        异步搜索港股代码
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的股票列表
        """
        try:
            logger.info(f"异步搜索港股: {keyword}")
            
            # 使用线程池执行同步的akshare调用
            df = await asyncio.to_thread(self._get_hk_stocks_data)
            
            # 模糊匹配搜索（同时匹配代码和名称）
            mask = (df['name'].str.contains(keyword, case=False, na=False) | 
                   df['symbol'].str.contains(keyword, case=False, na=False))
            results = df[mask]
            
            # 格式化返回结果并处理 NaN 值
            formatted_results = []
            for _, row in results.iterrows():
                # 创建基本结果对象，始终包含必需字段，缺失的使用默认值
                result = {
                    'name': row['name'] if pd.notna(row['name']) else '',
                    'symbol': str(row['symbol']) if pd.notna(row['symbol']) else '',
                    'market': '港股',
                    'price': float(row['price']) if pd.notna(row['price']) else 0.0,
                }
                
                formatted_results.append(result)
                
                # 限制只返回前10个结果
                if len(formatted_results) >= 10:
                    break
            
            logger.info(f"港股搜索完成，找到 {len(formatted_results)} 个匹配项（限制显示前10个）")
            return formatted_results
            
        except Exception as e:
            error_msg = f"搜索港股代码失败: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)
            raise Exception(error_msg)
            
    async def get_hk_stock_detail(self, symbol: str) -> Dict[str, Any]:
        """
        异步获取单个港股详细信息
        
        Args:
            symbol: 股票代码
            
        Returns:
            股票详细信息
        """
        try:
            logger.info(f"获取港股详情: {symbol}")
            
            # 使用线程池执行同步的akshare调用
            df = await asyncio.to_thread(self._get_hk_stocks_data)
            
            # 精确匹配股票代码
            result = df[df['symbol'] == symbol]
            
            if len(result) == 0:
                raise Exception(f"未找到股票代码: {symbol}")
            
            # 获取第一行数据
            row = result.iloc[0]
            
            # 格式化为字典，包含所有必需字段
            stock_detail = {
                'name': row['name'] if pd.notna(row['name']) else '',
                'symbol': str(row['symbol']) if pd.notna(row['symbol']) else '',
                'market': '港股',
                'price': float(row['price']) if pd.notna(row['price']) else 0.0,
                # 缺失的市值字段
                'market_value': 0.0,
                # 处理可能缺失的字段
                'price_change': float(row['price_change']) if 'price_change' in row and pd.notna(row['price_change']) else 0.0,
                'price_change_percent': self._parse_percent(row.get('price_change_percent')),
                'open': float(row['open']) if 'open' in row and pd.notna(row['open']) else 0.0,
                'high': float(row['high']) if 'high' in row and pd.notna(row['high']) else 0.0,
                'low': float(row['low']) if 'low' in row and pd.notna(row['low']) else 0.0,
                'pre_close': float(row['pre_close']) if 'pre_close' in row and pd.notna(row['pre_close']) else 0.0,
                'volume': float(row['volume']) if 'volume' in row and pd.notna(row['volume']) else 0.0,
                'turnover': float(row['turnover']) if 'turnover' in row and pd.notna(row['turnover']) else 0.0,
                'pe_ratio': 0.0  # 港股数据没有pe_ratio字段
            }
            
            logger.info(f"获取港股详情成功: {symbol}")
            return stock_detail
            
        except Exception as e:
            error_msg = f"获取港股详情失败: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)
            raise Exception(error_msg)
    
    def _parse_percent(self, value) -> float:
        """解析百分比值"""
        if pd.isna(value):
            return 0.0
        if isinstance(value, str) and '%' in value:
            try:
                return float(value.strip('%')) / 100
            except ValueError:
                return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def _get_hk_stocks_data(self) -> pd.DataFrame:
        """
        获取港股数据
        使用akshare库获取港股实时行情数据
        
        Returns:
            港股数据DataFrame
        """
        try:
            logger.info("获取港股数据")
            
            # 使用akshare库获取港股数据
            import akshare as ak
            df = ak.stock_hk_spot_em()
            
            # 打印列名以便调试
            logger.info(f"港股原始数据列名: {df.columns.tolist()}")
            
            # 定义列名映射，确保处理akshare可能的命名变化
            column_mapping = {
                '代码': 'symbol',
                '名称': 'name',
                '最新价': 'price',
                '涨跌额': 'price_change',
                '涨跌幅': 'price_change_percent',
                '今开': 'open',
                '最高': 'high',
                '最低': 'low',
                '昨收': 'pre_close',
                '成交量': 'volume',
                '成交额': 'turnover'
                # 注意：没有市值字段 (market_value)
            }
            
            # 只映射存在的列
            actual_mapping = {}
            for original, mapped in column_mapping.items():
                if original in df.columns:
                    actual_mapping[original] = mapped
            
            # 标准化列名
            df = df.rename(columns=actual_mapping)
            
            # 输出最终的列名
            logger.info(f"港股标准化后的列名: {df.columns.tolist()}")
            
            logger.info(f"获取到 {len(df)} 条港股数据")
            return df
            
        except Exception as e:
            error_msg = f"获取港股数据失败: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)
            raise Exception(error_msg) 