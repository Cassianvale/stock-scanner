import asyncio
import pandas as pd
from typing import List, Dict, Any, Optional
from utils.logger import get_logger

# 获取日志器
logger = get_logger()

class AStockServiceAsync:
    """
    A股服务
    提供A股数据的搜索和获取功能
    """
    
    def __init__(self):
        """初始化A股服务"""
        logger.debug("初始化AStockServiceAsync")
        
        # 可选：添加缓存以减少频繁请求
        self._cache = None
        self._cache_timestamp = None
    
    async def search_a_stocks(self, keyword: str) -> List[Dict[str, Any]]:
        """
        异步搜索A股代码
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的股票列表
        """
        try:
            logger.info(f"异步搜索A股: {keyword}")
            
            # 使用线程池执行同步的akshare调用
            df = await asyncio.to_thread(self._get_a_stocks_data)
            
            # 打印DataFrame的列名以进行调试
            logger.debug(f"A股数据列名: {df.columns.tolist()}")
            
            # 模糊匹配搜索（同时匹配代码和名称）
            mask = (df['name'].str.contains(keyword, case=False, na=False) | 
                   df['symbol'].str.contains(keyword, case=False, na=False))
            results = df[mask]
            
            # 格式化返回结果并处理 NaN 值
            formatted_results = []
            for _, row in results.iterrows():
                # 创建基本结果对象
                result = {
                    'name': row['name'] if pd.notna(row['name']) else '',
                    'symbol': str(row['symbol']) if pd.notna(row['symbol']) else '',
                    'market': '沪A' if str(row['symbol']).startswith('6') else '深A',
                    'price': float(row['price']) if pd.notna(row['price']) else 0.0,
                }
                
                # 如果存在市值字段，则添加
                if 'market_value' in row and pd.notna(row['market_value']):
                    result['market_value'] = float(row['market_value'])
                else:
                    # 如果不存在，使用默认值
                    result['market_value'] = 0.0
                
                formatted_results.append(result)
                
                # 限制只返回前10个结果
                if len(formatted_results) >= 10:
                    break
            
            logger.info(f"A股搜索完成，找到 {len(formatted_results)} 个匹配项（限制显示前10个）")
            return formatted_results
            
        except Exception as e:
            error_msg = f"搜索A股代码失败: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)
            raise Exception(error_msg)
            
    async def get_a_stock_detail(self, symbol: str) -> Dict[str, Any]:
        """
        异步获取单个A股详细信息
        
        Args:
            symbol: 股票代码
            
        Returns:
            股票详细信息
        """
        try:
            logger.info(f"获取A股详情: {symbol}")
            
            # 使用线程池执行同步的akshare调用
            df = await asyncio.to_thread(self._get_a_stocks_data)
            
            # 精确匹配股票代码
            result = df[df['symbol'] == symbol]
            
            if len(result) == 0:
                raise Exception(f"未找到股票代码: {symbol}")
            
            # 获取第一行数据
            row = result.iloc[0]
            
            # 格式化为字典
            stock_detail = {
                'name': row['name'] if pd.notna(row['name']) else '',
                'symbol': str(row['symbol']) if pd.notna(row['symbol']) else '',
                'market': '沪A' if str(row['symbol']).startswith('6') else '深A',
                'price': float(row['price']) if pd.notna(row['price']) else 0.0,
            }
            
            # 添加可选字段
            for field in ['price_change', 'open', 'high', 'low', 'pre_close', 
                          'market_value', 'pe_ratio', 'volume', 'turnover']:
                if field in row and pd.notna(row[field]):
                    if field == 'price_change_percent' and isinstance(row[field], str) and '%' in row[field]:
                        stock_detail[field] = float(row[field].strip('%'))/100
                    else:
                        stock_detail[field] = float(row[field])
                else:
                    stock_detail[field] = 0.0
            
            # 处理价格变化百分比
            if 'price_change_percent' in row and pd.notna(row['price_change_percent']):
                if isinstance(row['price_change_percent'], str) and '%' in row['price_change_percent']:
                    stock_detail['price_change_percent'] = float(row['price_change_percent'].strip('%'))/100
                else:
                    stock_detail['price_change_percent'] = float(row['price_change_percent'])
            else:
                stock_detail['price_change_percent'] = 0.0
            
            logger.info(f"获取A股详情成功: {symbol}")
            return stock_detail
            
        except Exception as e:
            error_msg = f"获取A股详情失败: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)
            raise Exception(error_msg)
    
    def _get_a_stocks_data(self) -> pd.DataFrame:
        """
        获取A股数据
        使用akshare库获取A股实时行情数据
        
        Returns:
            A股数据DataFrame
        """
        try:
            logger.info("获取A股数据")
            
            # 使用akshare库获取A股数据
            import akshare as ak
            df = ak.stock_zh_a_spot_em()
            
            # 打印列名以便调试
            logger.debug(f"A股原始数据列名: {df.columns.tolist()}")
            
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
                '成交额': 'turnover',
                '总市值': 'market_value',
                '市盈率': 'pe_ratio'
            }
            
            # 只映射存在的列
            actual_mapping = {}
            for original, mapped in column_mapping.items():
                if original in df.columns:
                    actual_mapping[original] = mapped
            
            # 标准化列名
            df = df.rename(columns=actual_mapping)
            
            # 输出最终的列名
            logger.debug(f"A股标准化后的列名: {df.columns.tolist()}")
            
            logger.info(f"获取到 {len(df)} 条A股数据")
            return df
            
        except Exception as e:
            error_msg = f"获取A股数据失败: {str(e)}"
            logger.error(error_msg)
            logger.exception(e)
            raise Exception(error_msg) 