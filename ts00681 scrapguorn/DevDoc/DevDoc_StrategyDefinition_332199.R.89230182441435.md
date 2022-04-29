
# 范例URL：
    'https://guorn.com/stock/rule/definition?id=332199.R.89230182441435'

对应页面：
    https://guorn.com/stock/strategy?sid=332199.R.89230182441435

# Json
"status": "ok", 
"data": 
	{
	"position_limit": 1, 
	"reference": "000300",
    
    标签 
	"tabs": 
		{
        策略回测    
		"back_test": 
			{
				"count": "28",  最大持仓股票数：
				"backup_num": "5", 备选买入股票数：
				"position_limit": 1, 个股最大买入仓位
				"end": "2020/08/28", 
				"min_position": 0.01, 
				"reference": "000300", 收益基准
				"trading_strategy": 
					{
						"buy_options": [], 
						"hold_options": [], 
						"sell_options": [{"id": "0.SM.\u6392\u540d\u540d\u6b21.0", "val": "20", "op": "ge"}]
					}, 
					
				"price": "close", 
				"period": 20,  调仓周期
				"position_bias": 0.3, 
				"max_count": 15, 
				"start": "2007/01/04", 
				"model": 0, 
                "trade_cost": 0.002,  # 交易成本 千分之二
				"ideal_count": 10, 
				"hedge": false, 
				"always_tradable": 0, 
				"ideal_position": 0.1, 
				"backup_fund": ""
			}, 

        每日选股			
		"screen": 
            {"date": "2020/08/28"}, 
		
        排名分析
		"rank": 
			{
                "start": "2007/01/04", 
			    "bucket_count": "10", 
			    "end": "2020/08/28", 
			    "period": 20
            }
		
        }, 
		
    "period": 20, 
    "position_bias": 0.3, 
    "max_count": 15, 
    
    筛选条件：股票每日指标_成交金额、股票每日指标_当日涨停、股票每日指标_每日跌停、股票每日指标_市盈率
    "filters": 
        [{"industry": 0, "type": "meas", "id": "0.M.\u80a1\u7968\u6bcf\u65e5\u6307\u6807_\u6210\u4ea4\u91d1\u989d.0", "val": 10000000, "op": "gt"}, {"industry": 0, "type": "meas", "id": "0.M.\u80a1\u7968\u6bcf\u65e5\u6307\u6807_\u5f53\u65e5\u6da8\u505c.0", "val": "1", "op": "lt"}, {"industry": 0, "type": "meas", "id": "0.M.\u80a1\u7968\u6bcf\u65e5\u6307\u6807_\u5f53\u65e5\u8dcc\u505c.0", "val": "1", "op": "lt"}, {"industry": 0, "type": "meas", "id": "0.M.\u80a1\u7968\u6bcf\u65e5\u6307\u6807_\u5e02\u76c8\u7387.0", "val": "0", "op": "gt"}], 
        
    "id": "402748.R.184239701155518",  ？？？有时还会弹出402748.R.184259127555410 
    "derived_indicators": [], 
    "category": "stock", 
    "saveas": true, 
    "end": "2020/08/28", 
    "start": "2007/01/05", 
    "desc": "", 
    "exclude_st": "1", 
    "ideal_count": 10, 
    "live_instr_date": null, 
    "trading_strategy": 
        {	
            "buy_options": [], 
            "hold_options": [], 
            "sell_options": 
                [{"id": "0.SM.\u6392\u540d\u540d\u6b21.0", "val": "20", "op": "ge"}] #排名名次>20
        }, 
    "price": "close", 
    "visibility": 2, 
    "timing": 
        {
        "indicators": [], 
        "position": "0", 
        "threshold": 
            ["-1", "-1"]
        },
    "current_tab": "back_test", 
    "hedge": false, 
    "always_tradable": 0, 
    "ideal_position": 0.1, 
    "strategy_source": 1, 
    "backup_fund": "", 
    "count": 28, 
    "backup_num": 5, 
    "trade_cost": 0.002, 
    "name": "TTM\u5e02\u76c8\u7387", 
    "min_position": 0.01, 

    排名条件
    "ranks": 
        [{"asc": true, "industry": 0, 
        "id": "0.M.\u80a1\u7968\u6bcf\u65e5\u6307\u6807_\u5e02\u76c8\u7387.0",  股票每日指标_市盈率
        "weight": 1}], 
    "pool_defn": [], 
    "model": 0
    }
    }